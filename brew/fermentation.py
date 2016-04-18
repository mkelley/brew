# Licensed under an MIT style license - see LICENSE

"""
fermentation --- Yeast and fermentations.
=========================================

"""

def real_extract(og, fg):
    """Real extract (degrees Plato) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    ae = sg2plato(fg)
    q = 0.22 + 0.001 * oe
    return (q * oe + ae) / (1 + q)

def real_attenuation(og, fg):
    """Real attenuation (%) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    re = real_extract(og, fg)
    return (oe - re) / oe * 100.

def abv(og, fg):
    """Alcohol by volume.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    from .util import sg2plato

    oe = sg2plato(og)
    re = real_extract(og, fg)
    abw = (oe - re) / (2.0665 - 0.010665 * oe)
    return abw * fg / 0.794

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

