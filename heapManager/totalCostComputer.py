"""
    this routine must be used for test in order to access if the total cost, of the current state of
    the graph is equal to the expected value
"""
import numpy as np
try:
    from .. import lbdaAndSigmaComputer
    from ..utils import utils
except:
    import lbdaAndSigmaComputer
    from utils import utils

class TotalCostComputer:
    def __init__(self,heap_updater,G,list_linked_nodes):
        self.heap_updater = heap_updater
        self.edges = self.heap_updater.edges
        self.G = G
        self.list_linked_nodes = list_linked_nodes
        self.NA = self.heap_updater.heapMin[0].nodej.dNa + self.heap_updater.nbNodes

        self.lbda = lbdaAndSigmaComputer.LbdaComputer().lbda

        self.pij, self.pji, self.muedgei, self.muedgej = self.partial_cost_computer_vectorized_idiffj()
        self.mui,self.pii = self.partial_cost_computer_vectorized_self_loop()

    def __call__(self):
        return self.compute_cost()

    def partial_cost_computer_vectorized_idiffj(self):
        """
        compute the values of pij , pji , mui and muj for i different of j
        :return:
        """
        pij_pji_mui_muj = [(edge.pij,edge.pji,edge.nodei.mu,edge.nodej.mu) for edge in self.edges]
        pij,pji,mui,muj = np.transpose(np.array(pij_pji_mui_muj))
        return pij,pji,mui,muj
    def partial_cost_computer_vectorized_self_loop(self):
        """
        compute the values of pii , mui for all nodes
        :return:
        """
        s = list(self.G.nodes)
        a = [(el.mu, el.prob) for el in s]
        mui,pii = np.transpose(np.array(a))
        return mui,pii

    @staticmethod
    def partial_entropy(value):
        return utils.partial_entropy_iterable(value)

    def compute_H_cost(self):
        cost_H = np.sum(self.partial_entropy(self.pij) * self.muedgei + self.partial_entropy(self.pji) * self.muedgej)
        cost_H += np.sum(self.mui * self.partial_entropy(self.pii))
        return cost_H

    def compute_B_cost(self):
        p = np.array([len(el) for el in self.list_linked_nodes])
        p = p / np.sum(p)

        layout_entropy = np.sum(self.partial_entropy(p))
        cost_B = layout_entropy - self.NA
        return cost_B

    def  compute_cost(self):
        return self.compute_H_cost() + self.lbda * self.compute_B_cost()
