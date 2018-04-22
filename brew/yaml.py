# Licensed under an MIT style license - see LICENSE
"""brewlog class definitions for pyyaml"""
import yaml
from . import ingredients
from . import timing

########################################################################
def culture_representer(dumper, item):
    data = {
        'culture': item.culture,
        'quantity': item.quantity,
        'timing': item.timing,
        'desc': item.desc,
    }
    return dumper.represent_mapping('!Culture', data)
def culture_constructor(loader, node):
    data = loader.construct_mapping(node)
    culture = getattr(ingredients.CultureBank, data.pop('culture'))
    if 'name' in data:
        del data['name']
    return ingredients.Culture(culture, **data)
yaml.add_representer(ingredients.Culture, culture_representer)
yaml.add_constructor('!Culture', culture_constructor)

########################################################################
def ppg_representer(dumper, ppg):
    return dumper.represent_scalar('!PPG', ppg.name)
def ppg_constructor(loader, node):
    name = loader.construct_scalar(node)
    return getattr(ingredients.PPG, name)
yaml.add_representer(ingredients.PPG, ppg_representer)
yaml.add_constructor('!PPG', ppg_constructor)

########################################################################
def ingredient_representer(name):
    def rep(dumper, item):
        data = {
            'name': item.name,
            'quantity': item.ppg,
            'timing': item.timing,
            'desc': item.desc,
        }
        return dumper.represent_mapping(name, data)
    return rep
def ingredient_constructor(cls):
    def con(loader, node):
        data = loader.construct_mapping(node)
        name = data.pop('name')
        quantity = data.pop('quantity', '')
        return cls(name, quantity, **data)
    return con
for name in ['Ingredient', 'Spice', 'Other', 'Priming']:
    cls = getattr(ingredients, name)
    yaml.add_representer(cls, ingredient_representer('!' + name))
    yaml.add_constructor('!' + name, ingredient_constructor(cls))

########################################################################
def fermentable_representer(name):
    def rep(dumper, item):
        data = {
            'ppg': item.ppg,
            'weight': item.weight,
            'timing': item.timing,
            'name': item.name,
            'desc': item.desc,
        }
        return dumper.represent_mapping(name, data)
    return rep
def fermentable_constructor(cls):
    def con(loader, node):
        data = loader.construct_mapping(node)
        ppg = data.pop('ppg')
        weight = float(data.pop('weight'))
        return cls(ppg, weight, **data)
    return con
for name in ['Fermentable', 'Grain', 'Sugar', 'Unfermentable']:
    cls = getattr(ingredients, name)
    yaml.add_representer(cls, fermentable_representer('!' + name))
    yaml.add_constructor('!' + name, fermentable_constructor(cls))

########################################################################
def fruit_representer(dumper, item):
    data = {
        'name': item.name,
        'sg': item.sg,
        'weight': item.weight,
        'timing': item.timing,
        'density': item.density,
        'desc': item.desc,
    }
    return dumper.represent_mapping(name, data)
def fruit_constructor(loader, node):
    data = loader.construct_mapping(node)
    name = data.pop('name')
    sg = data.pop('sg')
    weight = data.pop('weight')
    return ingredients.Fruit(name, sg, weight, **data)
yaml.add_representer(ingredients.Fruit, fruit_representer)
yaml.add_constructor('!Fruit', fruit_constructor)

########################################################################
def water_representer(dumper, item):
    data = {
        'name': item.name,
        'volume': item.volume,
        'timing': item.timing,
        'desc': item.desc,
    }
    return dumper.represent_mapping(name, data)
def water_constructor(loader, node):
    data = loader.construct_mapping(node)
    name = data.pop('name')
    return ingredients.Water(name, **data)
yaml.add_representer(ingredients.Water, water_representer)
yaml.add_constructor('!Water', water_constructor)

########################################################################
def timing_representer(name):
    def rep(dumper, timing):
        time = getattr(timing, 'time', None)
        return dumper.represent_scalar(name, time)
    return rep
def timing_constructor(cls):
    def con(loader, node):
        if node.value is '':
            return cls()
        else:
            return cls(float(node.value))
    return con
for name in ['Mash', 'Vorlauf', 'Sparge', 'Lauter', 'FirstWort', 'Boil',
             'HopStand', 'Primary', 'Secondary', 'Packaging', 'Final',
             'Unspecified']:
    cls = getattr(timing, name)
    yaml.add_representer(cls, timing_representer('!' + name))
    yaml.add_constructor('!' + name, timing_constructor(cls))

########################################################################
def hop_representer(dumper, item):
    data = {
        'name': item.name,
        'alpha': item.alpha,
        'beta': item.beta,
        'weight': item.weight,
        'timing': item.timing,
        'whole': item.whole,
        'desc': item.desc,
    }
    return dumper.represent_mapping('!Hop', data)
def hop_constructor(loader, node):
    data = loader.construct_mapping(node)
    name = data.pop('name')
    alpha = float(data.pop('alpha'))
    weight = float(data.pop('weight'))
    return ingredients.Hop(name, alpha, weight, **data)
yaml.add_representer(ingredients.Hop, hop_representer)
yaml.add_constructor('!Hop', hop_constructor)

########################################################################
class GravityMeasurement(yaml.YAMLObject):
    yaml_tag = '!GravityMeasurement'
    def __init__(self, date, gravity, T, note):
        self.date = date
        self.gravity = gravity
        self.T = T
        self.note = note

    def __repr__(self):
        return '{}(date={}, gravity={}, T={}, note={})'.format(
            self.__class__.__name__, self.date, self.gravity, self.T, self.note)

    def cor_grav(self, og):
        return self.gravity

    def ap_atten(self, og):
        return '{:.0f}'.format((og - float(self.cor_grav(og))) / (og - 1) * 100)

    def abv(self, og):
        from .util import abv
        return '{:.1f}'.format(abv(og, float(self.cor_grav(og))))

class Hydrometer(GravityMeasurement):
    yaml_tag = '!Hydrometer'
    def cor_grav(self, og):
        from .util import hydrometer_correct
        return '{:.3f}'.format(hydrometer_correct(self.gravity, self.T))

########################################################################
class Refractometer(GravityMeasurement):
    yaml_tag = '!Refractometer'
    def cor_grav(self, og):
        from .util import refractometer_correct
        return '{:.3f}'.format(refractometer_correct(og, self.gravity))
