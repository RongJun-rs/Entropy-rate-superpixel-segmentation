import numpy as np
import pdb,heapq,time
import collections
from utils.decorator import debugit


class EdgesExtendedInfo:
    """
        nodei,nodej and edge are the nodes'object and the edge's object that are on the graph
    """
    lbda = 0.5
    __slots__ = ["nodei","nodej","edge","wij","gain","pij","pji","pii","pjj","pii_new","pjj_new","timestamp"]
    def __init__(self,nodei,nodej,edge,gain):
        self.nodei = nodei
        self.nodej = nodej
        self.edge = edge
        self.wij = self.edge["weight"]
        self.gain = gain

        self.timestamp = time.time() # time of creation of the nodes
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
    def get_gain(self):
        self.pij = self.wij / self.nodei.w  # pij*ui is equal to pji*muj
        self.pji = self.wij / self.nodej.w
        self.pii = self.nodei.prob
        self.pjj = self.nodej.prob
        gain = self.get_gain_H() + self.lbda * self.get_gain_B()
        return gain
    def update_gain(self):
        self.gain = self.get_gain()
        self.timestamp = time.time()
    def add_edge_to_graph(self):
        """
            apply the changes on the graph
        """
        self.pii = self.pii_new
        self.pjj = self.pjj_new
        self.nodei.prob = self.pii
        self.nodej.prob = self.pjj
        self.nodei.union(self.nodej)
        self.edge['connected'] = True
    @staticmethod
    def partial_entropy(value):
        if value>0:
            return -value * np.log(value)
        else:
            return 0
    def get_gain_H(self):
        """
        compute the difference in cost by adding the edge linking nodei and nodej, for the function H
        , in other words H(A U {edge}) - H(A), where A is the constructed graph so far
        (not declared are this level)
        """

        mui = self.nodei.mu
        muj = self.nodej.mu


        self.pii_new = self.pii - self.pij
        self.pjj_new = self.pjj - self.pji

        part1 = mui * self.partial_entropy(self.pij) + muj * self.partial_entropy(self.pji)
        part2 = mui * (self.partial_entropy(self.pii_new) - self.partial_entropy(self.pii))
        part3 = muj * (self.partial_entropy(self.pjj_new) - self.partial_entropy(self.pjj))
        res = part1 + part2 + part3

        return res

    def get_gain_B(self):
        Si = self.nodei.linked_list_of_nodes
        Sj = self.nodej.linked_list_of_nodes

        if Si is Sj:
            return 0

        Sunion = Si.union(Sj)

        card_Sunion = len(Sunion)
        card_Si = len(Si)
        card_Sj = len(Sj)

        card_V = self.nodei.graph.number_of_nodes()


        diff_HA = self.partial_entropy(card_Sunion/card_V)
        diff_HA -= self.partial_entropy(card_Si/card_V) + self.partial_entropy(card_Sj/card_V)

        diff_NA = -1 # NA is reduced by 1 if Si is different from Sj

        gain = diff_HA - diff_NA
        return gain