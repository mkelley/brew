from brew import *
from brew.timing import Boil, HopStand, Secondary

print('=' * 80)
wort = Wort([Fermentable(PPG.AmericanTwoRow, 4.5),
             Fermentable(PPG.WheatMalt, 4.125, name='White wheat malt'),
             Fermentable(PPG.AmericanCaramel20, 6 / 16, name='Caramel Vienne malt'),
             Fermentable(PPG.AcidMalt, 2.5 / 16, name='White wheat malt'),
             Hop('Magnum', 11.5, 0.6, Boil(60)),
             Hop('Amarillo', 8.5, 0.3, HopStand(30)),
             Hop('Citra', 13.4, 0.7, HopStand(30)),
             Hop('Amarillo', 8.5, 1.0, Secondary(7)),
             Hop('Citra', 13.4, 3.5, Secondary(7)),
             ])
yeast = Culture(CultureBank.CaliforniaAle)
brew = Brew(wort, yeast)
beer = brew.brew()
brew.summary()
beer.summary()

wort = Wort([Fermentable(PPG.AmericanTwoRow, 4.5),
             Fermentable(PPG.WheatMalt, 4.125, name='White wheat malt'),
             Fermentable(PPG.AmericanCaramel20, 6 / 16, name='Caramel Vienne malt'),
             Fermentable(PPG.AcidMalt, 2.5 / 16, name='White wheat malt'),
             Hop('Magnum', 11.5, 0.7, Boil(60)),
             Hop('Amarillo', 8.5, 1.3, HopStand(30)),
             Hop('Citra', 13.4, 0.8, HopStand(30)),
             Hop('Amarillo', 8.5, 0.7, Secondary(7)),
             Hop('Citra', 13.4, 3.5, Secondary(7)),
             ], volume=5.75, boil_time=70, efficiency=0.76)
yeast = Culture(CultureBank.CaliforniaAle)
brew = Brew(wort, yeast)
beer = brew.brew()
brew.summary()
beer.summary()
