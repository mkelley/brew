# Licensed under an MIT style license - see LICENSE

"""
brew --- Homebrew recipe calculator.
====================================

"""

import collections
from enum import Enum

class Timing(Enum):
    mash = 1
    vorlauf = 2
    first_wort = 3
    boil = 4
    whirlpool = 5
    primary = 6
    secondary = 7
    other = 8
    final = 9

class Fermentable(object):
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

    Notes
    -----
    Use `Timing.other` and the `Fermentable` will not contribute to
    the specific gravity.

    """

    def __init__(self, ppg, weight, timing=Timing.mash, name=None):
        from . import mash

        assert isinstance(ppg, (mash.PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, Timing)
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
        return "{}, {:.2f} lbs".format(self.name, self.ppg, self.weight)
        
    def extract(self, mash_efficiency):
        """Amount of extract per gallon."""
        ex = self.weight * self.ppg
        if self.timing in (Timing.mash, Timing.vorlauf):
            ex *= mash_efficiency
        return ex

class Wort(collections.abc.MutableSequence):
    """Make some wort."""
    def __init__(self, a=None):
        self._list = []
        if a is not None:
            for v in a:
                self.append(v)

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
        s = "Wort:\n  "
        s += "\n  ".join([str(f) for f in self])
        return s
    
    def __reversed__(self, *args, **kwargs):
        return reversed(self._list)
        
    def __setitem__(self, index, value):
        assert isinstance(value, Fermentable)
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
        return list(filter(lambda v: v.timing.value == Timing.mash.value, self))
        
    @property
    def vorlauf(self):
        return list(filter(lambda v: v.timing.value == Timing.vorlauf.value, self))
        
    @property
    def first_wort(self):
        return list(filter(lambda v: v.timing.value == Timing.first_wort.value, self))
        
    @property
    def boil(self):
        return list(filter(lambda v: v.timing.value == Timing.boil.value, self))
    
    @property
    def whirlpool(self):
        return list(filter(lambda v: v.timing.value == Timing.whirlpool.value, self))

    @property
    def primary(self):
        return list(filter(lambda v: v.timing.value == Timing.primary.value, self))
        
    @property
    def secondary(self):
        return list(filter(lambda v: v.timing.value == Timing.secondary.value, self))
        
    @property
    def other(self):
        return list(filter(lambda v: v.timing.value == Timing.other.value, self))

    @property
    def fermentables(self):
        return list(filter(lambda v: isinstance(v, Fermentable), self))
    
    def gravity(self, volume, efficiency, time=Timing.final,
                verbose=True, **kwargs):
        """Estimate specific gravity.

        Parameters
        ----------
        volume : float
          The volume of the wort, either collected from the mash or
          post-boil.
        efficiency : float
          The efficiency of the mash and lauter, from 0 to 1.0.
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
        table : string
          Table of the grist and extract.

        """
        from . import mash
        from .util import tab2txt

        total_weight = sum([f.weight for f in self.fermentables])
        total_extract = sum([f.extract(efficiency) for f in self.fermentables])
        
        tab = []
        for f in self.mash + self.vorlauf:
            ex = f.extract(efficiency)
            tab.append([f.name, f.timing.name, f.weight,
                        f.weight / total_weight, f.ppg, ex, ex / total_extract])

        colnames = ['Grain/Adjunct', 'Timing', 'Weight', 'Weight Fraction',
                    'PPG', 'Extract', 'Extract Fraction']
        colformats = ['{}', '{}', '{:.3f}', '{:.1%}', '{:d}', '{:.1f}',
                      '{:.1%}']
        sg = sum([row[-2] for row in tab]) / volume / 1000 + 1
        footer = '''Volume: {:.1f} gal,
Efficiency: {:.0%},
Specific gravity: {:.3f}
'''.format(volume, efficiency, sg)

        if verbose:
            print(tab2txt(tab, colnames, footer, colformats=colformats,
                          **kwargs))

        return sg

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
