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

    parameter_sets : string or list of strings, optional
      Load these parameter sets from the configuration file (in
      order), after loading the defaults and before processing
      optional keyword values.

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
    hop_stand : bool, optional
      Hop stand after boil.
    kettle_gap : float, optional
      Leftover volume in kettle after racking, gal.

    attenuation : float, optional
      Use this apparent attentuation percentage.

    """

    def __init__(self, ingredients, target_volume, parameter_sets=None,
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
        self['T_rest'] = tuple(self['T_rest']) if isinstance(
            self['T_rest'], Iterable) else (self['T_rest'],)
        self['T_sacc'] = tuple(self['T_sacc']) if isinstance(
            self['T_sacc'], Iterable) else (self['T_sacc'],)
        assert isinstance(self['mash_out'], bool)
        self['efficiency'] = float(self['efficiency'])
        self['mlt_gap'] = float(self['mlt_gap'])

        self['boil_time'] = float(self['boil_time'])
        self['r_boil'] = float(self['r_boil'])
        assert isinstance(self['hop_stand'], bool)
        self['kettle_gap'] = float(self['kettle_gap'])

    def __getitem__(self, k):
        return self.config[k]

    def __setitem__(self, k, v):
        assert k in self.config, '{} is not parameter ({})'.format(
            k, ', '.join(self.config.keys()))
        self.config[k] = v

    @property
    def T_mash(self):
        T = self['T_rest'] + self['T_sacc']
        if self['mash_out']:
            T += (170,)
        return T

    @property
    def hop_stand(self):
        """Post-boil hop stand?

        `True` if any ingredient is added in a hop stand or if the
        `hop_stand` parameter is enabled.

        """
        return self['hop_stand'] or (len(self.ingredients.hop_stand) > 0)

    def volume(self, time, upto=False):
        """Volume at time in gallons.

        Parameters
        ----------
        time : Timing
          The time to consider.
        upto : bool, optional
          Include all additions up to `time`, but not at `time`.

        """

        from . import timing as T

        if upto:
            ingredients = self.ingredients.upto(time)
        else:
            ingredients = self.ingredients.at(time)

        volume = sum([i.volume for i in ingredients if hasattr(i, 'volume')])
        volume += self.target_volume

        if (time < T.Primary()) or (upto and (time == T.Primary())):
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

    def _extract(self, ingredients):
        """Helper function for extracts.

        Parameters
        ----------
        ingredients : Ingredients
          Ingredients to consider.

        """
        from . import timing as T

        extract = [f.extract(self['efficiency']) for f in ingredients]
        return extract

    def extract(self, time, upto=False):
        """Extract at time.

        Parameters
        ----------
        time : Timing
          Include all additions up to and at `time`.
        upto : bool, optional
          Include all additions up to `time`, but not at `time`.

        """

        from . import timing as T

        if upto:
            ingredients = self.ingredients.fermentables.upto(time)
        else:
            ingredients = self.ingredients.fermentables.at(time)

        return self._extract(ingredients)

    def grain_extract(self):
        """Extract from grains."""
        return self._extract(self.ingredients.grains)

    def unfermentable_extract(self):
        """Extract from unfermentables."""
        return self._extract(self.ingredients.unfermentables)

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

    def mash(self):
        """Mash and lauter grains to make wort.

        Returns
        -------
        wort : Wort
          The pre-boil wort.

        """

        from . import timing as T
        from .table import Table
        from .ingredients import Ingredients, Fermentable, Unfermentable
        from . import _default_format

        # all ingredients with extract, and just the mashed ones
        ingredients = self.ingredients.filter(Fermentable, Unfermentable)
        mashed = ingredients.filter(T.Mash, T.Vorlauf, T.Sparge, T.Lauter)

        total_weight = sum([f.weight for f in ingredients])
        # for water to grist ratio
        grain_weight = sum([f.weight for f in mashed.grains])

        v_kettle = self.volume(T.Lauter())
        extract = self._extract(ingredients)
        mash_extract = sum(self._extract(mashed))
        total_extract = sum(extract)

        preboil_sg = 1 + mash_extract / v_kettle / 1000
        wort = Wort(preboil_sg, v_kettle)

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
                           'Extract Fraction'),
                    caption='Mash',
                    format=_default_format)
        tab.colformats = ('{}', '{}', '{:.3f}', '{:.1%}', '{:d}', '{:.1f}',
                          '{:.1%}')
        tab.footer = '''Kettle volume: {:.1f} gal
Efficiency: {:.0%}
Pre-boil specific gravity: {:.3f}
'''.format(v_kettle, self['efficiency'], preboil_sg)

        if _default_format == 'yaml':
            print('    mash-and-lauter:')
        print(tab)

        # Infusion schedule table
        tab = Table(data=(self.T_mash, T_infusion, v_infusion),
                    names=('T mash (F)', 'T water (F)', 'Volume (gal)'),
                    caption='Lauter and sparge',
                    format=_default_format)
        tab.colformats = ('{:.0f}', '{:.0f}', '{:.2f}')
        tab.footer = '''Total mash water: {:.1f} gal ({:.1f} qt/lb)
Sparge with {:.1f} gal of water
Collect {:.1f} gal of wort
'''.format(v_mash, v_mash * 4 / grain_weight, v_sparge, v_kettle)

        print(tab)

        return wort

    def boil(self, wort=None):
        """Boil the wort.

        Uses gravity at start of boil.  John Palmer's How to Brew
        suggests this is OK.

        Parameters
        ----------
        wort : Wort, optional
          Boil this wort, else use `mash`.

        Returns
        -------
        boiled_wort : Wort
          Includes bittereness after all α-acid conversions, IBU.

        """

        from . import timing as T
        from .table import Table
        from . import _default_format

        if wort is None:
            wort = self.mash()

        v_preboil = wort.volume
        v_postboil = self.volume(T.Primary(), upto=True)

        sg_preboil = wort.gravity

        ex_postboil = sum(self.extract(T.Primary(), upto=True))
        sg_postboil = 1 + ex_postboil / v_postboil / 1000

        util = []
        bit = []
        hops = self.ingredients.hops
        for hop in hops:
            r = hop.bitterness(sg_preboil, v_postboil,
                               boil=self['boil_time'],
                               hop_stand=self.hop_stand)
            util.append(r[0])
            bit.append(r[1])

        # Bitterness table
        tab = Table(
            data=([hop.name for hop in hops],
                  [('Whole leaf' if hop.whole else 'Pellets') for hop in hops],
                  [hop.alpha for hop in hops],
                  [hop.weight for hop in hops],
                  [str(hop.timing) for hop in hops],
                  util,
                  bit),
            names=('Hop', 'Type', 'Alpha', 'Weight', 'Time', 'Utilization',
                   'Bitterness'),
            caption='Hops',
            format=_default_format)
        tab.colformats = ('{}', '{}', '{:.1f}', '{:.1f}', '{}', '{:.1f}',
                          '{:.0f}')
        tab.footer = '''Pre-boil: {} gal at {:.3f}
Post-boil: {} gal at {:.3f}, {:.0f} IBU
'''.format(v_preboil, sg_preboil, v_postboil, sg_postboil, sum(bit))
        if self.hop_stand:
            tab.footer += '\nHop stand'

        if _default_format == 'yaml':
            print('    hopping:')
        print(tab)

        return Wort(sg_postboil, v_postboil, sum(bit))

    def ferment(self, wort=None, grain_attenuation=None):
        """Ferment wort.

        Parameters
        ----------
        wort : Wort, optional
          Ferment this wort, else use `boil`.
        grain_attenuation : float, optional
          Force fermentation to match this apparent attenuation for grains.

        Returns
        -------
        beer : Beer
          Beer.

        """

        from collections import Iterable
        from . import timing as T
        from .util import final_gravity

        if wort is None:
            wort = self.boil()

        v_primary = wort.volume - self['kettle_gap']
        v_final = self.volume(T.Final())
        bit = wort.bitterness * v_primary / v_final

        ex_preferm = sum(self.extract(T.Primary(), upto=True))
        ex_final = sum(self.extract(T.Final()))
        ex_ferm = ex_final - ex_preferm
        ex_wort = v_primary * (wort.gravity - 1) * 1000
        ex = ex_wort + ex_ferm

        sg = 1 + ex / v_final / 1000

        grain_sg = 1 + (sg - 1) * sum(self.grain_extract()) / ex_final
        unfermentable_sg = 1 + (sg - 1) * \
            sum(self.unfermentable_extract()) / ex_final

        # if a mixed fermentation, use the highest attenuation
        beer = []
        for culture in self.ingredients.cultures:
            if grain_attenuation is None:
                fg = final_gravity(grain_sg, self['T_sacc'], culture)
            else:
                # use 152 to avoid a mash temperature correction
                fg = final_gravity(grain_sg, 152, ('', grain_attenuation))

            fg += unfermentable_sg - 1
            beer.append(Beer(sg, fg, bit))

        a = [b.app_attenuation for b in beer]
        i = a.index(max(a))
        beer = beer[i]

        print('''Starting gravity: {sg:.3f}
Final gravity: {fg:.3f}
Bitterness: {bit:.0f} IBU
Apparent attenutation: {aa:.0f}%
ABV: {abv:.1f}%
Calories: {cals:.0f}
Carbohydrates: {carbs:.1f} g
'''.format(sg=beer.sg, fg=beer.fg, bit=bit, aa=beer.app_attenuation,
           abv=beer.abv, cals=beer.calories, carbs=beer.carbohydrates))

        return beer


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

    @property
    def brix(self):
        from .util import sg2brix
        return sg2brix(self.gravity)

    @property
    def plato(self):
        from .util import sg2plato
        return sg2plato(self.gravity)


class Beer:
    """The final product.

    Parameters
    ----------
    sg : float
      Starting gravity.
    fg : float
      Final gravity.
    bitterness : float
      Beer bitterness in IBU.

    """

    def __init__(self, sg, fg, bitterness):
        assert isinstance(sg, float)
        assert isinstance(fg, float)
        assert isinstance(bitterness, (float, int))

        self.sg = sg
        self.fg = fg
        self.bitterness = int(bitterness)

    @property
    def abv(self):
        from .util import abv
        return abv(self.sg, self.fg)

    @property
    def app_attenuation(self):
        return 100 * (self.sg - self.fg) / (self.sg - 1)

    @property
    def calories(self):
        from .util import calories
        return calories(self.sg, self.fg)

    @property
    def carbohydrates(self):
        from .util import carbohydrates
        return carbohydrates(self.sg, self.fg)
