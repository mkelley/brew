# Licensed under an MIT style license - see LICENSE

"""
brew --- Homebrew recipe calculator.
====================================

"""

class Brew(object):
    """Homebrew recipe calculator.

    Parameters
    ----------
    volume : float, optional
      Target volume in gallons.
    mash : dict, optional
      
    kettle : dict, optional
      Same as mash, but for sugars added to the kettle.  Assumes 100%
      efficiency.
    r : float, optional
      Ratio of water volume to grain weight. [qt/lb]
    T_rest : float or list, optional
       Initial (pre-saccharification) rest temperature(s).
    T_sacc : float or list, optional
      Saccharification rest temperature(s).
    hops : dict, optional

    yeast : string or tuple, optional
      

    **kwargs
      Any `wort`, `hops.schedule`, or `mash.schedule` keywords.

    """

    def __init__(self, volume=5.5, mash={'American 2-row': 10},
                 kettle={}, r=1.4, T_rest=[], T_sacc=[150, 170], t_boil=60,
                 r_boil=1.3, hops={'Cascade': (7, 1.0, 60)},
                 yeast='WLP001', **kwargs):

        self.volume = volume
        self.mash = {'American 2-row': 10} if mash is None else mash
        self.kettle = kettle

        self.r = r
        self.T_mash = T_rest if isinstance(T_rest, (list, tuple)) else [T_rest]
        self.T_sacc = T_sacc if isinstance(T_sacc, (list, tuple)) else [T_sacc]
        self.T_mash.extend(self.T_sacc)

        self.t_boil = t_boil
        self.r_boil = r_boil

        self.hops = hops

        self.yeast = yeast

        self.kwargs = kwargs
        
        self.brew()

    def __repr__(self):
        return self.brew()

    @property
    def weight(self):
        w = 0
        if len(self.mash) == 0:
            return w

        for v in self.mash.values():
            w += v[0] if isinstance(v, (list, tuple)) else v

        return w

    @property
    def yeast(self):
        return self._yeast

    @yeast.setter
    def yeast(self, y):
        from . import fermentation
        self._yeast = fermentation.yeast(y)

    def brew(self, **kwargs):
        from . import mash
        from . import hops
        from . import fermentation

        self.kwargs.update(kwargs)

        sg, tab = mash.wort(self.mash, self.kettle, self.volume, **self.kwargs)
        outs = tab
        v_mash, T_infusions, tab = mash.infusion(
            self.r, self.weight, self.volume, self.T_mash,
            t_boil=self.t_boil, r_boil=self.r_boil,
            **self.kwargs)
        outs += tab

        # Use volume half way through boil to estimate boil specific
        # gravity
        v = self.volume + self.t_boil / 60.0 * self.r_boil / 2
        boil_sg = (sg - 1) * self.volume / v + 1

        util, bit, tab = hops.schedule(boil_sg, self.volume, self.hops,
                                       **self.kwargs)
        outs += tab

        grain_sg = mash.wort(self.mash, {}, self.volume, **self.kwargs)[0]
        fg, app_atten = fermentation.final_gravity(grain_sg, self.T_sacc[0],
                                                   self.yeast)
        cal = fermentation.calories(sg, fg)
        carbs = fermentation.carbohydrates(sg, fg)
        outs += '''
Fermentation with {}
Apparent attenutation: {:.0f}%
Final gravity: {:.3f}
ABV: {:.1f}%
Calories: {:.0f}
Carbohydrates: {:.1f} g
'''.format(self.yeast[0], app_atten, fg, fermentation.abv(sg, fg), cal, carbs)

        return outs
