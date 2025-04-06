__all__ = ['TruthValue']

# from .TruthValueFunctions import *
from .UncertaintyMappingFunctions import *

class TruthValue:
    def __init__(self, f, c, k=1.0):
        self.f = f
        self.c = c
        self.k = k

    def revise(self, other: 'TruthValue'):
        truth1 = self
        truth2 = other
        w_p_1 = fc_to_w_plus(truth1.f, truth1.c, truth1.k)
        w_p_2 = fc_to_w_plus(truth2.f, truth2.c, truth2.k)
        w_m_1 = fc_to_w_minus(truth1.f, truth1.c, truth1.k)
        w_m_2 = fc_to_w_minus(truth2.f, truth2.c, truth2.k)
        w_p, w_m = w_p_1 + w_p_2, w_m_1 + w_m_2
        self.set_w(w_p, w_p+w_m)

    def revise_fc(self, f, c, k=None):
        if k is None:
            k = self.k
        w_p_1 = fc_to_w_plus(self.f, self.c, self.k)
        w_p_2 = fc_to_w_plus(f, c, k)
        w_m_1 = fc_to_w_minus(self.f, self.c, self.k)
        w_m_2 = fc_to_w_minus(f, c, k)
        w_p, w_m = w_p_1 + w_p_2, w_m_1 + w_m_2
        self.set_w(w_p, w_p+w_m)

    
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
        