# Licensed under an MIT style license - see LICENSE
import brew as b

class TestBrew:
    def test_volume(self):
        ingredients = b.Ingredients([
            b.Fermentable(b.PPG.AmericanTwoRow, 10),
            b.Hop('Cascade', 7.0, 1.0, b.Boil(60)),
            b.Hop('Cascade', 7.0, 0.5, b.Boil(30)),
            b.Hop('Cascade', 7.0, 0.5, b.Boil(10)),
            b.Fruit('Tart Cherry Puree', 1.034, 6, density=1.0,
                    timing=b.Secondary()),
            b.Culture(b.CultureBank.CaliforniaAle)
        ])
        
        brew = b.Brew(ingredients, 5.0, kettle_gap=0.5)
        # End of boil: 5.0 + kettle_gap
        assert brew.volume(b.Boil(0)) == 5.5
        assert brew.volume(b.Final()) == 5.0 + 6 / 8

    def test_infusion(self):
        ingredients = b.Ingredients([
            b.Fermentable(b.PPG.AmericanTwoRow, 10),
            b.Hop('Cascade', 7.0, 1.0, b.Boil(60)),
            b.Hop('Cascade', 7.0, 0.5, b.Boil(30)),
            b.Hop('Cascade', 7.0, 0.5, b.Boil(10)),
            b.Culture(b.CultureBank.CaliforniaAle)
        ])
        
        brew = b.Brew(ingredients, 5.0, r_mash=1.5, T_sacc=150, T_water=200,
                      T_grain=70, mlt_gap=0.25, absorption=0.5, mash_out=True,
                      kettle_gap=0.5, r_boil=1.0, boil_time=60)
        T, v_i, v_s = brew.infusion()

        # Strike water T = 0.2 / 1.5 * (150 - 70) + 150
        assert int(T[0]) == int(160.7)

        # Mash out v = (170 - 150) * (0.2 * 10 + 1.5 * 10) / (200 - 150)
        assert int(v_i[1] * 16) == int(6.8 * 4)  # cups

        # Sparge v = (5.0 + 0.5 + 1.0 + 0.25 + 10 * 0.5 / 4) - 1.5 * 10 / 4 - 6.8 / 4
        assert int(v_s * 16) == int(2.55 * 16)  # cups

    def test_extract(self):
        ingredients = b.Ingredients([
            b.Fermentable(b.PPG.BelgianPilsener, 10),
            b.Hop('Czech Saaz', 3.0, 2.0, b.Boil(60)),
            b.Hop('German Hallertau', 6.0, 0.5, b.Boil(10)),
            b.Fermentable(b.PPG.TableSugar, 1, timing=b.Primary()),
            b.Culture(b.CultureBank.AbbeyAle)
        ])
        
        brew = b.Brew(ingredients, 5.0, efficiency=0.75)

        # 37 * 10 * 0.75
        assert int(sum(brew.extract(b.Lauter()))) == int(277.5)

        # + 46
        assert int(sum(brew.extract(b.Final()))) == int(323.5)

    def test_boil(self):
        ingredients = b.Ingredients([
            b.Fermentable(b.PPG.AmericanTwoRow, 10),
            b.Hop('Cascade', 7.0, 1.0, b.Boil(60)),
            b.Culture(b.CultureBank.CaliforniaAle)
        ])

        brew = b.Brew(ingredients, 5.0, efficiency=0.75, kettle_gap=0.5,
                      r_boil=1.0, boil_time=60)
        wort = brew.boil()

        # util = 1.65 * 0.000125**(1.046 - 1) * (1 - exp(-0.04 * 60)) / 4.15
        # ibu = 0.746 * util * 100 * 1.0 * 7.0 / 5.5
        assert int(wort.bitterness) == int(22.7)

        brew.ingredients[1].whole = True
        wort = brew.boil()
        assert int(wort.bitterness) == int(22.7 * 0.85)
        
