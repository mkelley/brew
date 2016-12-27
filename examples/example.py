from brew import *
from brew.timing import Boil

wort = Wort([Fermentable(PPG.AmericanTwoRow, 10),
             Hop('Cascade', 7.0, 1.0, Boil(60)),
             Hop('Cascade', 7.0, 0.5, Boil(30)),
             Hop('Cascade', 7.0, 0.5, Boil(10))
             ])
yeast = Culture(CultureBank.CaliforniaAle)
brew = Brew(wort, yeast)
beer = brew.brew()

brew.wort.append(Fruit('Mango puree', 11, 2))
beer = brew.brew()
