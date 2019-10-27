# Licensed under an MIT style license - see LICENSE

"""
bbtn --- Brew by the Numbers
============================
Alcohol and extract calculations from Hall (1995).

Hall, Brew by the Numbers, Zymergy, Summer 1995.

"""

__all__ = [
    'abv',
    'abw',
    'calories_alcohol',
    'calories_extract',
    'calories_protein',
    'plato2sg',
    'real_attenutation',
    'real_extract',
    'sg2plato'
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

    oe = sg2plato(og)
    re = real_extract(og, fg)
    return (oe - re) / (2.0665 - 0.010665 * oe)


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


def plato2sg(E):
    """Degrees Plato to specific gravity.

    Parmeters
    ---------
    E : float
      Extract in degrees plato.

    Notes
    -----
    Brew by the Numbers, Hall, Zymurgy, Summer 1995.

    """
    return (((4.3074e-8 * E) + 1.3488e-5) * E + 0.0038661) * E + 1.00001


def real_attenuation(og, fg):
    """Real attenuation (%) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    oe = sg2plato(og)
    re = real_extract(og, fg)
    return (oe - re) / oe * 100.


def real_extract(og, fg):
    """Real extract (degrees Plato) from original and final gravity.

    Brew by the Numbers, Hall, Zymergy, Summer 1995.

    """

    oe = sg2plato(og)
    ae = sg2plato(fg)
    q = 0.22 + 0.001 * oe
    return (q * oe + ae) / (1 + q)


def sg2plato(sg):
    """Extract in degrees Plato.

    Valid for the range 0 to 33° Plato / 1.000 to 1.144.

    Parmeters
    ---------
    sg : float
      Specific gravity.

    Notes
    -----
    Brew by the Numbers, Hall, Zymurgy, Summer 1995.

    """
    return -668.962 + 1262.45 * sg - 776.43 * sg**2 + 182.94 * sg**3
