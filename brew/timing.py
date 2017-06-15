# Licensed under an MIT style license - see LICENSE

"""
timing --- Timing for additions.
================================

"""

from abc import ABC

class Timing(ABC):
    def __init__(self):
        self.time = 'N/A'

    def __repr__(self):
        return "<Timing: {}>".format(self.name)

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.step < other.step
    
    def __le__(self, other):
        return (self < other) or (self == other)
    
    def __eq__(self, other):
        return self.step == other.step
    
    def __ne__(self, other):
        return not (self == other)
    
    def __gt__(self, other):
        return self.step > other.step
    
    def __ge__(self, other):
        return (self > other) or (self == other)

class Mash(Timing):
    """Mash additions."""
    name = 'Mash'
    step = 1

class Vorlauf(Timing):
    """Vorlauf additions, typically dark malts."""
    name = 'Vorlauf'
    step = 2

class FirstWort(Timing):
    """First wort additions, typically hops.

    Parameters
    ----------
    time : float
      Total boil length in minutes.

    """
    
    name = 'First wort'
    step = 3

    def __init__(self, time):
        assert isinstance(time, (float, int))
        self.time = int(time)
        
    def __str__(self):
        return "{}, {}-minute boil".format(self.name, self.time)

class Boil(Timing):
    """Boil additions.

    Parameters
    ----------
    time : float
      Minutes left in the boil.
      
    """
    
    name = 'Boil'
    step = 4

    def __init__(self, time):
        assert isinstance(time, (float, int))
        self.time = int(time)

    def __str__(self):
        return "{} for {} minutes".format(self.name, self.time)

    def __lt__(self, other):
        if isinstance(other, Boil):
            return self.time > other.time
        else:
            return self.step < other.step
    
    def __eq__(self, other):
        if isinstance(other, Boil):
            return self.time == other.time
        else:
            return self.step == other.step
    
    def __gt__(self, other):
        if isinstance(other, Boil):
            return self.time > other.time
        else:
            return self.step < other.step

class HopStand(Timing):
    """Hop stands.

    Parameters
    ----------
    time : float
      Minutes of steeping.

    """

    name = 'Hop stand'
    step = 5

    def __init__(self, time):
        assert isinstance(time, (float, int))
        self.time = time

    def __str__(self):
        return "{} minute {}".format(self.time, self.name)
    
    def __lt__(self, other):
        if isinstance(other, HopStand):
            return self.time < other.time
        else:
            return self.step < other.step
    
    def __eq__(self, other):
        if isinstance(other, HopStand):
            return self.time == other.time
        else:
            return self.step == other.step
    
    def __gt__(self, other):
        if isinstance(other, HopStand):
            return self.time < other.time
        else:
            return self.step < other.step

class Primary(Timing):
    """Additions in the primary."""
    name = 'Primary'
    step = 6

class Secondary(Timing):
    """Additions in the seconary.

    Parameters
    ----------
    time : float, optional
      Days of steeping, especially for hop additions.

    """

    name = 'Secondary'
    step = 7

    def __init__(self, time=None):
        if time is None:
            self.time = 0
        else:
            assert isinstance(time, (float, int))
            self.time = int(time)

    def __str__(self):
        if self.time == 0:
            return "{}".format(self.name)
        else:
            return "{} days in the {}".format(self.time, self.name)

    def __lt__(self, other):
        if isinstance(other, Secondary):
            return self.time < other.time
        else:
            return self.step < other.step
    
    def __eq__(self, other):
        if isinstance(other, Secondary):
            return self.time == other.time
        else:
            return self.step == other.step
    
    def __gt__(self, other):
        if isinstance(other, Secondary):
            return self.time < other.time
        else:
            return self.step < other.step

class Packaging(Timing):
    """Additions at packaging."""
    name = 'Packaging'
    step = 8

class Final(Timing):
    """The beer is ready!"""
    name = 'Final'
    step = 9

class Unspecified(Timing):
    """No specific time specified."""
    name = 'Not applicable'
    step = -1
