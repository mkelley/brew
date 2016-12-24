# Licensed under an MIT style license - see LICENSE

"""
brew --- Homebrew recipe calculator.
====================================

"""

import collections
from . import timing as T

class Ingredient(object):
    """Wort ingredient.

    Parameters
    ----------
    name : string
      The name of the ingredient.
    quantity : string
      The amount of the ingredient as a string.

    """
    
    def __init__(self, name, quanitity):
        assert isinstance(name, str)
        assert isinstance(quantity, str)
        self.name = name
        self.quantity = quantity

class Fermentable(Ingredient):
    """Grains and adjuncts.

    Parameters
    ----------
    ppg : mash.PPG or float
      The item being fermented, or the number of gravity points added
      per pound per gallon (requires `name`).
    weight : float
      The weight in pounds.
    timing : Timing, optional
      The timing of the addition.
    name : string, optional
      Use this name instead of the name in the `PPG` object.  Required
      if `pgg` is a float.

    """

    def __init__(self, ppg, weight, timing=T.Mash(), name=None):
        from . import mash

        assert isinstance(ppg, (mash.PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        if name is not None:
            assert isinstance(name, str)

        if isinstance(ppg, mash.PPG):
            self.name, self.ppg = ppg.value
            if name is not None:
                self.name = name
        else:
            ppg = float(ppg)
            assert name is not None, '`name` is required when `ppg` is a float.'
            self.name = name

        self.weight = float(weight)
        self.timing = timing

    def __repr__(self):
        return "<Fermentable: {}>".format(str(self))

    def __str__(self):
        return "{} ({:d} PPG), {:.2f} lbs, {}".format(
            self.name, self.ppg, self.weight, self.timing)

    def extract(self, mash_efficiency):
        """Amount of extract per gallon."""
        ex = self.weight * self.ppg
        if isinstance(self.timing, (T.Mash, T.Vorlauf)):
            ex *= mash_efficiency
        return ex

class Hop(Ingredient):
    """Hop addition.

    Parameters
    ----------
    name : string
      The name of the hop.
    alpha : float
      The weight percentage of alpha acids.
    weight : float
      The weight of the addition in ounces.
    timing : Timing, optional
      The timing of the addition.
    kind : bool, optional
      Set to `True` for whole leaf hops, `False` for pellets.
    
    """

    def __init__(self, name, alpha, weight, timing=None, whole=False):
        assert isinstance(name, str)
        assert isinstance(alpha, (float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(whole, bool)

        self.name = name
        self.alpha = alpha
        self.weight = weight
        self.timing = timing
        self.whole = whole

    def __repr__(self):
        return '<Hop: {}>'.format(str(self))

    def __str__(self):
        return '{} ({}% α), {:.2f} oz, {}'.format(
            self.name, self.alpha, self.weight, self.timing)

    def bitterness(self, gravity, volume, boil=None, hop_stand=False):
        """Compute bitterness contribution.

        Parameters
        ----------
        gravity : float
          The gravity of the boil.
        volume : float
          The post-boil volume in gallons.
        boil : float, optional
          The length of the boil.  Required for mash and first_wort
          hops.  Bitterness calculation uses `boil + 5`.
        hop_stand : bool, optional
          Set to `True` if there is a hop stand after the boil.  If
          so, any boil contributions within the last 5 minutes will be
          computed with an additional 5 minutes of timing.

        Returns
        -------
        util : float
          Percent utilization.
        bit : float
          Bittereness in IBUs.

        """

        from . import hops

        assert isinstance(gravity, float)
        assert isinstance(volume, (float, int))

        if isinstance(self.timing, (T.FirstWort, T.Mash)):
            assert isinstance(boil, (float, int)), 'Boil time is required for mash and first-wort hops.'
            t = boil + 5
        elif isinstance(self.timing, T.HopStand):
            t = 5
        elif isinstance(self.timing, T.Boil):
            t = self.timing.time
            t += 5 if hop_stand else 0
        else:
            return 0, 0

        util = hops.utilization(t, gravity, whole=self.whole)
        bit = hops.ibu(util, self.weight, self.alpha, volume)

        return util, bit

class Spice(Ingredient):
    pass

class Fruit(Ingredient):
    pass

class Other(Ingredient):
    pass

class Wort(collections.abc.MutableSequence):
    """Make wort with water, malt, adjuncts, hops, etc.

    Parameters
    ----------
    a : list
      A list of `Ingredient`s.
    efficiency : float, optional
      The efficiency of the mash and lauter, from 0 to 1.0.
    boil_time : float, optional
      The boil time in minutes.
    volume : float, optional
      The target wort volume in the primary, gallons.

    """

    def __init__(self, a=[], efficiency=0.75, boil_time=60, volume=5.5):
        import collections

        assert isinstance(a, collections.Iterable)
        assert isinstance(efficiency, float)
        assert isinstance(boil_time, (float, int))
        assert isinstance(volume, (float, int))

        self._list = list(a)
        self.efficiency = efficiency
        self.boil_time = float(boil_time)
        self.volume = float(volume)

    def __contains__(self, value):
        return value in self._list
        
    def __delitem__(self, k):
        del self._list[k]

    def __iadd__(self, *args, **kwargs):
        self._list.__iadd__(*args, **kwargs)
        
    def __iter__(self):
        return iter(self._list)
        
    def __getitem__(self, k):
        return self._list[k]
        
    def __len__(self, *args, **kwargs):
        return len(self._list)

    def __repr__(self):
        return "<Wort: {} ingredients ({} fermentables, {} hops)>".format(
            len(self), len(self.fermentables), len(self.hops))

    def __str__(self):
        s = "Wort:\n  "
        s += "\n  ".join(['[{}] {}'.format(i, f) for i, f in enumerate(self)])
        return s
    
    def __reversed__(self, *args, **kwargs):
        return reversed(self._list)
        
    def __setitem__(self, index, value):
        assert isinstance(value, Ingredient)
        collections.abc.MutableSequence.__setitem__(self, index, value)

    def append(self, v):
        self._list.append(v)

    def extend(self, iterable):
        self._list.extend(iterable)
        
    def count(self, *args):
        return self._list.count(*args)
        
    def index(self, *args):
        return self._list(*args)

    def insert(self, index, object):
        self._list.insert(index, object)

    def pop(self, *args):
        return self._list.pop(*args)
        
    def remove(self, v):
        self._list.remove(v)

    def reverse(self):
        self._list.reverse()

    @property
    def mash(self):
        return list(filter(lambda v: isinstance(v.timing, T.Mash), self))
        
    @property
    def vorlauf(self):
        return list(filter(lambda v: isinstance(v.timing, T.Vorlauf), self))
        
    @property
    def first_wort(self):
        return list(filter(lambda v: isinstance(v.timing, T.FirstWort), self))
        
    @property
    def boil(self):
        return list(filter(lambda v: isinstance(v.timing, T.Boil), self))
    
    @property
    def hop_stand(self):
        return list(filter(lambda v: isinstance(v.timing, T.HopStand), self))

    @property
    def primary(self):
        return list(filter(lambda v: isinstance(v.timing, T.Primary), self))
        
    @property
    def secondary(self):
        return list(filter(lambda v: isinstance(v.timing, T.Secondary), self))
        
    @property
    def packaging(self):
        return list(filter(lambda v: isinstance(v.timing, T.Packaging), self))

    @property
    def fermentables(self):
        return list(filter(lambda v: isinstance(v, Fermentable), self))
    
    @property
    def hops(self):
        return list(filter(lambda v: isinstance(v, Hop), self))

    @property
    def hop_stand(self):
        return any([isinstance(hop.timing, T.HopStand) for hop in self.hops])
    
    def gravity(self, time=T.Final, verbose=True, **kwargs):
        """Estimate specific gravity.

        Parameters
        ----------
        time : Timing
          The epoch at which the gravity should be estimated.  This
          parameter determines which `Fermantable`s are included.
        verbose : bool, optional
          If `True`, print a table of extract information.
        **kwargs
          Keyword arguments for `tab2txt`.

        Returns
        -------
        sg : float
          Specific gravity of the wort.

        """

        from . import mash
        from .util import tab2txt

        total_weight = sum([f.weight for f in self.fermentables])
        total_extract = sum([f.extract(self.efficiency)
                             for f in self.fermentables])
        
        tab = []
        for f in self.mash + self.vorlauf:
            ex = f.extract(self.efficiency)
            tab.append([f.name, f.timing.name, f.weight,
                        f.weight / total_weight, f.ppg, ex,
                        ex / total_extract])
        sg = sum([row[-2] for row in tab]) / self.volume / 1000 + 1

        if verbose:
            colnames = ['Grain/Adjunct', 'Timing', 'Weight', 'Weight Fraction',
                        'PPG', 'Extract', 'Extract Fraction']
            colformats = ['{}', '{}', '{:.3f}', '{:.1%}', '{:d}', '{:.1f}',
                          '{:.1%}']
            footer = ['Volume: {:.1f} gal'.format(self.volume),
                      'Efficiency: {:.0%}'.format(self.efficiency),
                      'Specific gravity: {:.3f}'.format(sg)]

            print(tab2txt(tab, colnames, ',\n'.join(footer),
                          colformats=colformats, **kwargs))

        return sg

    def bitterness(self, verbose=True, **kwargs):
        """Wort bitterness.

        Parameters
        ----------
        verbose : bool, optional
          Print out a table of hop contributions.
        **kwargs
          Keyword arguments for `tab2txt`.

        Returns
        -------
        bit : float
          The computed bitterness in IBUs.

        """

        from operator import itemgetter
        from .util import tab2txt

        hop_stand = self.hop_stand
        sg = self.gravity(verbose=False)

        tab = []
        for hop in self.hops:
            util, bit = hop.bitterness(sg, self.volume, boil=self.boil_time,
                                       hop_stand=hop_stand)
            tab.append([hop.name, 'Whole leaf' if hop.whole else 'Pellets',
                        hop.alpha, hop.weight, hop.timing.time, util, bit])

        tab.sort(key=itemgetter(0))
        tab.sort(key=itemgetter(3), reverse=True)
        util = [row[-2] for row in tab]
        bit = [row[-1] for row in tab]

        if verbose:
            colnames = ['Hop', 'Type', 'Alpha', 'Weight', 'Time', 'Utilization',
                        'Bitterness']
            colformats = ['{}', '{}', '{:.1f}', '{:.1f}', '{:.0f}', '{:.1f}',
                          '{:.0f}']

            footer = ['Boil specific gravity: {:.3f}'.format(sg),
                      'Volume: {} gal'.format(self.volume)]
            if hop_stand:
                footer += ['Hop stand']
            footer += ['Total bitterness: {:.0f} IBU'.format(sum(bit))]

            print(tab2txt(tab, colnames, ',\n'.join(footer),
                          colformats=colformats, **kwargs))

        return sum(bit)


class Brew(object):
    """Homebrew recipe calculator.

    Parameters
    ----------
    volume : float, optional
      Target volume in gallons.
    mash : dict, optional
      
    kettle : dict, optional
      Same as mash, but for sugars added to the kettle.  Assumes 100%
      efficiency.
    r : float, optional
      Ratio of water volume to grain weight. [qt/lb]
    T_rest : float or list, optional
       Initial (pre-saccharification) rest temperature(s).
    T_sacc : float or list, optional
      Saccharification rest temperature(s).
    hops : dict, optional

    yeast : string or tuple, optional
      

    **kwargs
      Any `wort`, `hops.schedule`, or `mash.schedule` keywords.

    """

    def __init__(self, volume=5.5, mash={'American 2-row': 10},
                 kettle={}, r=1.4, T_rest=[], T_sacc=[150, 170], t_boil=60,
                 r_boil=1.3, hops={'Cascade': (7, 1.0, 60)},
                 yeast='WLP001', **kwargs):

        self.volume = volume
        self.mash = {'American 2-row': 10} if mash is None else mash
        self.kettle = kettle

        self.r = r
        T_rest = T_rest if isinstance(T_rest, (list, tuple)) else [T_rest]
        self.T_sacc = T_sacc if isinstance(T_sacc, (list, tuple)) else [T_sacc]
        self.T_mash = []
        self.T_mash.extend(T_rest)
        self.T_mash.extend(self.T_sacc)

        self.t_boil = t_boil
        self.r_boil = r_boil

        self.hops = hops

        self.yeast = yeast

        self.kwargs = kwargs
        
        self.brew()

    def __repr__(self):
        return self.brew()

    @property
    def weight(self):
        w = 0
        if len(self.mash) == 0:
            return w

        for v in self.mash.values():
            w += v[0] if isinstance(v, (list, tuple)) else v

        return w

    @property
    def yeast(self):
        return self._yeast

    @yeast.setter
    def yeast(self, y):
        from . import fermentation
        self._yeast = fermentation.yeast(y)

    def brew(self, **kwargs):
        from . import mash
        from . import hops
        from . import fermentation

        self.kwargs.update(kwargs)

        sg, tab = mash.wort(self.mash, self.kettle, self.volume, **self.kwargs)
        outs = tab
        v_mash, T_infusions, tab = mash.infusion(
            self.r, self.weight, self.volume, self.T_mash,
            t_boil=self.t_boil, r_boil=self.r_boil,
            **self.kwargs)
        outs += tab

        # Use volume half way through boil to estimate boil specific
        # gravity
        v = self.volume + self.t_boil / 60.0 * self.r_boil / 2
        boil_sg = (sg - 1) * self.volume / v + 1

        util, bit, tab = hops.schedule(boil_sg, self.volume, self.hops,
                                       **self.kwargs)
        outs += tab

        grain_sg = mash.wort(self.mash, {}, self.volume, **self.kwargs)[0]
        fg, app_atten = fermentation.final_gravity(grain_sg, self.T_sacc[0],
                                                   self.yeast)
        cal = fermentation.calories(sg, fg)
        carbs = fermentation.carbohydrates(sg, fg)
        outs += '''
Fermentation with {}
Apparent attenutation: {:.0f}%
Final gravity: {:.3f}
ABV: {:.1f}%
Calories: {:.0f}
Carbohydrates: {:.1f} g
'''.format(self.yeast[0], app_atten, fg, fermentation.abv(sg, fg), cal, carbs)

        return outs
