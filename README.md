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

Mash
----

Estimate wort gravity based on a grist of 10 lbs 2-row, 2 lbs Munich,
and a post-boil gravity of 5.5 gal.

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

Boil
----

Hop schedule and total IBU estimate from 7.3% alpha Cascade pellets, 1
ounce added at 60, 10, and 0 minutes left in the boil.

```python
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

Ferment
-------

```python
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

