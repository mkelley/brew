# Licensed under an MIT style license - see LICENSE

"""
brew --- A homebrew calculator.
===============================

"""

from . import ingredients
from . import timing
from . import brew
from . import util

from .brew import *
from .ingredients import *
from .timing import *

_default_format = 'text'  # default format for tables

def set_format(format):
    """Set the default format for summary output.

    Parameters
    ----------
    format : string
      'text', 'html', 'notebook'

    """
    global _default_format
    assert format in ['text', 'html', 'notebook']
    _default_format = format
