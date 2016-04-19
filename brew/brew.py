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

        self.yeast = yeast

        self.kwargs = kwargs
        
        self.brew()

    def __repr__(self):
        self.brew()

    @property
    def weight(self):
        w = 0
        if len(self.mash) == 0:
            return w

        for v in self.mash.values():
            w += v[0] if isinstance(v, (list, tuple)) else v

        return w

    def brew(self):
        from . import mash
        from . import hops
        from . import fermentation

        sg = mash.wort(self.mash, self.kettle, self.volume, **self.kwargs)
        mash.schedule(self.r, self.weight, self.volume, self.T_mash,
                      t_boil=self.t_boil, r_boil=self.r_boil, **self.kwargs)

        # Use volume half way through boil to estimate boil specific
        # gravity
        v = self.volume + self.t_boil / 60.0 * self.r_boil / 2
        boil_sg = (sg - 1) * self.volume / v + 1

        hops.schedule(boil_sg, self.volume, self.hops, **self.kwargs)

        product, name, atten = fermentation.find_yeast(self.yeast)
        grain_sg = mash.wort(self.mash, {}, self.volume, **self.kwargs)
        fg, app_atten = fermentation.final_gravity(grain_sg, self.T_mash[0],
                                                   self.yeast)
        print('Fermentation with {} / {}'.format(product, name))
        print('Apparent attenutation: {:.0f}%'.format(app_atten))
        print('Final gravity: {:.3f}'.format(fg))
