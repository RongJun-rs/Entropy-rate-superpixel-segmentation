import numpy as np
import pdb,heapq
import collections
from utils.decorator import debugit


class EdgesExtendedInfo:
    __slots__ = ["nodei","nodej","wij","gain"]
    def __init__(self,nodei,nodej,wij,gain):
        self.nodei = nodei
        self.nodej = nodej
        self.wij = wij
        self.gain = gain

    def __lt__(self, other):
        """
            an edge is of lower value than an other edge, if its gain is higher
            The aim of this non intuitive definition is to construct a minHeap structure that behaves as
             a maxHeap
        """
        return self.gain > other.gain
    def __eq__(self, other):

        self_pos = (self.nodei.pos,self.nodej.pos)
        other_pos = (other.nodei.pos,other.nodej.pos)

        pos_self_1 = min(self_pos)
        pos_self_2 = max(self_pos)

        pos_other_1 = min(other_pos)
        pos_other_2 = max(other_pos)

        return  (pos_self_1 == pos_other_1) and (pos_self_2 == pos_other_2)

    def __le__(self, other):
        return self.gain >= other.gain
    def __repr__(self):
        keys = self.__slots__
        values = [self.nodei,self.nodej,self.wij,self.gain]
        s =  dict(zip(keys,values))
        out = f"{self.__class__.__name__}("
        for key,value in s.items():
            out += f" {key} = {value} , "
        out = out[:-3]
        out += f")"
        return out
class HeapInitializer:
    lbda = 0.01
    def __init__(self,edges_with_nodes):
        self.edges_with_nodes = edges_with_nodes

        self.nodei = self.edges_with_nodes[:, 0]
        self.nodej = self.edges_with_nodes[:, 1]
        self.wij = self.edges_with_nodes[:,2]


        self.gainH = self.init_gain_H()
        self.gainB = self.init_gain_B()
        self.gain = self.gainH + self.lbda * self.gainB

        #self.edges_with_nodes_and_gain = np.hstack([self.edges_with_nodes,-self.gain.reshape(-1,1)])
        self.edges_with_nodes_and_gain = [(float(b),a) for (a,b) in zip(self.edges_with_nodes,-self.gain.reshape(-1,1))]

        self.edges_with_nodes_and_gainAsNamedTuple = [EdgesExtendedInfo(tmp[1][0],tmp[1][1],tmp[1][2],tmp[0]) for tmp in self.edges_with_nodes_and_gain]
        self.heapMin = self.createBinaryMaxHeap()

    @staticmethod
    def partial_entropy(value):
        return -value * np.log(value)

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