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

def hop_additions(hops):
    """Generator yielding (name, alpha, weight, time) from hop dictionary.

    Designed for `schedule`.

    Each dictionary key is the hop name, each value is `(alpha,
    weight, time)` where weight and time may be arrays.  Weight in
    ounces, alpha as % by weight, boil time in minutes.

    """

    for name, (alpha, weight, time) in hops.items():
        n_weights = len(weight) if isinstance(weight, (tuple, list)) else 1
        n_time = len(time) if isinstance(time, (tuple, list)) else 1
        n = max(n_weights, n_time)
        _weight = [weight] * n if n_weights == 1 else weight
        _time = [time] * n if n_time == 1 else time

        assert len(_weight) == len(_time), "Incompatible weight and time for {}: {}, {}".format(name, weight, time)

        for i in range(n):
            yield name, alpha, _weight[i], _time[i]

def schedule(sg, volume, hops, whole=False, hop_stand=False, html=False):
    """Compute IBUs based on a hop schedule and wort boil.

    Hop schedule will be sorted by time, weight, then alpha.

    Parameters
    ----------
    sg : float
      The approximate specific gravity of the boil.
    volume : float
      The final volume of the boil.
    hops : dict
      Each key is the hop name, each value is `(alpha, weight, time)`
      where weight and time may be arrays.  Weight in ounces, alpha as
      % by weight, boil time in minutes.
    whole : bool, optional
      Set to `True` if the hops are whole leaf.  Otherwise, pellets
      are assumed.
    hop_stand : bool, optional
      If `True`, then hops added after 5 min will have an alpha acid
      utilization equivalent to a 5 min boil.
    html : bool
      True to print HTML-formatted table.

    Returns
    -------
    util : list
      The computed utilization percentages.  [%]
    bit : list
      The computed bitterness contributions.  [IBU]
    outs : str
      A table of hop additions.

    """

    from operator import itemgetter
    from .util import tab2txt

    assert isinstance(sg, (float, int))
    assert isinstance(volume, (float, int))

    tab = []
    for (name, alpha, weight, time) in hop_additions(hops):
        tt = max(5.0, time) if hop_stand else time
        util = utilization(tt, sg, whole=whole)
        bit = ibu(util, weight, alpha, volume)
        tab.append([name, alpha, weight, time, util, bit])

    tab.sort(key=itemgetter(0))
    tab.sort(key=itemgetter(3), reverse=True)
    util = [row[-2] for row in tab]
    bit = [row[-1] for row in tab]

    colnames = ['Hop', 'Alpha', 'Weight', 'Time', 'Utilization',
                'Bitterness']
    colformats = ['{}', '{:.1f}', '{:.1f}', '{:.0f}', '{:.1f}', '{:.0f}']

    footer = ['Boil specific gravity: {:.3f}'.format(sg),
              'Volume: {} gal'.format(volume),
              'Whole leaf' if whole else 'Pellets']
    if hop_stand:
        footer += ['Hop stand']
    footer += ['Total bitterness: {:.0f} IBU'.format(sum(bit))]
    footer = ', '.join(footer)

    outs = tab2txt(tab, colnames, footer, colformats=colformats, html=html)

    return util, bit, outs
