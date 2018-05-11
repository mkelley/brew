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
    'Grain',
    'Sugar',
    'Other',
    'Priming',
    'Water',
    'Ingredients',
]

# Source: Home Brewer's Companion
# Beersmith: http://www.beersmith.com/Grains/Grains/GrainList.htm
# name, PPG
class PPG(Enum):
    AcidMalt = "Acid malt", 27  # (Germany) Beersmith
    AmericanTwoRow = "American 2-row", 37
    AmericanSixRow = "American 6-row", 35
    AmericanPaleAle = "American pale ale", 36
    BelgianPaleAle = "Belgian pale ale", 37
    BelgianPilsener = "Belgian pilsener", 37
    DriedMaltExtract = "Dried malt extract", 44
    EnglishTwoRow = "English 2-row", 38
    EnglishMild = "English mild", 37
    MarisOtter = "Maris Otter", 38
    GoldenPromise = "Golden Promise", 38
    WheatMalt = "Wheat malt", 38  # midwest / german / belgian
    AmericanRyeMalt = "American rye malt", 36
    GermanRyeMalt = "German rye malt", 38
    GermanPilsner = "German pilsner", 37
    EnglishRyeMalt = "English rye malt", 40
    EnglishOatMalt = "English oat malt", 35
    AmericanVienna = "American Vienna", 36
    GermanVienna = "German Vienna", 37
    AmericanCarapils = "American Carapils", 34  # dextrine
    BelgianCarapils = "Belgian Carapils", 36
    AmericanMunich = "American Munich", 34
    GermanMunich = "German Munich", 37
    GermanMunichII = "Germain Munich II", 36
    BelgianMunich = "Belgian Munich", 37
    Caramunich = "Caramunich", 33  # Beersmith
    AmericanCaramel10 = "American caramel 10", 35
    AmericanCaramel20 = "American caramel 20", 35
    AmericanCaramel40 = "American caramel 40", 35
    AmericanCaramel60 = "American caramel 60", 34
    AmericanCaramel120 = "American caramel 120", 33
    EnglishCrystal20_30 = "English crystal 20-30", 36
    EnglishCrystal60_70 = "English crystal 60-70", 34
    EnglishCaramalt = "English Caramalt", 36
    BelgianCrystal = "Belgian crystal", 36
    AmericanVictory = "American Victory", 33
    BelgianBiscuit = "Belgian biscuit", 36
    BelgianAromatic = "Belgian aromatic", 36
    EnglishBrown = "English brown", 33
    EnglishAmber = "English amber", 33
    BelgianSpecialB = "Belgian Special B", 35
    AmericanChocolate = "American chocolate", 28  # Beersmith
    EnglishPaleChocolate = "English pale chocolate", 34 # Beersmith
    EnglishChocolate = "English chocolate", 34  # Beersmith
    Carahell = "Carahell", 35  # guess
    Black = "Black", 25  # Beersmith
    RoastedBarley = "Roasted barley", 18
    BarleyRaw = "Barley, raw", 32  # 30 to 34
    Barleyflaked = "Barley, flaked", 32  # 30 to 34
    CornFlaked = "Corn, flaked", 39
    CornGrits = "Corn grits", 37
    MilletRaw = "Millet, raw", 37
    SorghumRaw = "Sorghum, raw", 37
    OatsRaw = "Oats, raw", 33
    OatsFlaked = "Oats, flaked", 33
    RiceRaw = "Rice, raw", 38
    RiceFlaked = "Rice, flaked", 38
    RyeRaw = "Rye, raw", 36
    RyeFlaked = "Rye, flaked", 36
    WheatFlaked = "Wheat, flaked", 33
    WheatRaw = "Wheat, raw", 37
    WheatTorrified = "Wheat, torrified", 35
    
    AgaveSyrup = "Agave syrup", 34
    BelgianCandiSugar = "Belgian candi sugar", 46
    BelgianCandiSyrup = "Belgian candi syrup", 36
    CaneSugar = "Cane sugar", 46
    TableSugar = "Table sugar", 46
    TurbinadoSugar = "Turbinado sugar", 46
    LightBrownSugar = "Light brown sugar", 46
    DarkBrownSugar = "Dark brown sugar", 46
    CornSugarDextrose = "Corn sugar (dextrose)", 46
    Lactose = "Lactose", 35
    Honey = "Honey", 32  # 30 to 35
    MapleSap = "Maple sap", 9
    MapleSyrup = "Maple syrup", 30  # variable
    Molasses = "Molasses", 36
    Rapadura = "Rapadura", 40
    RiceExtract = "Rice extract", 34
    WhiteSorghumSyrup = "White sorghum syrup", 38
    
    PumpkinPuree = "Pumpkin puree", 2

class CultureBank(Enum):
    # name, min, max apparent attenutation
    AmericanAleUS05 = ('US-05, American Ale', 81, 81)
    AmericanAle1056 = ('WY1056, American Ale', 73, 77)
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
    LactobacillusBrevis = ('WLP672, Lactobacillus Brevis', 80, 80)
    LactobacillusDelbrueckii = ('WLP677, Lactobacillus Delbrueckii', 75, 82)
    HouseSourMix = ('House sour mix', 86, 86)
    BottleDregs = ('Bottle dregs', 0, 100)

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

class Culture(Ingredient):
    """Yeast or other cultures, ready for fermentation.

    Parameters
    ----------
    culture : CultureBank
      Type of culture to propagate.
    quantity : string, optional
      Quantity of the culture.
    timing : Timing, optional
      Timing of the addition.
    desc : string, optional
      Long-form description.
    
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

class Fermentable(Ingredient):
    """Grains and adjuncts.

    Parameters
    ----------
    ppg : PPG, int, or float
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
            self.ppg = int(ppg)
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
        if self.timing < T.Lauter():
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
            ppg = int(ppg)
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
        if self.timing < T.Lauter():
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
                 beta=None, desc=None):
        assert isinstance(name, str)
        assert isinstance(alpha, (float, int))
        assert isinstance(weight, (float, int))
        assert isinstance(timing, (T.Timing, type(None)))
        assert isinstance(whole, bool)
        assert isinstance(beta, (float, int, type(None)))
        assert isinstance(desc, (str, type(None)))

        self.name = name
        self.alpha = alpha
        self.weight = weight
        self.timing = timing
        self.whole = whole
        self.beta = beta
        self.desc = name if desc is None else desc

    def __repr__(self):
        return '<Hop: {}>'.format(str(self))

    def __str__(self):
        if self.beta is None:
            beta = ''
        else:
            beta = ', {}% β'.format(self.beta)
        return '{} ({}% α{}), {} at {}'.format(
            self.name, self.alpha, beta, self.quantity,
            self.timing if self.timing is not None else T.Unspecified())

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

class Grain(Fermentable):
    """A mashable grain or similar."""
    def __init__(self, ppg, weight, timing=T.Mash(), name=None, desc=None):
        Fermentable.__init__(self, ppg, weight, timing=timing, name=name,
                             desc=desc)

class Sugar(Fermentable):
    """Sugars, syrups, and similar 100% fermentables."""
    def __init__(self, ppg, weight, timing=T.Boil(0), name=None, desc=None):
        Fermentable.__init__(self, ppg, weight, timing=timing, name=name,
                             desc=desc)

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
    volume : float, optional
      The volume in gallons.
    timing : Timing
      The time of addition.
    desc : string, optional
      A long-form description.

    """
    
    def __init__(self, name, volume=0, timing=T.Unspecified(), desc=None):
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
    a : iterable
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
        from .table import Table
        item, quantity, timing = [], [], []
        for i in self:
            item.append(i.name)
            quantity.append(i.quantity)
            timing.append(str(i.timing))

        tab = Table(data=(item, quantity, timing),
                    names=('Item', 'Quantity', 'Timing'))
        return str(tab)
    
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
        return self.filter(Fermentable)

    @property
    def unfermentables(self):
        return self.filter(Unfermentable)
    
    @property
    def grains(self):
        return self.filter(Grain)

    @property
    def sugars(self):
        return self.filter(Sugar)

    @property
    def spices(self):
        return self.filte(Spice)

    @property
    def fruits(self):
        return self.filter(Fruit)
    
    @property
    def hops(self):
        return self.filter(Hop)
    
    @property
    def cultures(self):
        return self.filter(Culture)

    def filter(self, *t):
        """Filter ingredients by type and/or timing.

        Parameters
        ----------
        *t : Ingredient or Timing classes
          The types or timing of ingredients to return.

        """

        ingredients = self
        
        if any([issubclass(x, Ingredient) for x in t]):
            i = filter(lambda i: isinstance(i, t), ingredients)
            ingredients = Ingredients(i)
        
        if any([issubclass(x, T.Timing) for x in t]):
            i = filter(lambda i: isinstance(i.timing, t), ingredients)
            ingredients = Ingredients(i)

        return ingredients
