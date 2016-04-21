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
    T_mash : float or list, optional
      Mash temperature(s).
    hops : dict, optional

    yeast : string or tuple, optional
      

    **kwargs
      Any `wort`, `hops.schedule`, or `mash.schedule` keywords.

    """

    def __init__(self, volume=5.5, mash={'American 2-row': 10},
                 kettle={}, r=1.4, T_mash=[150, 170], t_boil=60,
                 r_boil=1.3, hops={'Cascade': (7, 1.0, 60)},
                 yeast='WLP001', **kwargs):

        self.volume = volume
        self.mash = {'American 2-row': 10} if mash is None else mash
        self.kettle = kettle

        self.r = r
        self.T_mash = T_mash

        self.t_boil = t_boil
        self.r_boil = r_boil

        self.hops = hops

        self._yeast = yeast

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

        if isinstance(y, str):
            product, name, atten = fermentation.find_yeast(self.yeast)
            '{} / {}'.format(product, name)
            self._yeast = name, atten
        elif isinstance(y, (tuple, list)):
            assert isinstance(y[0], str)
            assert isintance(y[1], (float, int))
            assert isintance(y[2], (float, int))
            self._yeast = y
        else:
            raise TypeError('yeast must be a product key (e.g., "WLP001") or a 3-element tuple with the name, minimum, and maximum apparent attenutations (%).')

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
        fg, app_atten = fermentation.final_gravity(grain_sg, self.T_mash[0],
                                                   self.yeast)
        outs += '''
Fermentation with {}
Apparent attenutation: {:.0f}%
Final gravity: {:.3f}
'''.format(self.yeast[0], app_atten, fg)

        return outs
