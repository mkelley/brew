# Licensed under an MIT style license - see LICENSE

"""
mash --- Wort and mash.
=======================

"""

from enum import Enum

# Source: Home Brewer's Companion
# Beersmith: http://www.beersmith.com/Grains/Grains/GrainList.htm
class PPG(Enum):
    AmericanTwoRow = "American 2-row", 37
    AmericanSixRow = "American 6-row", 35
    AmericanPaleAle = "American pale ale", 36
    BelgianPaleAle = "Belgian pale ale", 37
    BelgianPilsener = "Belgian pilsener", 37
    EnglishTwoRow = "English 2-row", 38
    EnglishMild = "English mild", 37
    MarisOtter = "Maris Otter", 38
    WheatMalt = "Wheat malt",  38  # midwest / german / belgian
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
    EnglishPaleChocolate = "English pale chocolate", 34  # Beersmith
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
    riceFlaked = "Rice, flaked", 38
    RyeRaw = "Rye, raw", 36
    RyeFlaked = "Rye, flaked", 36
    WheatFlaked = "Wheat, flaked", 33
    WheatRaw = "Wheat, raw", 37
    WheatTorrified = "Wheat, torrified", 35
    AgaveSyrup = "Agave syrup", 34
    BelgianCandiSugar = "Belgian candi sugar", 46
    BelgianCandiSyrup = "Belgian candi syrup", 36
    CaneSugar = "Cane sugar", 46
    LightBrownSugar = "Light brown sugar", 46
    DarkBrownSugar = "Dark brown sugar", 46
    CornSugarDextrose = "Corn sugar (dextrose)", 46
    Honey = "Honey", 32  # 30 to 35
    MapleSap = "Maple sap", 9
    MapleSyrup = "Maple syrup", 30  # variable
    Molasses = "Molasses", 36
    Rapadura = "Rapadura", 40
    RiceExtract = "Rice extract", 34
    WhiteSorghumSyrup = "White sorghum syrup", 38
    PumpkinPuree = "Pumpkin puree", 2

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
