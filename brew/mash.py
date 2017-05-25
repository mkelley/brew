# Licensed under an MIT style license - see LICENSE

"""
mash --- Wort and mash.
=======================

"""

from enum import Enum

# Source: Home Brewer's Companion
# Beersmith: http://www.beersmith.com/Grains/Grains/GrainList.htm
# name, PPG, 100% fermentatble flag
class PPG(Enum):
    AcidMalt = "Acid malt", 27, False  # (Germany) Beersmith
    AmericanTwoRow = "American 2-row", 37, False
    AmericanSixRow = "American 6-row", 35, False
    AmericanPaleAle = "American pale ale", 36, False
    BelgianPaleAle = "Belgian pale ale", 37, False
    BelgianPilsener = "Belgian pilsener", 37, False
    DriedMaltExtract = "Dried malt extract", 44, False
    EnglishTwoRow = "English 2-row", 38, False
    EnglishMild = "English mild", 37, False
    MarisOtter = "Maris Otter", 38, False
    WheatMalt = "Wheat malt", 38, False  # midwest / german / belgian
    AmericanRyeMalt = "American rye malt", 36, False
    GermanRyeMalt = "German rye malt", 38, False
    GermanPilsner = "German pilsner", 37, False
    EnglishRyeMalt = "English rye malt", 40, False
    EnglishOatMalt = "English oat malt", 35, False
    AmericanVienna = "American Vienna", 36, False
    GermanVienna = "German Vienna", 37, False
    AmericanCarapils = "American Carapils", 34, False  # dextrine
    BelgianCarapils = "Belgian Carapils", 36, False
    AmericanMunich = "American Munich", 34, False
    GermanMunich = "German Munich", 37, False
    GermanMunichII = "Germain Munich II", 36, False
    BelgianMunich = "Belgian Munich", 37, False
    Caramunich = "Caramunich", 33, False  # Beersmith
    AmericanCaramel10 = "American caramel 10", 35, False
    AmericanCaramel20 = "American caramel 20", 35, False
    AmericanCaramel40 = "American caramel 40", 35, False
    AmericanCaramel60 = "American caramel 60", 34, False
    AmericanCaramel120 = "American caramel 120", 33, False
    EnglishCrystal20_30 = "English crystal 20-30", 36, False
    EnglishCrystal60_70 = "English crystal 60-70", 34, False
    EnglishCaramalt = "English Caramalt", 36, False
    BelgianCrystal = "Belgian crystal", 36, False
    AmericanVictory = "American Victory", 33, False
    BelgianBiscuit = "Belgian biscuit", 36, False
    BelgianAromatic = "Belgian aromatic", 36, False
    EnglishBrown = "English brown", 33, False
    EnglishAmber = "English amber", 33, False
    BelgianSpecialB = "Belgian Special B", 35, False
    AmericanChocolate = "American chocolate", 28, False  # Beersmith
    EnglishPaleChocolate = "English pale chocolate", 34, False # Beersmith
    EnglishChocolate = "English chocolate", 34, False  # Beersmith
    Carahell = "Carahell", 35, False  # guess
    Black = "Black", 25, False  # Beersmith
    RoastedBarley = "Roasted barley", 18, False
    BarleyRaw = "Barley, raw", 32, False  # 30 to 34
    Barleyflaked = "Barley, flaked", 32, False  # 30 to 34
    CornFlaked = "Corn, flaked", 39, False
    CornGrits = "Corn grits", 37, False
    MilletRaw = "Millet, raw", 37, False
    SorghumRaw = "Sorghum, raw", 37, False
    OatsRaw = "Oats, raw", 33, False
    OatsFlaked = "Oats, flaked", 33, False
    RiceRaw = "Rice, raw", 38, False
    RiceFlaked = "Rice, flaked", 38, False
    RyeRaw = "Rye, raw", 36, False
    RyeFlaked = "Rye, flaked", 36, False
    WheatFlaked = "Wheat, flaked", 33, False
    WheatRaw = "Wheat, raw", 37, False
    WheatTorrified = "Wheat, torrified", 35, False
    AgaveSyrup = "Agave syrup", 34, False
    BelgianCandiSugar = "Belgian candi sugar", 46, True
    BelgianCandiSyrup = "Belgian candi syrup", 36, True
    CaneSugar = "Cane sugar", 46, True
    LightBrownSugar = "Light brown sugar", 46, True
    DarkBrownSugar = "Dark brown sugar", 46, True
    CornSugarDextrose = "Corn sugar (dextrose)", 46, True
    Lactose = "Lactose", 35, False
    Honey = "Honey", 32, True  # 30 to 35
    MapleSap = "Maple sap", 9, True
    MapleSyrup = "Maple syrup", 30, True  # variable
    Molasses = "Molasses", 36, True
    Rapadura = "Rapadura", 40, True
    RiceExtract = "Rice extract", 34, True
    WhiteSorghumSyrup = "White sorghum syrup", 38, True
    PumpkinPuree = "Pumpkin puree", 2, False

def strike_water(r, T_grain, T_target):
    """Temperature of strike water.

    Parameters
    ----------
    r : float
      Ratio of water volume to grain weight. [qt/lb]
    T_grain : float
      Temperature of grain. [F]
    T_target : float
      Target temperature. [F]

    """
    return 0.2 / r * (float(T_target) - T_grain) + T_target

def infusion_volume(volume, weight, T, T_target, T_water=200.):
    """Volume of water infusion to reach temperature T_target.

    Parameters
    ----------
    volume : float
      Present water volume. [qt]
    weight : float
      Grain weight. [lb]
    T : float
      Present mash temperature. [F]
    T_target : float
      Target temperature. [F]
    T_water : float, optional
      Infusion water temperature. [F]

    """
    return (T_target - T) * (.2 * weight + volume) / (T_water - T)
