# Licensed under an MIT style license - see LICENSE

"""
fermentation --- Yeast and fermentations.
=========================================

"""

# key, (name, min, max apparent attenutation)
yeast_data = {
    'WLP001': ('California Ale', 73, 80),
    'WLP002': ('English Ale', 63, 70),
    'WLP004': ('Irish Ale', 69, 74),
    'WLP051': ('California Ale V', 70, 75),
    'WLP072': ('French Ale', 68, 75),
    'WLP080': ('Cream Ale Blend', 75, 80),
    'WLP300': ('Hefeweizen', 72, 76),
    'WLP400': ('Belgian Wit', 74, 78),
    'WLP500': ('Monastery Ale', 75, 80),
    'WLP530': ('Abbey Ale', 75, 80),
    'WLP550': ('Belgian Ale', 78, 85),
    'WLP565': ('Belgian Saison I', 65, 75),
    'WLP566': ('Belgian Saison II', 78, 85),
    'WLP568': ('Belgian Style Saison', 70, 80),
    'WLP570': ('Belgian Golden Ale', 73, 78),
    'WLP585': ('Belgian Saison III', 70, 74),
    'WLP590': ('French Saison', 73, 80),
    'WLP810': ('San Francisco Lager', 65, 70),
    'WLP820': ('Oktoberfest/Märzen Lager', 65, 73),
    'WLP644': ('Sacchromyces bruxellensis Trois', 85, 100),
    'WLP645': ('Brettanomyces claussenii', 85, 100),
    'WLP648': ('Brettanomyces bruxellensis Trois Vrai', 85, 100),
    'WLP650': ('Brettanomyces bruxellensis', 85, 100),
    'WLP650': ('Brettanomyces lambicus', 85, 100),
    'WLP655': ('Sour Mix 1', 85, 100),
    'WLP665': ('Flemish Ale Blend', 80, 100),
    'WLP670': ('American Farmhouse Blend', 75, 82),
}

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

def final_gravity(sg, T_mash, yst):

    """Estimate final gravity.
    
    Parameters
    ----------
    sg : float
      Starting gravity, without any 100% fermentables.
    T_mash : float
      Mash temperature.
    yst : string or tuple
      Name of a yeast strain, (name, attenuation), or (name, (min, max
      attenuation)).

    Returns
    -------
    fg : float
    app_atten : float

    """

    name, atten = yeast(yst)
    dT = T_mash - 152
    if isinstance(atten, (list, tuple)):
        a = sum(atten) / 2 - dT
    else:
        a = atten - dT

    return sg - (sg - 1) * a / 100, a

def find_yeast(k):
    """Find yeast data by product key in internal database.

    """

    try:
        name, atten_min, atten_max = yeast_data[k]
    except KeyError:
        print("Yeast not found.  Valid values:")
        for k, v in sorted(yeast_data.items()):
            print('"{}" ({})'.format(k, v[0]))
        raise

    return k, name, (atten_min, atten_max)

def priming_sugar(T, r, v):
    """Weight of corn sugar for priming.

    Parameters
    ----------
    T : float
      Fermentation temperature in Fahrenheit.
    r : float
      Ratio of CO2 volume at STP to beer volume (i.e., volumes of
      dissolved CO2).
    v : float
      Volume of beer, gallons.

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
      Table sugar = 0.905 * corn
      Honey = 1.11 * corn

    Brad Smith, BYO May-Jun 2015 (vol 21, no 3)

    """

    return (0.5360 * v) *  ((r - 3.0378) + (0.050 * T) - (0.0002655 * T**2))

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

def yeast(y):
    """Yeast name and attenuation.

    First checks that `y` is a tuple of (name, attenuation) or (name,
    (min, max attenuation)).  If not, then find yeast from the
    internal database.

    """

    try:
        if isinstance(y, (tuple, list)):
            assert isinstance(y[0], str)
            assert isinstance(y[1], (tuple, list, float, int))
            if isinstance(y[1], (tuple, list)):
                assert len(y[1]) == 2
                assert isinstance(y[1][0], (float, int))
                assert isinstance(y[1][1], (float, int))
        elif isinstance(y, str):
            product, name, atten = find_yeast(y)
            name = '{} / {}'.format(product, name)
            y = name, atten
        else:
            raise TypeError
        return y
    except (TypeError, AssertionError) as exc:
        raise TypeError('yeast must be a product key (e.g., "WLP001") or a 2-element tuple: (name, attenuation in %).  attenuation may be a tuple of min, max attenuation.') from exc

