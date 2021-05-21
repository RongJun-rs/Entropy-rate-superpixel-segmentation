import numpy as np
import pdb,heapq
import collections
from utils.decorator import debugit
from utils import utils
try:
    from . import edge_extended_info
    from .. import lbdaComputer
except:
    from heapManager import edge_extended_info
    import lbdaComputer

class HeapInitializer:
    lbda = lbdaComputer.LbdaComputer().lbda
    def __init__(self,edges_with_nodes):
        self.edges_with_nodes = edges_with_nodes

        self.nodei = self.edges_with_nodes[:, 0]
        self.nodej = self.edges_with_nodes[:, 1]
        self.edges = self.edges_with_nodes[:,2]

        self.wij = [el["weight"] for el in self.edges]


        self.gainH = self.init_gain_H()
        self.gainB = self.init_gain_B()
        self.gain = self.gainH + self.lbda * self.gainB

        #self.edges_with_nodes_and_gain = np.hstack([self.edges_with_nodes,-self.gain.reshape(-1,1)])
        gen = zip(self.edges_with_nodes,self.gain)
        #self.edges_with_nodes_and_gainAsNamedTuple = [edge_extended_info.EdgesExtendedInfo(nodei,nodej,wij,gain) for ((nodei ,nodej ,wij),gain) in gen]
        self.edges_with_nodes_and_gainAsNamedTuple = [edge_extended_info.EdgesExtendedInfo(nodei,nodej,edge,gain) for ((nodei ,nodej ,edge),gain) in gen]
        self.heapMin = self.createBinaryMaxHeap()

    @staticmethod
    def partial_entropy(value):
        res = np.zeros_like(value)
        res[value>0] = (-value * np.log(value)) [value>0]
        return res
    def init_gain_H(self):
        """
        compute the difference in cost by adding the edge linking nodei and nodej, for the function H
        , in other words H(A U {edge}) - H(A), where A is the constructed graph so far
        (not declared are this level)
        """




        self.mui = np.array([el.mu for el in self.nodei])
        self.muj = np.array([el.mu for el in self.nodej])

        wi = np.array([el.w for el in self.nodei])
        wj = np.array([el.w for el in self.nodej])

        self.pij = self.wij / wi # pij*ui is equal to pji*self.muj
        self.pji = self.wij / wj

        self.pji = self.pji.astype("float32")
        self.pij = self.pij.astype("float32")


        self.pii_new = 1.0 - self.pij
        self.pjj_new = 1.0 - self.pji

        part1 = self.mui * self.partial_entropy(self.pij) + self.muj * self.partial_entropy(self.pji)
        part2 = self.mui * self.partial_entropy(self.pii_new)
        part3 = self.muj * self.partial_entropy(self.pjj_new)
        res = part1 + part2 + part3

        return res

    #from utils.decorator import debugit
    def init_gain_B(self):
        card_V = self.nodei[0].graph.number_of_nodes()

        gain_HA = self.partial_entropy(2/card_V) - 2 * self.partial_entropy(1/card_V)
        gain_NA = -1

        gain = gain_HA - gain_NA
        return float(gain)

    #@debugit
    def createBinaryMaxHeap(self,verbose=True):
        """
        if verbose is True, returns
        :return:
        the_heap ;
        """
        the_heap = []
        heapq.heapify(the_heap)
        #s = self.edges_with_nodes_and_gain
        s = self.edges_with_nodes_and_gainAsNamedTuple
        N = len(s)
        for i, el in enumerate(s):
            heapq.heappush(the_heap, el )
            if i % 1000 == 0 and verbose:
                print(i/N)
        return the_heap