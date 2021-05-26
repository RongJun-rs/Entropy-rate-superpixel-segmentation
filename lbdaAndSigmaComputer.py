from utils import singleton
import numpy as np

class LbdaComputer(metaclass=singleton.SingletonMeta):
    lbdap = 0.5
    def __init__(self,gainH,gainB,K):
        self.gainH = gainH
        self.gainB = gainB
        self.K = K
        self.beta = np.max(self.gainH)/np.max(self.gainB)
        self.lbda = self.compute_lbda()

    def compute_lbda(self):
        lbda = self.lbdap * self.beta * self.K
        return lbda
    def __call__(self):
        return self.lbda


class SigmaReader(metaclass=singleton.SingletonMeta):
    def __init__(self,sigma):
        self.sigma = sigma
    def __call__(self):
        return self.sigma