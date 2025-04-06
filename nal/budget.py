from typing import Type
import numpy as np
from math import sqrt, log, exp

class BudgetValue:
    ts_update = 0
    def __init__(self, p=0.8, d=0.99, q=0.0) -> None:
        self.p = float(p) # priority
        self.d = float(d) # durability
        self.q = float(q) # quality

    @staticmethod
    def get_decay_factor(half_life_period: float):
        return -1/half_life_period*log(0.5)
    
    def decay(self, ts_now):
        '''
        half-life period
        |  dt  | 1-durability |
        | ---- | ------------ |
        |    1 |  0.69314718  |
        |    2 |  0.34657359  |
        |    4 |  0.17328680  |
        |    8 |  0.08664340  |
        |   16 |  0.04332170  |
        |   32 |  0.02166085  |
        |   64 |  0.01083042  |
        |  128 |  0.00541521  |
        |  256 |  0.00270761  |
        |  512 |  0.00135380  |
        | 1024 |  0.00067690  |
        '''
        if ts_now > self.ts_update:
            dt = ts_now - self.ts_update
            self.ts_update = ts_now
            Q = 0.3
            q = self.q * Q
            self.p = q + (self.p - q)*exp(-(1-self.d)*dt)
    
    def exhibit_p(self, a: float, stubbornness=0.1):
        '''exhibit the priority of the budget'''
        s = min(1, max(0, stubbornness))
        dp = a*(1-self.p) * (1-(1-self.p)*s)
        self.p += dp
        self.p = min(1.0, self.p)

    def inhibit_p(self, a: float, stubbornness=0.1):
        '''inhibit the priority of the budget'''
        s = min(1, max(0, stubbornness))
        dp = - a*self.p *(1-self.p*s)
        self.p += dp
        self.p = max(0, self.p)

    def __iter__(self):
        '''return (f, c, k)'''
        return iter((self.p, self.d, self.q))

    def __str__(self) -> str:
        return f'${self.p:.3f};{self.d:.3f};{self.q:.3f}$'

    def __repr__(self) -> str:
        return str(self)