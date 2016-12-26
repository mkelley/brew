# Licensed under an MIT style license - see LICENSE

"""
hops --- Hops and hopping.
==========================

"""

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

def ibu(utilization, weight, alpha, volume):
    """Utilization and alpha in percent, weight in oz, volume in gallons."""
    return 0.746 * utilization * weight * alpha / volume
