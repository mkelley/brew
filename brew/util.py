# Licensed under an MIT style license - see LICENSE

"""
util --- Small brewing functions.
=================================

"""

__all__ = [
    'strike_water',
    'infusion_volume'
]

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
