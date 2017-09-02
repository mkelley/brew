# Licensed under an MIT style license - see LICENSE

"""
brew --- Brew some beer.
========================

"""

__all__ = [
    'Brew',
]

class Brew:
    """Brew some beer.

    Default values for optional parameters are retrieved from
    `configuration`.

    Parameters
    ----------
    ingredients : Ingredients
      Ingredients.
    target_volume : float
      The target wort volume in the primary, before any `Primary`
      additions, gallons.

    parameter_sets : list of strings, optional
      Load these parameter sets from the configuration file (in
      order), before processing optional keyword values.

    r_mash : float, optional
      Ratio of water volume to grain weight, qt/lb.
    absorption : float, optional
      Water absorption for grain, qt/lb.
    T_grain : int, optional
      Dry grain temperature.
    T_water : int, optional
      Water temperature for step infusions.
    T_rest : int or array-like, optional
      Initial (pre-saccharification) rest temperature(s).
    T_sacc : int or array-like, optional
      The saccharification temperature step(s).
    mash_out : bool, optional
      Set to `True` to add a mash-out step, targeting 170 F.
    efficiency : float, optional
      The efficiency of the mash and lauter, from 0 to 1.0.
    mlt_gap : float, optional
      Leftover volume in MLT after lauter, gal.

    boil_time : float, optional
      The boil time in minutes.
    r_boil : float, optional
      Boil-off rate, gal/hr.
    kettle_gap : float, optional
      Leftover volume in kettle after racking, gal.

    attenuation : float, optional
      Use this apparent attentuation percentage.

    """

    def __init__(self, ingredients, target_volume, parameter_sets=['default'],
                 **kwargs):
        from collections import Iterable
        from .configuration import get_config
        from .ingredients import Ingredients

        assert isinstance(ingredients, Ingredients)
        assert isinstance(target_volume, (float, int))
        
        self.ingredients = ingredients
        self.target_volume = float(target_volume)
        self.config = get_config(parameter_sets)
        self.config.update(kwargs)

        # sanitize inputs
        self['r_mash'] = float(self['r_mash'])
        self['absorption'] = float(self['absorption'])
        self['T_grain'] = int(self['T_grain'])
        self['T_water'] = int(self['T_water'])
        self['T_rest'] = tuple(self['T_rest']) if isinstance(self['T_rest'], Iterable) else (self['T_rest'],)
        self['T_sacc'] = tuple(self['T_sacc']) if isinstance(self['T_sacc'], Iterable) else (self['T_sacc'],)
        assert isinstance(self['mash_out'], bool)
        self['efficiency'] = float(self['efficiency'])
        self['mlt_gap'] = float(self['mlt_gap'])

        self['boil_time'] = float(self['boil_time'])
        self['r_boil'] = float(self['r_boil'])
        self['kettle_gap'] = float(self['kettle_gap'])
 
    def __getitem__(self, k):
        return self.config[k]

    def __setitem__(self, k, v):
        assert k in self.config, '{} is not parameter ({})'.format(k, ', '.join(self.config.keys()))
        self.config[k] = v

    @property
    def T_mash(self):
        T = self['T_rest'] + self['T_sacc']
        if self['mash_out']:
            T += (170,)
        return T
        
    def volume(self, time):
        """Volume at time in gallons.

        Parameters
        ----------
        time : Timing
          Include all additions up to and at `time`.

        """

        from . import timing as T
        
        ingredients = self.ingredients.at(time)
        volume = sum([i.volume for i in ingredients if hasattr(i, 'volume')])
        volume += self.target_volume
        
        if time < T.Primary():
            volume += self['kettle_gap']

        if isinstance(time, T.Boil):
            t = min(self['boil_time'], time.time)
            volume += t / 60 * self['r_boil']
        elif time < T.Boil(self['boil_time']):
            volume += self['boil_time'] / 60 * self['r_boil']
        
        if time < T.Lauter():
            weight = sum([f.weight for f in ingredients.grains])
            volume += self['mlt_gap'] + weight * self['absorption'] / 4

        return volume
        
    def extract(self, time):
        """Extract at time.

        Parameters
        ----------
        time : Timing
          Include all additions up to and at `time`.

        """

        from . import timing as T
        
        ingredients = self.ingredients.fermentables.at(time)
        extract = [f.extract(self['efficiency']) for f in ingredients.at(T.Sparge())]
        extract.extend([f.extract(1.0) for f in ingredients.after(T.Sparge())])
        return extract

    def mash(self):
        """Mash and lauter grains to make wort.

        Returns
        -------
        wort : Wort
          The pre-boil wort.

        """

        from . import timing as T
        from .table import Table

        ingredients = self.ingredients.at(T.Lauter())
        total_weight = sum([f.weight for f in ingredients])
        grain_weight = sum([f.weight for f in ingredients.grains])

        v_kettle = self.volume(T.Lauter())
        extract = self.extract(T.Lauter())
        total_extract = sum(extract)
        
        sg = 1 + total_extract / v_kettle / 1000
        wort = Wort(sg, v_kettle)

        T_infusion, v_infusion, v_sparge = self.infusion()
        v_mash = sum(v_infusion)

        # Extract table
        tab = Table(data=([i.name for i in ingredients],
                          [i.timing.name for i in ingredients],
                          [i.weight for i in ingredients],
                          [i.weight / total_weight for i in ingredients],
                          [i.ppg for i in ingredients],
                          extract,
                          [ex / total_extract for ex in extract]),
                    names=('Grain/Adjunct', 'Timing', 'Weight',
                           'Weight Fraction', 'PPG', 'Extract',
                           'Extract Fraction'))
        tab.colformats = ('{}', '{}', '{:.3f}', '{:.1%}', '{:d}', '{:.1f}',
                          '{:.1%}')
        tab.footer = '''Kettle volume: {:.1f} gal
Efficiency: {:.0%}
Pre-boil specific gravity: {:.3f}
'''.format(v_kettle, self['efficiency'], sg)

        print(tab)
        
        # Infusion schedule table
        tab = Table(data=(self.T_mash, T_infusion, v_infusion),
                    names=('T mash (F)', 'T water (F)', 'Volume (gal)'))
        tab.colformats = ('{:.0f}', '{:.0f}', '{:.2f}')
        tab.footer = '''Total mash water: {:.1f} gal ({:.1f} qt/lb)
Sparge with {:.1f} gal of water
Collect {:.1f} gal of wort
'''.format(v_mash, v_mash * 4 / grain_weight, v_sparge, v_kettle)

        print(tab)

        return wort

    def infusion(self):
        """Strike water and infusion volumes.

        Returns
        -------
        T_infusion : tuple of float
          Water temperatures, °F.
        v_infusion : tuple of float
          Infusion volumes, gallons.
        v_sparge : float
          Sparge water volume, gallons.

        """
        
        from . import timing as T
        from .util import strike_water, infusion_volume
        
        grain_weight = sum([f.weight for f in
                            self.ingredients.at(T.Sparge()).grains])
        v_infusion = []
        T_infusion = []
        for i in range(len(self.T_mash)):
            if i == 0:
                v_infusion.append(self['r_mash'] * grain_weight / 4)
                T_strike = strike_water(self['r_mash'], self['T_grain'],
                                        self.T_mash[0])
                T_infusion.append(T_strike)
            else:
                v = infusion_volume(sum(v_infusion) * 4, grain_weight,
                                    self.T_mash[i-1], self.T_mash[i])
                v_infusion.append(v / 4)
                T_infusion.append(self['T_water'])

        v_mash = sum(v_infusion)
        v_sparge = self.volume(T.Sparge()) - v_mash
        assert v_sparge >= 0, 'Negative sparge volume, lower r_mash or change temperature steps.'

        return tuple(T_infusion), tuple(v_infusion), v_sparge
        

class Wort:
    """Wort.

    Parameters
    ----------
    gravity : float
      Specific gravity.
    volume : float
      Volume in gallons.
    bitterness : float, optional
      Bitterness in IBUs.

    """
    
    def __init__(self, gravity, volume, bitterness=None):
        self.gravity = gravity
        self.volume = volume
        self.bitterness = bitterness

