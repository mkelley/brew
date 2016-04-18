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

Boil specific gravity: 1.055, Volume: 5.5 gal, Pellets, Total
bitterness: 30 IBU


