============
brew
============

A library for homebrewing.

Requires: python3 (3.4+ recommended).


Caution
=======

I hope you find brew useful, but use at your own risk.  If you
encounter errors, your feedback would be appreciated.


Examples
========

Estimate wort gravity based on a grist of 10 lbs 2-row, 2 lbs Munich,
and a post-boil gravity of 5.5 gal.

>>> brew.mash.wort({'American 2-row': 10, 'German Munich': 2}, {}, 5.5)

  ==============  ======  ===============  ===  =======  ================
  Grain/Adjunct   Weight  Weight Fraction  PPG  Extract  Extract Fraction
  ==============  ======  ===============  ===  =======  ================
  American 2-row  10.000  83.3%            37   277.5    83.3%           
  German Munich   2.000   16.7%            37   55.5     16.7%           
  ==============  ======  ===============  ===  =======  ================
  
  Volume: 5.5 gal
  Efficiency: 75%
  Specific gravity: 1.061


Hop schedule and total IBU estimate from 7.3% alpha Cascade pellets, 1
ounce added at 60, 10, and 0 minutes left in the boil.  Initial boil
gravity is 1.055, final volume is 5.5 gal.

>>> brew.hops.schedule(1.055, 5.5, {'Cascade': (7.3, [1, 1, 1], [60, 10, 0])})

  =======  =====  ======  ====  ===========  ==========
  Hop      Alpha  Weight  Time  Utilization  Bitterness
  =======  =====  ======  ====  ===========  ==========
  Cascade  7.3    1.0     60    22.1         22        
  Cascade  7.3    1.0     10    8.0          8         
  Cascade  7.3    1.0     0     0.0          0         
  =======  =====  ======  ====  ===========  ==========
  
  Boil specific gravity: 1.055
  Volume: 5.5 gal
  Pellets
  Total bitterness: 30 IBU

Brew a saison.
>>> brew.Brew(mash={'German pilsner': 8.5, 'American rye malt': 1.5, 'wheat, flaked': 1}, hops={'Belma': (10.8, 0.7, 60), 'French Strisselspalt': (1.2, 1.0, 10)}, yeast='WLP566', T_sacc=[146, 170])

  =================  ======  ===============  ===  =======  ================
  Grain/Adjunct      Weight  Weight Fraction  PPG  Extract  Extract Fraction
  =================  ======  ===============  ===  =======  ================
  German pilsner     8.500   77.3%            37   235.9    78.3%           
  American rye malt  1.500   13.6%            36   40.5     13.4%           
  wheat, flaked      1.000   9.1%             33   24.8     8.2%            
  =================  ======  ===============  ===  =======  ================
  
  Volume: 5.5 gal
  Efficiency: 75%
  Specific gravity: 1.055
  
  
  ==========  ===========  ============
  T mash (F)  T water (F)  Volume (gal)
  ==========  ===========  ============
  146         158          3.85        
  170         200          1.96        
  ==========  ===========  ============
  
  Total mash water: 5.8 gal (2.1 qt/lb)
  Sparge with 2.9 gal of water
  
  
  ====================  =====  ======  ====  ===========  ==========
  Hop                   Alpha  Weight  Time  Utilization  Bitterness
  ====================  =====  ======  ====  ===========  ==========
  Belma                 10.8   0.7     60    23.3         24        
  French Strisselspalt  1.2    1.0     10    8.4          1         
  ====================  =====  ======  ====  ===========  ==========
  
  Boil specific gravity: 1.049
  Volume: 5.5 gal
  Pellets
  Total bitterness: 25 IBU
  
  
  Fermentation with WLP566 / Belgian Saison II
  Apparent attenutation: 88%
  Final gravity: 1.007
  ABV: 6.3%
  Calories: 184
  Carbohydrates: 14.2 g

