# Licensed under an MIT style license - see LICENSE

"""
fermentation --- Yeast and fermentations.
=========================================

"""

from enum import Enum

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
    FrenchSaison = ('WLP590, French Saison', 73, 80)
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

def abv(og, fg):
    """Alcohol by volume.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    return abw(og, fg) * fg / 0.794

def abw(og, fg):
    """Alcohol by weight.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    re = real_extract(og, fg)
    return (oe - re) / (2.0665 - 0.010665 * oe)

def carbohydrates(og, fg):
    """Estimated carbohydrates per 12 oz."""
    return calories_extract(og, fg) / 3.8

def calories(og, fg):
    """Calories per 12 oz."""
    return (calories_alcohol(og, fg)
            + calories_extract(og, fg)
            + calories_protein(og, fg))

def calories_alcohol(og, fg):
    """Calories from alcohol per 12 oz.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    return 25.2 * fg * abw(og, fg)

def calories_extract(og, fg):
    """Calories from residual sugars per 12 oz.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    return 13.5 * fg * real_extract(og, fg)    

def calories_protein(og, fg):
    """Calories from protein per 12 oz.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    return 0.994 * fg * real_extract(og, fg)

def final_gravity(sg, T_sacc, culture):
    """Estimate final gravity.
    
    Parameters
    ----------
    sg : float
      Starting gravity, without any 100% fermentables.
    T_sacc : int or array
      Saccharification temperature(s).  For a list, the average will be used.
    culture : CultureBank or array
      The culture to use for fermentation, `(name, attenuation)`, or
      `(name, min, max attenuation)`.

    Returns
    -------
    fg : float

    """
    
    import collections

    assert isinstance(culture, (CultureBank, collections.Iterable))
    if isinstance(culture, CultureBank):
        c = culture.value
    else:
        c = culture

    atten = sum(c[1:]) / (len(c) - 1)
    dT = T_sacc - 152
    a = atten - dT
    return sg - (sg - 1) * a / 100

def priming_sugar(T, r, v, fermentable='table sugar'):
    """Weight of sugar for priming.

    Parameters
    ----------
    T : float
      Fermentation temperature in Fahrenheit.
    r : float
      Ratio of CO2 volume at STP to beer volume (i.e., volumes of
      dissolved CO2).
    v : float
      Volume of beer, gallons.
    fermentable : string
      Type of fermentable: corn sugar, table sugar, dry malt extract,
      or honey.

      American ales: 2.2 to 3.0
       British ales: 1.5 to 2.2
     German weizens: 2.8 to 5.1
       Belgian ales: 2.0 to 4.5
    European lagers: 2.4 to 2.6
    American lagers: 2.5 to 2.8

    1 "volume of CO2" is 1 liter of CO2 at STP dissolved in 1 liter
    liquid.

    For other sugars:
      Dry malt extract = 1.54 * corn
      Table sugar = 0.95 * corn
      Honey = 1.11 * corn

    Brad Smith, BYO May-Jun 2015 (vol 21, no 3)

    """
    scales = {
        'corn sugar': 1.0,
        'table sugar': 0.95,
        'dry malt extract': 1.54,
        'honey': 1.11
    }
    assert fermentable in scales
    scale = scales[fermentable]
    return scale * (0.5360 * v) *  ((r - 3.0378) + (0.050 * T) - (0.0002655 * T**2))

def real_attenuation(og, fg):
    """Real attenuation (%) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    re = real_extract(og, fg)
    return (oe - re) / oe * 100.

def real_extract(og, fg):
    """Real extract (degrees Plato) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    ae = sg2plato(fg)
    q = 0.22 + 0.001 * oe
    return (q * oe + ae) / (1 + q)
