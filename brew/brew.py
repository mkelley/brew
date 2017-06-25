# Licensed under an MIT style license - see LICENSE

"""
brew --- Homebrew recipe calculator.
====================================

"""

from collections.abc import MutableSequence
from . import timing as T

__all__ = [
    'Ingredient',
    'Fermentable',
    'Unfermentable',
    'Hop',
    'Spice',
    'Fruit',
    'Other',
    'Priming',
    'Water',
    'Wort',
    'Culture',
    'Beer',
    'Brew',
    'set_format'
]

_default_format = 'text'  # default format for summaries

def set_format(format):
    """Set the default format for summary output.

    Parameters
    ----------
    format : string
      'text', 'html', 'notebook'

    """
    global _default_format
    assert format in ['text', 'html', 'notebook']
    _default_format = format

def execute_brew_log(filename):
    import textwrap
    import lxml.etree as ET

    ns = {'brew': 'http://www.marthaandmike.name/brewlog'}
    tree = ET.parse(filename)
    c = tree.find('//brew:workbook/brew:python', namespaces=ns).text.strip()
    c = textwrap.dedent(c)
    exec(c)
    
class Ingredient:
    """Wort ingredient.

    Parameters
    ----------
    name : string
      The name of the ingredient.
    quantity : string
      The amount of the ingredient as a string.
    timing : Timing, optional
      When to add it.
    desc : string, optional
      A long-form description of the ingredient.

    """
    
    def __init__(self, name, quantity, timing=T.Unspecified(), desc=None):
        assert isinstance(name, str)
        assert isinstance(quantity, str)
        self.name = name
        self.quantity = quantity
        self.timing = timing
        self.desc = name if desc is None else desc
        
    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, str(self))

    def __str__(self):
        return "{}, {} at {}".format(self.name, self.quantity, self.timing)

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
      if `ppg` is a float.
    desc : string, optional
      A long-form description.

    """

    def __init__(self, ppg, weight, timing=T.Mash(), name=None, desc=None):
        from . import mash

        assert isinstance(ppg, (mash.PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(name, (str, type(None)))
        assert isinstance(desc, (str, type(None)))

        if isinstance(ppg, mash.PPG):
            self.name, self.ppg, self.fermentable100 = ppg.value
            if name is not None:
                self.name = name
        else:
            ppg = float(ppg)
            assert name is not None, '`name` is required when `ppg` is a float.'
            self.name = name

        self.weight = float(weight)
        self.timing = timing
        self.desc = name if desc is None else desc

    def __str__(self):
        return "{} ({:d} PPG), {} at {}".format(
            self.name, self.ppg, self.quantity, self.timing)

    @property
    def quantity(self):
        if "{:.2f}".format(self.weight) == '1.00':
            return '1.00 lb'
        else:
            return "{:.2f} lbs".format(self.weight)
    
    def extract(self, mash_efficiency):
        """Amount of extract per gallon."""
        ex = self.weight * self.ppg
        if isinstance(self.timing, (T.Mash, T.Vorlauf)):
            ex *= mash_efficiency
        return ex

class Unfermentable(Ingredient):
    """Affects gravity, but does not ferment out.

    Parameters
    ----------
    ppg : mash.PPG or float
      The item being added, or the number of gravity points added
      per pound per gallon (requires `name`).
    weight : float
      The weight in pounds.
    timing : Timing, optional
      The timing of the addition.
    name : string, optional
      Use this name instead of the name in the `PPG` object.  Required
      if `ppg` is a float.
    desc : string, optional
      A long-form description.

    """

    def __init__(self, ppg, weight, timing=T.Mash(), name=None, desc=None):
        from . import mash

        assert isinstance(ppg, (mash.PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(name, (str, type(None)))
        assert isinstance(desc, (str, type(None)))

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
        self.desc = name if desc is None else desc

    def __str__(self):
        return "{} ({:d} PPG), {} at {}".format(
            self.name, self.ppg, self.quantity, self.timing)

    @property
    def quantity(self):
        if "{:.2f}".format(self.weight) == '1.00':
            return '1.00 lb'
        else:
            return "{:.2f} lbs".format(self.weight)
    
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
    desc : string, optional
      A long-form description.

    """

    def __init__(self, name, alpha, weight, timing=None, whole=False,
                 desc=None):
        assert isinstance(name, str)
        assert isinstance(alpha, (float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(whole, bool)
        assert isinstance(desc, (str, type(None)))

        self.name = name
        self.alpha = alpha
        self.weight = weight
        self.timing = timing
        self.whole = whole
        self.desc = name if desc is None else desc

    def __repr__(self):
        return '<Hop: {}>'.format(str(self))

    def __str__(self):
        return '{} ({}% α), {} at {}'.format(
            self.name, self.alpha, self.quantity, self.timing)

    @property
    def quantity(self):
        return "{:.2f} oz".format(self.weight)
    
    def bitterness(self, gravity, volume, boil=None, hop_stand=False):
        """Compute bitterness.

        John Palmer's How to Brew suggests initial gravity is OK.

        Parameters
        ----------
        gravity : float
          The gravity of the boil at the start.
        volume : float
          The post-boil volume in gallons.
        boil : float, optional
          The length of the boil.  Required for mash and first wort
          hops.
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

class Fruit(Fermentable):
    """Fermentable fruit forms.

    Adds volume to the wort.  If this is the wrong behavior (e.g., a
    dried fruit like raisins), set the density to 0?
    
    Parameters
    ----------
    name : string
      The name.
    sg : float
      Specific gravity of the fruit.
    weight : float
      Weight in pounds.
    timing : Timing, optional
      The timing of the addition.
    density : float, optional
      Density of the fruit, pounds per pint.
    desc : string, optional
      A long-form description.

    """

    def __init__(self, name, sg, weight, timing=T.Secondary(),
                 density=1.0, desc=None):
        assert isinstance(name, str)
        assert isinstance(sg, float)
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(density, (float, int))
        assert isinstance(desc, (str, type(None)))

        self.name = name
        self.sg = float(sg)
        self.weight = float(weight)
        self.timing = timing
        self.fermentable100 = False
        self.density = float(density)
        self.desc = name if desc is None else desc

    @property
    def ppg(self):
        """1 pound of fruit diluted in 1 gallon of water."""
        fruit_vol = 1 / self.density / 8  # gal
        fruit_ex = (self.sg - 1) * 1000 * fruit_vol
        water_vol = 1.0  # gal
        ppg = fruit_ex / (fruit_vol + water_vol)

        # but PPG should be an integer, take care with rounding to keep accuracy
        n, d = ppg.as_integer_ratio()
        if d == 2:
            ppg = (n + 1) // 2
        else:
            ppg = round(ppg)

        return ppg

    @property
    def volume(self):
        return self.weight / self.density / 8

class Other(Ingredient):
    pass

class Priming(Ingredient):
    pass

class Water(Ingredient):
    """Water.

    Parameters
    ----------
    name : string
      The name (brief description) of the water.
    volume : float
      The volume in gallons.
    timing : Timing
      The time of addition.
    desc : string, optional
      A long-form description.

    """
    
    def __init__(self, name, volume, timing, desc=None):
        assert isinstance(name, str)
        assert isinstance(volume, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(desc, (str, type(None)))

        self.name = name
        self.volume = float(volume)
        self.timing = timing
        self.desc = name if desc is None else desc

    @property
    def quantity(self):
        if self.volume == 0:
            return ""
        else:
            return "{:.2f} gal".format(self.volume)

class Wort(MutableSequence):
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
      The target wort volume in the primary, before any `Primary`
      additions, gallons.
    T_sacc : int or array-like, optional
      The saccharification temperature step(s).

    """

    def __init__(self, a=[], efficiency=0.75, boil_time=60, volume=5.5,
                 T_sacc=152):
        from collections import Iterable

        assert isinstance(a, Iterable)
        assert isinstance(efficiency, float)
        assert isinstance(boil_time, (float, int))
        assert isinstance(volume, (float, int))
        assert isinstance(T_sacc, (int, float, Iterable))

        self._list = list(a)
        self.efficiency = efficiency
        self.boil_time = float(boil_time)
        self._volume = float(volume)
        self.T_sacc = tuple(T_sacc) if isinstance(T_sacc, Iterable) else (T_sacc,)

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
        MutableSequence.__setitem__(self, index, value)

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
    def unfermentables(self):
        return list(filter(lambda v: isinstance(v, Unfermentable), self))
    
    @property
    def fruits(self):
        return list(filter(lambda v: isinstance(v, Fruit), self))
    
    @property
    def hops(self):
        return list(filter(lambda v: isinstance(v, Hop), self))

    @property
    def hop_stand(self):
        return any([isinstance(hop.timing, T.HopStand) for hop in self.hops])

    def volume(self, time=T.Final()):
        """Total volume.

        Considers wort volume in the primary and any additions
        thereafter.

        Parameters
        ----------
        time : Timing, optional
          Volume at this time.  Times before `Timing.Primary` exclude
          primary additions, but do not account for any losses in the
          brew-day process, e.g., the kettle volume gap.

        Returns
        -------
        v : float
          Volume in gallons.

        """

        v = self._volume
        v += sum([x.volume for x in self
                  if hasattr(x, 'volume') and x.timing <= time])
        return v
    
    def gravity(self, time=T.Final(), volume=None, fermentable100=True):
        """Estimate specific gravity.

        Parameters
        ----------
        time : Timing, optional
          The epoch at which the gravity should be estimated.  This
          parameter determines volume and which `Fermantable`s are
          included.
        volume : float, optional
          Use this volume instead of `volume(time)`.
        fermentable100 : bool, optional
          Set to `False` to exclude 100% fermentables.

        Returns
        -------
        sg : float
          Specific gravity of the wort.

        """

        from . import mash

        volume = self.volume(time=time) if volume is None else volume

        if fermentable100:
            fermentables = list(filter(lambda f: f.timing <= time,
                                       self.fermentables))
        else:
            fermentables = list(filter(
                lambda f: f.timing <= time and not f.fermentable100,
                self.fermentables))
            
        unfermentables = list(filter(lambda f: f.timing <= time,
                                     self.unfermentables))
        
        total_weight = sum([f.weight for f in fermentables])
        total_weight += sum([f.weight for f in unfermentables])
        extract = [f.extract(self.efficiency) for f in fermentables]
        extract += [f.extract(self.efficiency) for f in unfermentables]
        total_extract = sum(extract)

        return total_extract / volume / 1000 + 1
    
    def summary(self, **kwargs):
        """Summarize ingredients and mash extract.

        Parameters
        ----------
        format : string, optional
          Output format: 'text', 'html', 'notebook'.
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        self.summarize_ingredients(**kwargs)
        self.summarize_extract(**kwargs)

    def summarize_extract(self, **kwargs):
        """Summarize mash extract.

        Parameters
        ----------
        format : string, optional
          Output format: 'text', 'html', 'notebook'.
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        from .util import rows2tab

        kwargs['format'] = kwargs.get('format', _default_format)
        
        total_weight = sum([f.weight for f in self.fermentables])
        total_weight += sum([f.weight for f in self.unfermentables])
        extract = [f.extract(self.efficiency) for f in self.fermentables]
        extract += [f.extract(self.efficiency) for f in self.unfermentables]
        total_extract = sum(extract)
        sg = total_extract / self.volume() / 1000 + 1
        rows = []
        for x in self.fermentables + self.unfermentables:
            if x in self.mash + self.vorlauf:
                efficiency = self.efficiency
            else:
                efficiency = 1.0

            ex = x.extract(efficiency)
            rows.append([x.name, x.timing.name, x.weight,
                         x.weight / total_weight, x.ppg, ex,
                         ex / total_extract])

        colnames = ['Grain/Adjunct', 'Timing', 'Weight', 'Weight Fraction',
                    'PPG', 'Extract', 'Extract Fraction']
        colformats = ['{}', '{}', '{:.3f}', '{:.1%}', '{:d}', '{:.1f}',
                      '{:.1%}']
        footer = ['Volume: {:.1f} gal'.format(self.volume()),
                  'Efficiency: {:.0%}'.format(self.efficiency),
                  'Specific gravity: {:.3f}'.format(sg)]

        extracts = rows2tab(rows, colnames, ',\n'.join(footer),
                            colformats=colformats, verbose=True, **kwargs)

    def summarize_ingredients(self, **kwargs):
        """Summarize ingredients.

        Parameters
        ----------
        format : string, optional
          Output format: 'text', 'html', 'notebook'.
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        from .util import rows2tab
        
        kwargs['format'] = kwargs.get('format', _default_format)

        rows = []
        for f in self:
            t = '' if isinstance(f.timing, T.Unspecified) else str(f.timing)
            rows.append([str(f.quantity), str(f.name), t])

        colnames = ['Quantity', 'Item', 'Timing']
        ingredients = rows2tab(rows, colnames, verbose=True, **kwargs)

class Culture:
    """Yeast or other cultures, ready for fermentation.

    Parameters
    ----------
    cultures : CultureBank
      The type of culture(s) to propagate.
    quantity : string, optional
      The quantity of the culture.
    timing : Timing, optional
      The timing of the addition.
    desc : string, optional
      A long-form description.
    
    """

    def __init__(self, culture, quantity='1', timing=T.Primary(), desc=None):
        from .fermentation import CultureBank
        assert culture in CultureBank
        assert isinstance(quantity, str)
        assert isinstance(timing, T.Timing)
        assert isinstance(desc, (str, type(None)))
        self.culture = culture
        self.quantity = quantity
        self.timing = timing
        self.name = self.culture.value[0]
        self.desc = self.name if desc is None else desc

    def ferment(self, wort, bitterness=None, attenuation=None):
        """Ferment some wort.

        Parameters
        ----------
        wort : Wort
          The wort to ferment.
        bitterness : float, optional
          Beer bitterness in IBU.
        attenuation : float, optional
          Use this apparent attentuation percentage.

        """
        
        from . import fermentation
        from . import timing as T

        assert isinstance(wort, Wort)
        
        if bitterness is not None:
            assert isinstance(bitterness, (float, int))
            bitterness = int(bitterness)

        sg = wort.gravity()
        grain_sg = wort.gravity(fermentable100=False)
        fg = grain_sg
        if attenuation is None:
            fg = fermentation.final_gravity(grain_sg, wort.T_sacc, self.culture)
        else:
            fg = fermentation.final_gravity(grain_sg, 152, ('', attenuation))

        if len(wort.unfermentables) > 0:
            w = Wort([x for x in wort if isinstance(x, Unfermentable)])
            fg += w.gravity() - 1

        return Beer(sg, fg, bitterness=bitterness)

class Beer:
    """The final product.

    Parameters
    ----------
    sg : float
      Starting gravity.
    fg : float
      Final gravity.
    bitterness : float, optional
      Beer bitterness in IBU.

    """

    def __init__(self, sg, fg, bitterness=None):
        assert isinstance(sg, float)
        assert isinstance(fg, float)

        if bitterness is not None:
            assert isinstance(bitterness, (float, int))
            bitterness = int(bitterness)

        self.sg = sg
        self.fg = fg
        self.bitterness = bitterness

    @property
    def abv(self):
        from . import fermentation
        return fermentation.abv(self.sg, self.fg)

    @property
    def app_attenuation(self):
        return 100 * (self.sg - self.fg) / (self.sg - 1)

    @property
    def calories(self):
        from . import fermentation
        return fermentation.calories(self.sg, self.fg)

    @property
    def carbohydrates(self):
        from . import fermentation
        return fermentation.carbohydrates(self.sg, self.fg)

    def summary(self):
        """Print a summary of the beer."""

        print('''
Starting gravity: {:.3f}
Final gravity: {:.3f}'''.format(self.sg, self.fg))

        if self.bitterness is not None:
            print('Bitterness: {:d} IBU'.format(self.bitterness))

        print('''Apparent attenutation: {:.0f}%
ABV: {:.1f}%
Calories: {:.0f}
Carbohydrates: {:.1f} g
'''.format(self.app_attenuation, self.abv, self.calories, self.carbohydrates))

class Brew:
    """Homebrew recipe calculator.

    Parameters
    ----------
    wort : Wort
      The wort to brew.
    culture : Culture
      The fermentation culture.
    r_mash : float, optional
      Ratio of water volume to grain weight. [qt/lb]
    T_rest : int or array-like, optional
      Initial (pre-saccharification) rest temperature(s).
    mash_out : bool, optional
      Set to `True` to add a mash-out step, targeting 170 F.
    r_boil : float, optional
      Boil-off rate, gal/hr.
    mlt_gap : float, optional
      Leftover volume in MLT after lauter, gal.
    kettle_gap : float, optional
      Leftover volume in kettle after racking, gal.
    T_water : int, optional
      Water temperature for step infusions.
    T_grain : int, optional
      Grain temperature.

    """

    def __init__(self, wort, culture, r_mash=1.4, T_rest=[],
                 mash_out=True, r_boil=1.0, mlt_gap=0.25, kettle_gap=0.5,
                 T_water=200, T_grain=65):
        from collections import Iterable

        assert isinstance(wort, Wort)
        assert isinstance(culture, (Culture, Iterable))
        assert isinstance(r_mash, (float, int))
        assert isinstance(T_rest, (int, float, Iterable))
        assert isinstance(mash_out, bool)
        assert isinstance(r_boil, (float, int))
        assert isinstance(mlt_gap, (float, int))
        assert isinstance(kettle_gap, (float, int))
        assert isinstance(T_water, (int, float))
        assert isinstance(T_grain, (int, float))
        
        self.wort = wort
        if isinstance(culture, Iterable):
            self.culture = list(culture)
        else:
            self.culture = [culture]
        self.r_mash = float(r_mash)
        self.T_rest = tuple(T_rest) if isinstance(T_rest, Iterable) else (T_rest)
        self.mash_out = mash_out
        self.r_boil = float(r_boil)
        self.mlt_gap = float(mlt_gap)
        self.kettle_gap = float(kettle_gap)
        self.T_water = int(T_water)
        self.T_grain = int(T_grain)

    def __repr__(self):
        return self.brew()

    @property
    def T_mash(self):
        T = self.T_rest + self.wort.T_sacc
        if self.mash_out:
            T += (170,)
        return T

    @property
    def boil_gravity(self):
        """At the start of the boil."""
        v = self.wort.gravity(time=T.Boil(self.wort.boil_time),
                              volume=self.boil_volume)
        return v

    @property
    def boil_volume(self):
        """At the start of the boil."""
        v = (self.wort.volume(T.Boil(0))
             + self.wort.boil_time / 60 * self.r_boil
             + self.kettle_gap)
        return v

    @property
    def post_boil_gravity(self):
        """At the end of the boil."""
        return self.wort.gravity(time=T.Boil(0))

    def brew(self, attenuation=None):
        """Brew the beer.

        Parameters
        ----------
        attenuation : float, optional
          Use this attenutation percentage for the yeast.

        Returns
        -------
        beer : Beer
          The final product.

        """
        
        from collections import Iterable
        
        # if a mixed fermentation, report the beer with the greatest attenuation
        if isinstance(self.culture, Iterable):
            beer = []
            for culture in self.culture:
                beer.append(culture.ferment(self.wort, attenuation=attenuation))

            a = [b.app_attenuation for b in beer]
            i = a.index(max(a))
            return beer[i]
        else:
            return self.culture.ferment(self.wort, attenuation=attenuation)

    def bitterness(self):
        """Beer bitterness.

        Returns
        -------
        bit : float
          The computed bitterness in IBUs.

        """

        bitterness = 0
        for hop in self.wort.hops:
            bitterness += hop.bitterness(self.boil_gravity,
                                         self.post_boil_volume,
                                         boil=self.wort.boil_time,
                                         hop_stand=self.wort.hop_stand)
        return bitterness

    def infusion(self):
        """Water temperature and volume schedule for infusion mashing.

        Returns
        -------
        T_infusion : tuple
          Temperature of each infusion, Fahrenheit.
        v_infusion : tuple
          Volume of each infusion, gallons.
        v_sparge : float
          Volume of sparge water, gallons.

        """

        from .util import rows2tab
        from . import mash

        grain_weight = sum([g.weight for g in self.wort.mash if hasattr(g, 'weight')])

        v_infusion = []
        T_infusion = []
        for i in range(len(self.T_mash)):
            if i == 0:
                v_infusion.append(self.r_mash * grain_weight / 4)
                T = mash.strike_water(self.r_mash, self.T_grain, self.T_mash[0])
                T_infusion.append(T)
            else:
                v = mash.infusion_volume(
                    sum(v_infusion) * 4, grain_weight,
                    self.T_mash[i-1], self.T_mash[i])
                v_infusion.append(v / 4)
                T_infusion.append(self.T_water)

        v_mash = sum(v_infusion)
        v_sparge = self.boil_volume - v_mash + self.mlt_gap + 0.125 * grain_weight

        return T_infusion, v_infusion, v_sparge

    def summary(self, **kwargs):
        """Summarize ingredients, wort, infusion, and bitterness."""
        self.summarize_ingredients(**kwargs)
        self.wort.summarize_extract(**kwargs)
        self.summarize_infusion(**kwargs)
        self.summarize_bitterness(**kwargs)

    def summarize_bitterness(self, **kwargs):
        """Summarize beer bitterness.

        Parameters
        ----------
        format : string, optional
          Output format: 'text', 'html', 'notebook'.
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        from operator import itemgetter
        from .util import rows2tab

        kwargs['format'] = kwargs.get('format', _default_format)
        
        tab = []
        for hop in self.wort.hops:
            util, bit = hop.bitterness(self.boil_gravity,
                                       self.boil_volume,
                                       boil=self.wort.boil_time,
                                       hop_stand=self.wort.hop_stand)
            
            tab.append([hop.name, 'Whole leaf' if hop.whole else 'Pellets',
                        hop.alpha, hop.weight, hop.timing.time, util, bit])

        tab.sort(key=itemgetter(0))
        tab.sort(key=itemgetter(3), reverse=True)
        util = [row[-2] for row in tab]
        bit = [row[-1] for row in tab]

        v = self.wort.volume(T.Boil(0))
        v_final = self.wort.volume()
        bit_final = sum(bit) * v / v_final

        colnames = ['Hop', 'Type', 'Alpha', 'Weight', 'Time', 'Utilization',
                    'Bitterness']
        colformats = ['{}', '{}', '{:.1f}', '{:.1f}', '{:.0f}', '{:.1f}',
                      '{:.0f}']

        footer = ['Boil specific gravity: {:.3f}'.format(self.boil_gravity),
                  'Boil volume: {} gal'.format(self.boil_volume),
                  'Post-boil specific gravity: {:.3f}'.format(self.post_boil_gravity)]
        if self.wort.hop_stand:
            footer += ['Hop stand']
        footer += ['Post-boil bitterness: {:.0f} IBU'.format(sum(bit))]
        footer += ['Final bitterness: {:.0f} IBU'.format(bit_final)]

        tab = rows2tab(tab, colnames, ',\n'.join(footer),
                       colformats=colformats, verbose=True, **kwargs)

    def summarize_infusion(self, **kwargs):
        """Water temperature and volume schedule for infusion mashing.

        Parameters
        ----------
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        from .util import rows2tab
        
        kwargs['format'] = kwargs.get('format', _default_format)

        grain_weight = sum([g.weight for g in self.wort.mash if hasattr(g, 'weight')])
        if grain_weight == 0:
            return

        T_infusion, v_infusion, v_sparge = self.infusion()
        
        tab = []
        for i in range(len(self.T_mash)):
            tab.append([self.T_mash[i], T_infusion[i], v_infusion[i]])

        v_mash = sum(v_infusion)
        #v_wort = v_mash + v_sparge - 0.125 * grain_weight - self.mlt_gap

        footer = '''Total mash water: {:.1f} gal ({:.1f} qt/lb),
Sparge with {:.1f} gal of water
Collect {:.1f} gal of wort
'''.format(v_mash, v_mash * 4 / grain_weight, v_sparge, self.boil_volume)

        columns = ['T mash (F)', 'T water (F)', 'Volume (gal)']
        colformats = ['{:.0f}', '{:.0f}', '{:.2f}']

        tab = rows2tab(tab, columns, footer, colformats=colformats,
                       verbose=True, **kwargs)

    def summarize_ingredients(self, **kwargs):
        """Summarize ingredients.

        Parameters
        ----------
        format : string, optional
          Output format: 'text', 'html', 'notebook'.
        **kwargs
          Keyword arguments for `rows2tab`.

        """

        from .util import rows2tab
        
        kwargs['format'] = kwargs.get('format', _default_format)

        rows = []
        for i in list(self.wort) + self.culture:
            t = '' if isinstance(i.timing, T.Unspecified) else str(i.timing)
            if _default_format == 'html':
                item = i.desc
            else:
                item = i.name

            rows.append([str(i.quantity), item, t])

        colnames = ['Quantity', 'Item', 'Timing']
        ingredients = rows2tab(rows, colnames, verbose=True, **kwargs)
