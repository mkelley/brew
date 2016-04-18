# Licensed under an MIT style license - see LICENSE

"""
mash --- Wort and mash.
=======================

"""

ppg_data = {
    # Source: Home Brewer's Companion
    # Beersmith: http://www.beersmith.com/Grains/Grains/GrainList.htm
    'American 6-row': 35,
    'American 2-row': 37,
    'Belgian pale ale': 37,
    'Belgian pilsener': 37,
    'English 2-row': 38,
    'Maris Otter': 38,
    'wheat malt': 38,  # midwest / german / belgian
    'American rye malt': 36,
    'German rye malt': 38,
    'German pilsner': 37,
    'English rye malt': 40,
    'English oat malt': 35,
    'American Vienna': 36,
    'German Vienna': 37,
    'English 2-row Vienna': 36,
    'American Carapils': 34,  # dextrine
    'Belgian Carapils': 36,
    'American Munich': 34,
    'German Munich II': 36,
    'German Munich': 37,
    'Belgian Munich': 37,
    'Caramunich': 33,  # Beersmith
    'American caramel 10': 35,
    'American caramel 20': 35,
    'American caramel 40': 35,
    'American caramel 60': 34,
    'American caramel 120': 33,
    'English crystal 20-30': 36,
    'English Caramalt': 36,
    'Belgian crystal': 36,
    'American victory': 33,
    'Belgian biscuit': 36,
    'Belgian aromatic': 36,
    'English brown': 33,
    'English amber': 33,
    'Belgian special B': 35,
    #'chocolate': (23, 28),
    'American chocolate': 28,  # Beersmith
    'English pale chocolate': 34,  # Beersmith
    'English chocolate': 34,  # Beersmith
    'Carahell': 35,  # guess
    #'black': (23, 28),
    'black': 25,  # Beersmith
    'roasted barley': 18,
    'barley, raw': (30, 34),
    'barley, flaked': (30, 34),
    'corn, flaked': 39,
    'corn, grits': 37,
    'millet, raw': 37,
    'sorghum, raw': 37,
    'oats, raw': 33,
    'oats, flaked': 33,
    'rice, raw': 38,
    'rice, flaked': 38,
    'rye, raw': 36,
    'rye, flaked': 36,
    'wheat, flaked': 33,
    'wheat, raw': 37,
    'wheat, torrified': 35,
    'agave syrup': 34,
    'Belgian candi sugar': 46,
    'cane sugar': 46,
    'corn sugar, dextrose': 46,
    'honey': (30, 35),
    'maple sap': 9,
    'maple syrup': 30,  # varible
    'molasses': 36,
    'rapadura': 40,
    'rice extract': 34,
    'white sorghum syrup': 38,
}

def grain_generator(grain):
    """Create a generator that yields name, weight, ppg from a dictionary.

    Designed for `wort`.  The dictionary keys are the grain names,
    values are either `weight` (for grains in ppg_db) or `(weight,
    ppg)`.  `weight` is in pounds.

    """

    from operator import itemgetter
    for name, v in sorted(grain.items(), key=itemgetter(1), reverse=True):
        if isinstance(v, (list, tuple)):
            weight, ppg = v
        else:
            weight = v
            try:
                ppg = ppg_data[name]
            except KeyError:
                print("{} not found.  Valid grain/adjucts:".format(grain))
                for k in sorted(ppg_data.keys()):
                    print("  ", k)
                raise

        if isinstance(ppg, tuple):
            ppg = int(sum(ppg) / len(ppg))

        yield name, weight, ppg

def wort(mash, kettle, volume, efficiency=0.75, html=False):
    """Estimate wort gravity.

    Parameters
    ----------
    mash : dict
      For each grain/adjunct as a key, provide the number of pounds in
      the mash or a tuple of pounds and the gravity points per pound
      per gallon.  The extraction from grains/adjuncts added in the
      mash will be reduced by `efficiency`.  For example:

        wort({'American 2-row': 10, 'Other Munich': (2, 34)}, ...

    kettle : dict
      Same as `mash` but assumes 100% extraction efficiency.
      Typically for kettle sugars.
    volume : float
      Number of gallons collected from the mash, or post boil volume.
    efficiency : float
      The efficiency of the mash and lauter.
    html : bool
      True to print HTML-formatted table.

    """

    from .util import tab2txt

    total_weight = 0
    for name, weight, ppg in grain_generator(dict(mash, **kettle)):
        total_weight += weight

    tab = []
    for name, weight, ppg in grain_generator(mash):
        ex = weight * ppg * efficiency
        tab.append([name, weight, weight / total_weight, ppg, ex])

    for name, weight, pgg in grain_generator(kettle):
        ex = weight * ppg
        tab.append([grain, weight, weight / total_weight, ppg, ex])


    colnames = ['Grain/Adjunct', 'Weight', 'Grist Fraction', 'PPG', 'Extract']
    colformats = ['{}', '{:.3f}', '{:.0%}', '{:d}', '{:.2f}']

    sg = sum([row[-1] for row in tab]) / volume / 1000 + 1
    footer = ['Volume: {:.1f} gal'.format(volume),
              'Efficiency: {:.0%}'.format(efficiency),
              'Specific gravity: {:.3f}'.format(sg)]
    footer = ', '.join(footer)

    print(tab2txt(tab, colnames, footer, colformats=colformats, html=html))

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

def schedule(r, weight, T_grain, T_mash, T_water=200., r_final=3.2):
    """Water temperature and volume schedule for mashing.

    Parameters
    ----------
    r : float
      Ratio of water volume to grain weight. [qt/lb]
    weight : float
      The grain weight. [lbs]
    T_grain : float
      The grain temperature. [F]
    T_mash : float or list
      The mash temperature.  May be a list of temperatures for step
      infusions. [F]
    T_water : float, optional
      Infusion water temperature. [F]
    r_final : float, optional
      Final ratio of water volume to grain weight.  [qt/lb]

    """
    if isinstance(T_mash, (tuple, list)):
        T_mash = list(T_mash)
    else:
        T_mash = [T_mash]

    T = T_mash.pop(0)
    Ts = strike_water(r, T_grain, T)
    v_total = r * weight
    print()
    print("    [{:.0f} F] Strike water:   {:.0f} F, {:.1f} gal".format(
        T, Ts, v_total / 4))

    for i in range(len(T_mash)):
        v = infusion_volume(v_total, weight, T, T_mash[i])
        v_total += v
        T = T_mash[i]
        print("    [{:.0f} F] Water infusion: {:.1f} qt at {:.0f}".format(
            T_mash[i], v, T_water))

    print()
    print("    Total mash water: {:.1f} gal, {:.1f} qt/lb".format(
        v_total / 4., v_total / weight))
    print("    Sparge with {:.1f} gal of water.".format(
        (r_final * weight - v_total) / 4.))

