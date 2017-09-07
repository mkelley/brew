# brew 2.0-beta

A library for homebrewing.

Requires: python3 (3.4+ recommended).


## Caution
I hope you find brew useful, but use at your own risk.  If you
encounter errors, your feedback would be appreciated.

## Overview

The `Brew` class holds the recipe and brew day configuration.  It will `mash`, `boil`, and `ferment` your ingredients to make beer.  The ingredients are held in an `Ingredients` class.  Each ingredient, e.g., `Grain`, `Sugar`, `Hop`, `Fruit`, `Unfermentable`, `Spice`, `Culture`, specifies the amount to add, and when to add it (i.e., timing).  The timing can be at any step in the process, e.g., `Mash`, `Vorlauf`, `Boil`, `Hop Stand`, `Secondary`, but some steps do not make sense for some ingredients, and may cause strange results.  See the `Brew` docstring (`help(Brew)`) for definitions of all configurable brew parameters, e.g., mash water to grist ratio (`r_mash`), boil time (`boil_time`), boil-off rate (`r_boil`), or volume left in kettle after racking (`kettle_gap`).

The module is configured via a small text (JSON) file in your home directory.  The file name can be discovered via:
```
>>> import brew.configuration
>>> brew.configuration.config_file
'/home/msk/.config/brew/config.json'
```
The file is split into configuration sections.  The 'default' section is always loaded, additional sections are optionally loaded and override the defaults:
```
$ cat /home/msk/.config/brew/config.json
{
  "default": {
    "r_mash": 2.8,
    "absorption": 0.5,
    "T_grain": 65,
    "T_water": 200,
    "T_rest": [],
    "T_sacc": 152,
    "mash_out": false,
    "efficiency": 0.65,
    "mlt_gap": 0.25,
    "boil_time": 60,
    "r_boil": 1.0,
    "hop_stand": false,
    "kettle_gap": 0.5
  },
  "pre-Aug 2017": {
    "r_mash": 1.4,
    "mash_out": true,
    "efficiency": 0.72
  }
}
```
The result of loading parameter sets can be shown via:
```
>>> brew.configuration.get_config(['pre-Aug 2017'])
{'T_grain': 65,
 'T_rest': [],
 'T_sacc': 152,
 'T_water': 200,
 'absorption': 0.5,
 'boil_time': 60,
 'efficiency': 0.72,
 'hop_stand': False,
 'kettle_gap': 0.5,
 'mash_out': True,
 'mlt_gap': 0.25,
 'r_boil': 1.0,
 'r_mash': 1.4}
```

## Examples
### Step-by-step

#### Mash

Estimate wort gravity based on a grist of 10 lbs 2-row, 2 lbs Munich, and 5.0 gal in the primary.

```
>>> brew = Brew(Ingredients([Grain(PPG.AmericanTwoRow, 10), Grain(PPG.GermanMunich, 2)]), 5.5)
>>> wort = brew.mash()

==============  ======  ======  ===============  ===  =======  ================
Grain/Adjunct   Timing  Weight  Weight Fraction  PPG  Extract  Extract Fraction
==============  ======  ======  ===============  ===  =======  ================
American 2-row  Mash    10.000  83.3%            37   240.5    83.3%           
German Munich   Mash    2.000   16.7%            37   48.1     16.7%           
==============  ======  ======  ===============  ===  =======  ================
  
Kettle volume: 7.0 gal
Efficiency: 65%
Pre-boil specific gravity: 1.041
  

==========  ===========  ============
T mash (F)  T water (F)  Volume (gal)
==========  ===========  ============
152         158          8.40        
==========  ===========  ============
  
Total mash water: 8.4 gal (2.8 qt/lb)
Sparge with 0.4 gal of water
Collect 7.0 gal of wort
```

#### Boil

Hop schedule and total IBU estimate from 7.3% alpha Cascade pellets, 1
ounce added at 60, 10, and 0 minutes left in the boil.

```
>>> brew.ingredients.extend([Hop('Cascade', 7.3, 1, Boil(60)), Hop('Cascade', 7.3, 1, Boil(10)), Hop('Cascade', 7.3, 1, Boil(0))])
>>> print(brew.ingredients)
Ingredients:
  [0] American 2-row (37 PPG), 10.00 lbs at Mash
  [1] German Munich (37 PPG), 2.00 lbs at Mash
  [2] Cascade (7.3% α), 1.00 oz at Boil for 60 minutes
  [3] Cascade (7.3% α), 1.00 oz at Boil for 10 minutes
  [4] Cascade (7.3% α), 1.00 oz at Boil for 0 minutes

>>> wort = brew.boil(wort)
=======  =======  =====  ======  ===================  ===========  ==========
Hop      Type     Alpha  Weight  Time                 Utilization  Bitterness
=======  =======  =====  ======  ===================  ===========  ==========
Cascade  Pellets  7.3    1.0     Boil for 60 minutes  25.0         23        
Cascade  Pellets  7.3    1.0     Boil for 10 minutes  9.0          8         
Cascade  Pellets  7.3    1.0     Boil for 0 minutes   0.0          0         
=======  =======  =====  ======  ===================  ===========  ==========

Pre-boil: 7.0 gal at 1.041
Post-boil: 6.0 gal at 1.048, 31 IBU
```

#### Ferment

```
>>> brew.ingredients.append(Culture(CultureBank.CaliforniaAle))
>>> print(brew.ingredients)
Ingredients:
  [0] American 2-row (37 PPG), 10.00 lbs at Mash
  [1] German Munich (37 PPG), 2.00 lbs at Mash
  [2] Cascade (7.3% α), 1.00 oz at Boil for 60 minutes
  [3] Cascade (7.3% α), 1.00 oz at Boil for 10 minutes
  [4] Cascade (7.3% α), 1.00 oz at Boil for 0 minutes
  [5] WLP001, California Ale, 1 at Primary

>>> brew.ferment(wort)
Starting gravity: 1.048
Final gravity: 1.011
Bitterness: 31 IBU
Apparent attenutation: 77%
ABV: 4.8%
Calories: 164
Carbohydrates: 16.5 g

```

### Brew a saison

```
>>> ingredients = Ingredients([Grain(PPG.GermanPilsner, 8.5), Grain(PPG.AmericanRyeMalt, 1.5), Grain(PPG.WheatFlaked, 1), Hop('Belma', 10.8, 0.7, Boil(60)), Hop('French Strisselspalt', 1.2, 1.0, Boil(10)), Culture(CultureBank.BelgianSaisonII)])
>>> brew = Brew(ingredients, 5.0, parameter_sets='pre-Aug 2017', T_sacc=[146], efficiency=0.75)
>>> print(brew.ingredients)
Ingredients:
  [0] German pilsner (37 PPG), 8.50 lbs at Mash
  [1] American rye malt (36 PPG), 1.50 lbs at Mash
  [2] Wheat, flaked (33 PPG), 1.00 lb at Mash
  [3] Belma (10.8% α), 0.70 oz at Boil for 60 minutes
  [4] French Strisselspalt (1.2% α), 1.00 oz at Boil for 10 minutes
  [5] WLP566, Belgian Saison II, 1 at Primary

>>> brew.ferment()
=================  ======  ======  ===============  ===  =======  ================
Grain/Adjunct      Timing  Weight  Weight Fraction  PPG  Extract  Extract Fraction
=================  ======  ======  ===============  ===  =======  ================
German pilsner     Mash    8.500   77.3%            37   235.9    78.3%           
American rye malt  Mash    1.500   13.6%            36   40.5     13.4%           
Wheat, flaked      Mash    1.000   9.1%             33   24.8     8.2%            
=================  ======  ======  ===============  ===  =======  ================

Kettle volume: 6.5 gal
Efficiency: 75%
Pre-boil specific gravity: 1.046



==========  ===========  ============
T mash (F)  T water (F)  Volume (gal)
==========  ===========  ============
146         158          3.85        
170         200          1.96        
==========  ===========  ============

Total mash water: 5.8 gal (2.1 qt/lb)
Sparge with 2.3 gal of water
Collect 6.5 gal of wort



====================  =======  =====  ======  ===================  ===========  ==========
Hop                   Type     Alpha  Weight  Time                 Utilization  Bitterness
====================  =======  =====  ======  ===================  ===========  ==========
Belma                 Pellets  10.8   0.7     Boil for 60 minutes  23.8         24        
French Strisselspalt  Pellets  1.2    1.0     Boil for 10 minutes  8.6          1         
====================  =======  =====  ======  ===================  ===========  ==========

Pre-boil: 6.5 gal at 1.046
Post-boil: 5.5 gal at 1.055, 26 IBU


Starting gravity: 1.055
Final gravity: 1.007
Bitterness: 26 IBU
Apparent attenutation: 87%
ABV: 6.3%
Calories: 184
Carbohydrates: 14.2 g
```

### Brew a spiced mild
```
>>> ingredients = Ingredients([
    Grain(PPG.MarisOtter, 6.5),
    Grain(PPG.OatsFlaked, 1),
    Grain(PPG.EnglishCrystal60_70, 0.5),
    Grain(PPG.Black, 0.5, name='Carafa II'),
    Hop('UK Target', 10, 0.25, Boil(60)),
    Hop('UK Target', 10, 0.125, Boil(20)),
    Spice('Cinnamon', '6 sticks', Packaging()),
    Spice('Allspice, whole (ground)', '1 tablespoon', Packaging()),
    Spice('Nutmeg, whole (ground)', '1 tablespoon', Packaging()),
    Spice('Cloves, whole (ground)', '2 teaspoons', Packaging()),
    Spice('Ginger, dried, ground', '1/2 tablespoon', Packaging()),
    Spice('Tincture of orange zest', 'from 2 Valencia oranges extracted with 2 oz vodka', Packaging()),
    Water('Filtered WSSC tap', 0, Unspecified()),
    Priming('Table sugar', '2.1 oz', Packaging()),
    Culture(CultureBank.DryEnglishAle)
])
>>> brew = Brew(ingredients, 5.0, efficiency=0.64, T_sacc=[154])
>>> brew.ferment()
=====================  ======  ======  ===============  ===  =======  ================
Grain/Adjunct          Timing  Weight  Weight Fraction  PPG  Extract  Extract Fraction
=====================  ======  ======  ===============  ===  =======  ================
Maris Otter            Mash    6.500   76.5%            38   158.1    79.8%           
Oats, flaked           Mash    1.000   11.8%            33   21.1     10.7%           
English crystal 60-70  Mash    0.500   5.9%             34   10.9     5.5%            
Carafa II              Mash    0.500   5.9%             25   8.0      4.0%            
=====================  ======  ======  ===============  ===  =======  ================

Kettle volume: 6.5 gal
Efficiency: 64%
Pre-boil specific gravity: 1.030



==========  ===========  ============
T mash (F)  T water (F)  Volume (gal)
==========  ===========  ============
154         160          5.95        
==========  ===========  ============

Total mash water: 5.9 gal (2.8 qt/lb)
Sparge with 1.9 gal of water
Collect 6.5 gal of wort



=========  =======  =====  ======  ===================  ===========  ==========
Hop        Type     Alpha  Weight  Time                 Utilization  Bitterness
=========  =======  =====  ======  ===================  ===========  ==========
UK Target  Pellets  10.0   0.2     Boil for 60 minutes  27.5         9         
UK Target  Pellets  10.0   0.1     Boil for 20 minutes  16.6         3         
=========  =======  =====  ======  ===================  ===========  ==========

Pre-boil: 6.5 gal at 1.030
Post-boil: 5.5 gal at 1.036, 12 IBU


Starting gravity: 1.036
Final gravity: 1.010
Bitterness: 12 IBU
Apparent attenutation: 73%
ABV: 3.4%
Calories: 123
Carbohydrates: 13.3 g
```
