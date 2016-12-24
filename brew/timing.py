# Licensed under an MIT style license - see LICENSE

"""
timing --- Timing for additions.
================================

"""

class Timing:
    def __init__(self):
        self.time = 'N/A'

    def __repr__(self):
        return "<Timing: {}>".format(name)

    def __str__(self):
        return self.name

class Mash(Timing):
    """Mash additions."""
    name = 'Mash'

class Vorlauf(Timing):
    """Vorlauf additions, typically dark malts."""
    name = 'Vorlauf'

class FirstWort(Timing):
    """First wort additions, typically hops."""
    name = 'First wort'

class Boil(Timing):
    """Boil additions.

    Parameters
    ----------
    time : float
      Minutes left in the boil.
      
    """
    
    name = 'Boil'

    def __init__(self, time):
        assert isinstance(time, (float, int))
        self.time = int(time)

    def __str__(self):
        return "{} for {} minutes".format(self.name, self.time)

class HopStand(Timing):
    """Hop stands.

    Parameters
    ----------
    time : float
      Minutes of steeping.

    """

    name = 'Hop stand'

    def __init__(self, time):
        assert isinstance(time, (float, int))
        self.time = time

    def __str__(self):
        return "{} minute {}".format(self.time, self.name)

class Primary(Timing):
    """Additions in the primary."""
    name = 'Primary'

class Secondary(Timing):
    """Additions in the seconary.

    Parameters
    ----------
    time : float, optional
      Days of steeping, especially for hop additions.

    """

    name = 'Secondary'

    def __init__(self, time=None):
        if time is None:
            self.time = time
        else:
            assert isinstance(time, (float, int))
            self.time = int(time)

    def __str__(self):
        if self.time is None:
            return "{}".format(self.name)
        else:
            return "{} days in the {}".format(self.time, self.name)

class Packaging(Timing):
    """Additions at packaging."""
    name = 'Packaging'

class Final(Timing):
    """The beer is ready!"""
    name = 'Final'

