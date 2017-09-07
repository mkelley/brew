# Licensed under an MIT style license - see LICENSE

"""
util --- Small brewing functions.
=================================

"""

__all__ = [
    'abv',
    'abw',
    'calories',
    'calories_alcohol',
    'calories_extract',
    'calories_protein',
    'carbohydrates',
    'f2c',
    'final_gravity',
    'hydrometer_correct',
    'ibu',
    'infusion_volume',
    'priming_sugar',
    'real_attenutation',
    'real_extract',
    'refractometer_correct',
    'sg2brix',
    'sg2plato',
    'strike_water',
    'utilization',
]

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

def carbohydrates(og, fg):
    """Estimated carbohydrates per 12 oz."""
    return calories_extract(og, fg) / 3.8

def f2c(T):
    """Fahrenheit to Celcius."""
    return (T - 32) * 5 / 9.

def final_gravity(sg, T_sacc, culture):
    """Estimate final gravity.
    
    Parameters
    ----------
    sg : float
      Starting gravity, without any 100% fermentables.
    T_sacc : int or array-like
      Saccharification temperature(s).  For a list, the average will be used.
    culture : CultureBank or array-like
      The culture to use for fermentation, `(name, attenuation)`, or
      `(name, min, max attenuation)`.

    Returns
    -------
    fg : float

    """
    
    from collections import Iterable
    from .ingredients import Culture

    assert isinstance(culture, (Culture, Iterable))
    if isinstance(culture, Culture):
        aa = culture.attenuation
    else:
        aa = culture[1:]

    if isinstance(T_sacc, Iterable):
        T = sum(T_sacc) / len(T_sacc)
    else:
        T = T_sacc

    atten = sum(aa) / len(aa)
    dT = T - 152
    a = atten - dT
    return sg - (sg - 1) * a / 100

def hydrometer_correct(sg, T):
    """Correct hydrometer specific gravity measurment.

    Equation is accurate from 32 F to 212 F (60/60).

    Parmeters
    ---------
    sg : float
      Specific gravity.
    T : float
      Temperature, °F.

    Notes
    -----

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """
    return sg * (1.00130346
                 - 1.34722124e-4 * T
                 + 2.04052596e-6 * T**2
                 - 2.32820948e-9 * T**3)

def ibu(utilization, weight, alpha, volume):
    """Utilization and alpha in percent, weight in oz, volume in gallons."""
    return 0.746 * utilization * weight * alpha / volume

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

def refractometer_correct(sg0, sg_r):
    """Correct final gravity measurment from refractometer.

    Parameters
    ----------
    sg0 : float
      Starting specific gravity.
    sg_r : float
      Raw (uncorrected) specific gravity measurement from refractometer.

    """
    return 1 - 0.002349 * sg2brix(sg0) + 0.006276 * sg2brix(sg_r)

def sg2brix(sg):
    """Specific gravity to degrees brix

    Parmeters
    ---------
    sg : float
      Specific gravity.

    Notes
    -----
    http://www.brewersfriend.com/brix-converter/
    
    """
    return ((182.461 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622

def sg2plato(sg):
    """Extract in degrees Plato.

    Valid for the range 0 to 33° Plato / 1.000 to 1.144.

    Parmeters
    ---------
    sg : float
      Specific gravity.

    Notes
    -----
    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """
    return -668.962 + 1262.45 * sg - 776.43 * sg**2 + 182.94 * sg**3

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

def utilization(t, sg, whole=False):
    """Percent hop utilization, Tinseth method.

    Formula source: Modern Homebrew Recipes, Gordon Strong.  For whole
    hops, the utilization is reduced by 15%, based on The Complete Joy
    of Homebrewing, Charlie Papazian.

    Parameters
    ----------
    t : float
      Time in the boil. [min]
    sg : float
      Specific gravity of the boil.
    whole : bool
      Set to `True` if using whole hops.  `False` assumes pellets.

    """

    from math import exp

    u = 1.65 * 0.000125**(sg - 1) * (1 - exp(-0.04 * t)) / 4.15
    u *= 0.85 if whole else 1.0
    return u * 100
