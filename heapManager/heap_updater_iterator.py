import numpy as np


class HeapUpdaterIterator:
    lbda = 0.1
    def __init__(self,heapMin):
        self.heapMin = heapMin


    def computeGain(self):


    @staticmethod
    def partial_entropy(value):
        return -value * np.log(value)

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
