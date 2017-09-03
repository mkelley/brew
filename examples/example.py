#import brew as b
#from brew import Ingredients, Fermentable, Spice, Fruit, Water, Unspecified, Priming, PPG, Hop, Culture, CultureBank, Boil, Packaging
from brew import *

ingredients = Ingredients([
    Fermentable(PPG.AmericanTwoRow, 10),
    Hop('Cascade', 7.0, 1.0, Boil(60)),
    Hop('Cascade', 7.0, 0.5, Boil(30)),
    Hop('Cascade', 7.0, 0.5, Boil(10)),
    Culture(CultureBank.CaliforniaAle)
])

brew = Brew(ingredients, 5.0)
brew.ferment()

print('-' * 80)
ingredients.append(Fruit('Mango puree', 1.070, 5))
brew = Brew(ingredients, 5.0)
brew.ferment()

print('-' * 80)
ingredients = Ingredients([
    Fermentable(PPG.MarisOtter, 6.5),
    Fermentable(PPG.OatsFlaked, 1),
    Fermentable(PPG.EnglishCrystal60_70, 0.5),
    Fermentable(PPG.Black, 0.5, name='Carafa II'),
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
brew = Brew(ingredients, 5.0, efficiency=0.64, T_sacc=154)
brew.ferment()

