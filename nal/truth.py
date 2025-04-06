__all__ = ['TruthValue']

# from .TruthValueFunctions import *
from .UncertaintyMappingFunctions import *
from math import exp, log


class TruthValue:
    ts_update = 0
    def __init__(self, f, c, k=1.0, eternal=False) -> None:
        self.f: float = f
        self.c: float = c
        self.k: float = k
        if eternal:
            self.ts_update = None


    # def revise(self, other: 'TruthValue'):
    #     truth1 = self
    #     truth2 = other
    #     w_p_1 = fc_to_w_plus(truth1.f, truth1.c, truth1.k)
    #     w_p_2 = fc_to_w_plus(truth2.f, truth2.c, truth2.k)
    #     w_m_1 = fc_to_w_minus(truth1.f, truth1.c, truth1.k)
    #     w_m_2 = fc_to_w_minus(truth2.f, truth2.c, truth2.k)
    #     w_p, w_m = w_p_1 + w_p_2, w_m_1 + w_m_2
    #     self.set_w(w_p, w_p+w_m)

    def revise_fc(self, f, c, k=None):
        if k is None:
            k = self.k
        w_p_1 = fc_to_w_plus(self.f, self.c, self.k)
        w_p_2 = fc_to_w_plus(f, c, k)
        w_m_1 = fc_to_w_minus(self.f, self.c, self.k)
        w_m_2 = fc_to_w_minus(f, c, k)
        w_p, w_m = w_p_1 + w_p_2, w_m_1 + w_m_2
        self.set_w(w_p, w_p+w_m)

    def to_w(self):
        f, c, k = self.f, self.c, self.k
        return fc_to_w_plus(f, c, k), fc_to_w_minus(f, c, k)    
    
    def revise_w(self, w_p, w, ts_now=None, duration=20):
        """
        Args:
            a_decay: decay factor. See methods, `Truth.get_decay_factor` and `Truth.decay`, for more information
        """
        # update ts
        self.projection(ts_now, duration)

        w_p1, w_m1 = self.to_w()
        w1 = w_p1 + w_m1
        # revision
        w = w1 + w
        w_p = w_p1 + w_p
        # calculate f, c
        self.f, self.c = w_to_f(w_p, w), w_to_c(w, self.k)

    def revise(self, truth: 'TruthValue', ts_now, duration=20):
        # update ts
        if truth.c == 0: return
        self.projection(ts_now, duration)

        w_p1, w_m1 = self.to_w()
        w_p2, w_m2 = truth.to_w()
        # revision
        w = w_p1 + w_m1 + w_p2 + w_m2
        w_p = w_p1 + w_p2
        # calculate f, c
        self.f, self.c = w_to_f(w_p, w), w_to_c(w, self.k)

    def projection(self, ts_now=None, duration=20):
        if ts_now is not None:
            if self.ts_update is not None:
                if self.ts_update < ts_now:
                    dt = ts_now - self.ts_update
                    self.decay(self.get_decay_factor(duration), dt)
                self.ts_update = ts_now
        
    def update(self, f, c, k, ts_update):
        self.f, self.c, self.k, self.ts_update = f, c, k, ts_update

    def reset(self, f, c):
        self.f, self.c = f, c
    
    def set_w(self, w_plus, w):
        self.f, self.c = (w_to_f(w_plus, w), w_to_c(w, self.k)) if w != 0 else (0.5, 0.0)

    def set_fc(self, f, c):
        self.f, self.c = f, c

    @staticmethod
    def from_w(w_plus, w, k):
        f, c = (w_to_f(w_plus, w), w_to_c(w, k)) if w != 0 else (0.5, 0.0)
        return TruthValue(f, c, k)
    
    @property
    def e(self):
        return (self.c * (self.f - 0.5) + 0.5)

    def __repr__(self):
        return f"%{self.f:.2f};{self.c:.2f} (k={self.k:.2f})%"
    
    def __str__(self):
        return f"({self.f:.2f};{self.c:.2f})"
        

    @staticmethod
    def get_decay_factor(half_life_period: float):
        return -1/half_life_period*log(0.5)

    def decay(self, alpha: float, ts_now: float) -> None:
        """
        decay confidence by
        c' = c*exp(-alpha*dt)
        The smaller the alpha is, the slower the decay
        
        half-life period
        |  dt  |    alpha   |
        | ---- | ---------- |
        |    1 | 0.69314718 |
        |    2 | 0.34657359 |
        |    4 | 0.17328680 |
        |    8 | 0.08664340 |
        |   16 | 0.04332170 |
        |   32 | 0.02166085 |
        |   64 | 0.01083042 |
        |  128 | 0.00541521 |
        |  256 | 0.00270761 |
        |  512 | 0.00135380 |
        | 1024 | 0.00067690 |
        """
        if ts_now > self.ts_update:
            dt = ts_now - self.ts_update
            self.ts_update = ts_now
            self.c = self.c*exp(-alpha*dt)
