# Licensed under an MIT style license - see LICENSE

"""
configuration --- Brew calculator parameters.
=============================================

"""

import os
from collections import OrderedDict
import json

config_file = os.sep.join([os.path.expanduser('~'), '.config',
                           'brew', 'config.json'])

# defaults for empty configuration file
config_default = OrderedDict(
    (('r_mash', 2.8),
     ('absorption', 0.5),
     ('T_grain', 65),
     ('T_water', 200),
     ('T_rest', []),
     ('T_sacc', 152),
     ('mash_out', False),
     ('efficiency', 0.65),
     ('mlt_gap', 0.25),
     ('boil_time', 60),
     ('r_boil', 1.0),
     ('hop_stand', False),
     ('kettle_gap', 0.5),
    )
)

def get_config(parameter_sets=['default']):
    """Read parameters from the configuration file.

    Parameters
    ----------
    parameter_sets : list of strings, optional
      Load these parameter sets, in order.

    Returns
    -------
    config : dict

    """

    global config_file, config_default

    config = OrderedDict()
    if not os.path.exists(config_file):
        directory = os.path.dirname(config_file)
        if not os.path.exists(directory):
            directories = directory.split(os.path.sep)
            for i in range(len(directories)):
                d = os.path.sep.join(directories[:(i+1)])
                if d == '':
                    continue

                try:
                    os.mkdir(d)
                except FileExistsError:
                    pass
            
        config['default'] = config_default
        with open(config_file, 'w') as outf:
            json.dump(config, outf, indent=2)
    else:
        with open(config_file, 'r') as inf:
            config = json.load(inf)

    c = {}
    for s in parameter_sets:
        c.update(config[s])

    return c
