# Licensed under an MIT style license - see LICENSE

"""
ingredients --- Beer ingredients
================================

"""

from enum import Enum
from collections.abc import MutableSequence
from . import timing as T

__all__ = [
    'PPG',
    'CultureBank',
    'Culture',
    'Ingredient',
    'Fermentable',
    'Unfermentable',
    'Hop',
    'Spice',
    'Fruit',
    'Other',
    'Priming',
    'Water',
    'Ingredients',
]

# Source: Home Brewer's Companion
# Beersmith: http://www.beersmith.com/Grains/Grains/GrainList.htm
# name, PPG, grain flag, 100% fermentable flag
class PPG(Enum):
    AcidMalt = "Acid malt", 27, True, False  # (Germany) Beersmith
    AmericanTwoRow = "American 2-row", 37, True, False
    AmericanSixRow = "American 6-row", 35, True, False
    AmericanPaleAle = "American pale ale", 36, True, False
    BelgianPaleAle = "Belgian pale ale", 37, True, False
    BelgianPilsener = "Belgian pilsener", 37, True, False
    DriedMaltExtract = "Dried malt extract", 44, True, False
    EnglishTwoRow = "English 2-row", 38, True, False
    EnglishMild = "English mild", 37, True, False
    MarisOtter = "Maris Otter", 38, True, False
    WheatMalt = "Wheat malt", 38, True, False  # midwest / german / belgian
    AmericanRyeMalt = "American rye malt", 36, True, False
    GermanRyeMalt = "German rye malt", 38, True, False
    GermanPilsner = "German pilsner", 37, True, False
    EnglishRyeMalt = "English rye malt", 40, True, False
    EnglishOatMalt = "English oat malt", 35, True, False
    AmericanVienna = "American Vienna", 36, True, False
    GermanVienna = "German Vienna", 37, True, False
    AmericanCarapils = "American Carapils", 34, True, False  # dextrine
    BelgianCarapils = "Belgian Carapils", 36, True, False
    AmericanMunich = "American Munich", 34, True, False
    GermanMunich = "German Munich", 37, True, False
    GermanMunichII = "Germain Munich II", 36, True, False
    BelgianMunich = "Belgian Munich", 37, True, False
    Caramunich = "Caramunich", 33, True, False  # Beersmith
    AmericanCaramel10 = "American caramel 10", 35, True, False
    AmericanCaramel20 = "American caramel 20", 35, True, False
    AmericanCaramel40 = "American caramel 40", 35, True, False
    AmericanCaramel60 = "American caramel 60", 34, True, False
    AmericanCaramel120 = "American caramel 120", 33, True, False
    EnglishCrystal20_30 = "English crystal 20-30", 36, True, False
    EnglishCrystal60_70 = "English crystal 60-70", 34, True, False
    EnglishCaramalt = "English Caramalt", 36, True, False
    BelgianCrystal = "Belgian crystal", 36, True, False
    AmericanVictory = "American Victory", 33, True, False
    BelgianBiscuit = "Belgian biscuit", 36, True, False
    BelgianAromatic = "Belgian aromatic", 36, True, False
    EnglishBrown = "English brown", 33, True, False
    EnglishAmber = "English amber", 33, True, False
    BelgianSpecialB = "Belgian Special B", 35, True, False
    AmericanChocolate = "American chocolate", 28, True, False  # Beersmith
    EnglishPaleChocolate = "English pale chocolate", 34, True, False # Beersmith
    EnglishChocolate = "English chocolate", 34, True, False  # Beersmith
    Carahell = "Carahell", 35, True, False  # guess
    Black = "Black", 25, True, False  # Beersmith
    RoastedBarley = "Roasted barley", 18, True, False
    BarleyRaw = "Barley, raw", 32, True, False  # 30 to 34
    Barleyflaked = "Barley, flaked", 32, True, False  # 30 to 34
    CornFlaked = "Corn, flaked", 39, True, False
    CornGrits = "Corn grits", 37, True, False
    MilletRaw = "Millet, raw", 37, True, False
    SorghumRaw = "Sorghum, raw", 37, True, False
    OatsRaw = "Oats, raw", 33, True, False
    OatsFlaked = "Oats, flaked", 33, True, False
    RiceRaw = "Rice, raw", 38, True, False
    RiceFlaked = "Rice, flaked", 38, True, False
    RyeRaw = "Rye, raw", 36, True, False
    RyeFlaked = "Rye, flaked", 36, True, False
    WheatFlaked = "Wheat, flaked", 33, True, False
    WheatRaw = "Wheat, raw", 37, True, False
    WheatTorrified = "Wheat, torrified", 35, True, False
    
    AgaveSyrup = "Agave syrup", 34, False, False
    BelgianCandiSugar = "Belgian candi sugar", 46, False, True
    BelgianCandiSyrup = "Belgian candi syrup", 36, False, True
    CaneSugar = "Cane sugar", 46, False, True
    TableSugar = "Table sugar", 46, False, True
    TurbinadoSugar = "Turbinado sugar", 46, False, True
    LightBrownSugar = "Light brown sugar", 46, False, True
    DarkBrownSugar = "Dark brown sugar", 46, False, True
    CornSugarDextrose = "Corn sugar (dextrose)", 46, False, True
    Lactose = "Lactose", 35, False, False
    Honey = "Honey", 32, False, True  # 30 to 35
    MapleSap = "Maple sap", 9, False, True
    MapleSyrup = "Maple syrup", 30, False, True  # variable
    Molasses = "Molasses", 36, False, True
    Rapadura = "Rapadura", 40, False, True
    RiceExtract = "Rice extract", 34, False, True
    WhiteSorghumSyrup = "White sorghum syrup", 38, False, True
    
    PumpkinPuree = "Pumpkin puree", 2, False, False

class CultureBank(Enum):
    # name, min, max apparent attenutation
    CaliforniaAle = ('WLP001, California Ale', 73, 80)
    EnglishAle = ('WLP002, English Ale', 63, 70)
    IrishAle = ('WLP004, Irish Ale', 69, 74)
    DryEnglishAle = ('WLP007, Dry English Ale', 70, 80)
    CaliforniaAleV = ('WLP051, California Ale V', 70, 75)
    FrenchAle = ('WLP072, French Ale', 68, 75)
    CreamAleBlend = ('WLP080, Cream Ale Blend', 75, 80)
    Hefeweizen = ('WLP300, Hefeweizen', 72, 76)
    BelgianWit = ('WLP400, Belgian Wit', 74, 78)
    MonasteryAle = ('WLP500, Monastery Ale', 75, 80)
    AbbeyAle = ('WLP530, Abbey Ale', 75, 80)
    BelgianAle = ('WLP550, Belgian Ale', 78, 85)
    BelgianSaisonI = ('WLP565, Belgian Saison I', 65, 75)
    BelgianSaisonII = ('WLP566, Belgian Saison II', 78, 85)
    BelgianStyleSaison = ('WLP568, Belgian Style Saison', 70, 80)
    BelgianGoldenAle = ('WLP570, Belgian Golden Ale', 73, 78)
    BelgianSaisonIII = ('WLP585, Belgian Saison III', 70, 74)
    TrappistHighGravity = ('WY3787, Trappist Style High Gravity', 74, 78)
    FrenchSaisonWhiteLabs = ('WLP590, French Saison', 73, 80)
    FrenchSaisonWyeast = ('WY3711, French Saison', 77, 83)
    SanFranciscoLager = ('WLP810, San Francisco Lager', 65, 70)
    OktoberfestLager = ('WLP820, Oktoberfest/Märzen Lager', 65, 73)
    SacchromycesBruxellensisTrois = ('WLP644, Sacchromyces bruxellensis Trois', 85, 100)
    BrettanomycesClaussenii = ('WLP645, Brettanomyces claussenii', 85, 100)
    BrettanomycesBruxellensisTroisVrai = ('WLP648, Brettanomyces bruxellensis Trois Vrai', 85, 100)
    BrettanomycesBruxellensis = ('WLP650, Brettanomyces bruxellensis', 85, 100)
    BrettanomycesLambicus = ('WLP653, Brettanomyces lambicus', 85, 100)
    SourMix1 = ('WLP655, Sour Mix 1', 85, 100)
    FlemishAleBlend = ('WLP665, Flemish Ale Blend', 80, 100)
    AmericanFarmhouseBlend = ('WLP670, American Farmhouse Blend', 75, 82)
    AmericanAle = ('US-05, American Ale', 81, 81)
    HouseSourMix = ('House sour mix', 86, 86)
    BottleDregs = ('Bottle dregs', 0, 100)

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
        assert culture in CultureBank
        assert isinstance(quantity, str)
        assert isinstance(timing, T.Timing)
        assert isinstance(desc, (str, type(None)))
        self.culture = culture
        self.quantity = quantity
        self.timing = timing
        self.name = self.culture.value[0]
        self.attenuation = (self.culture.value[1], self.culture.value[2])
        self.desc = self.name if desc is None else desc

class Ingredient:
    """Beer ingredient.

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
    ppg : PPG or float
      The item being fermented, or the number of gravity points added
      per pound per gallon (requires `name`).
    weight : float
      The weight in pounds.
    grain : bool, optional
      Indicates if this ingredient is a grain (especially for mash
      water absorption calculation).  Ignored if `ppg` is a `PPG`
      instance.
    fermentable100 : bool, optional
      Indicates if this ingredient is 100% fermentable.  Ignored if
      `ppg` is a `PPG` instance.
    timing : Timing, optional
      The timing of the addition.
    name : string, optional
      Use this name instead of the name in the `PPG` object.  Required
      if `ppg` is a float.
    desc : string, optional
      A long-form description.

    """

    def __init__(self, ppg, weight, grain=True, fermentable100=False,
                 timing=T.Mash(), name=None, desc=None):
        assert isinstance(ppg, (PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(grain, bool)
        assert isinstance(fermentable100, bool)
        assert isinstance(name, (str, type(None)))
        assert isinstance(desc, (str, type(None)))

        if isinstance(ppg, PPG):
            self.name, self.ppg, self.grain, self.fermentable100 = ppg.value
            if name is not None:
                self.name = name
        else:
            self.ppg = float(ppg)
            self.grain = grain
            self.fermentable100 = fermentable100
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
        assert isinstance(ppg, (PPG, float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, T.Timing)
        assert isinstance(name, (str, type(None)))
        assert isinstance(desc, (str, type(None)))

        if isinstance(ppg, PPG):
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
    whole : bool, optional
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

        from .util import ibu, utilization

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

        util = utilization(t, gravity, whole=self.whole)
        bit = ibu(util, self.weight, self.alpha, volume)

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
        self.grain = False
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

class Ingredients(MutableSequence):
    """A collection of ingredients.

    Parameters
    ----------
    a : list
      A list of `Ingredient`s.

    """

    def __init__(self, a=[]):
        from collections import Iterable
        assert isinstance(a, Iterable)
        self._list = list(a)

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
        return "<Ingredients: {} items ({} fermentables, {} hops)>".format(
            len(self), len(self.fermentables), len(self.hops))

    def __str__(self):
        s = "Ingredients:\n  "
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

    def upto(self, time):
        """All ingredients included up to `time`.

        Parameters
        ----------
        time : Timing
        
        """
        return Ingredients([i for i in self if i.timing < time])

    def at(self, time):
        """All ingredients included at `time`.

        Parameters
        ----------
        time : Timing
        
        """
        return Ingredients([i for i in self if i.timing <= time])

    def after(self, time):
        """All ingredients included after `time`.

        Parameters
        ----------
        time : Timing
        
        """
        return Ingredients([i for i in self if i.timing > time])

    @property
    def mash(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Mash), self)))
        
    @property
    def vorlauf(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Vorlauf), self)))
        
    @property
    def first_wort(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.FirstWort), self)))
        
    @property
    def boil(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Boil), self)))
    
    @property
    def hop_stand(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.HopStand), self)))

    @property
    def primary(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Primary), self)))
        
    @property
    def secondary(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Secondary), self)))
        
    @property
    def packaging(self):
        return Ingredients(list(filter(lambda v: isinstance(v.timing, T.Packaging), self)))

    @property
    def fermentables(self):
        return Ingredients(list(filter(lambda v: isinstance(v, Fermentable), self)))

    @property
    def grains(self):
        return Ingredients(list(filter(lambda v: v.grain, self.fermentables)))

    @property
    def unfermentables(self):
        return Ingredients(list(filter(lambda v: isinstance(v, Unfermentable), self)))
    
    @property
    def fruits(self):
        return Ingredients(list(filter(lambda v: isinstance(v, Fruit), self)))
    
    @property
    def hops(self):
        return Ingredients(list(filter(lambda v: isinstance(v, Hop), self)))
    
    @property
    def cultures(self):
        return Ingredients(list(filter(lambda v: isinstance(v, Culture), self)))
