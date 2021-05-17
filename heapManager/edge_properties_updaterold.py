# """
#     contains one class, that checks if an edge must be added to the networkx graph
# """
#
# import numpy as np
# import scipy.stats
#
# class EdgePropertiesUpdater:
#     """
#         An object  (useful, for the construction of the output graph), that represents an edge on the initial
#         graph (look at main for more details),it contains the weight value of an edge, and its two linked nodes
#         (implemented as 'Node' object) and nodes of the 'G' graph of main
#
#         :attribute
#             nodei is the first node of the input tuple (edge_info)
#             nodej, the second node, and wij the weight between the two nodes
#
#             pij, is the transition probability from i to j (in the cas i and j are connected)
#             pji, is also defined
#
#             pii and pjj are also declared
#         :methods
#             get_Gain_H : compute the gain on the function H for adding the current edge
#             get_Gain_B : compute the gain on the function B for adding the current edge
#             get_Gain : compute the gain on the total function for adding the current edge
#
#             link : link the two node on the resulting edge
#
#             update : update the value of the gain, (is called each time the MaxHeap structure is updated, and the
#                     edge is at the top)
#
#         :Remarks :
#             * even if self edges exists, we don't includes them in the edge, but as node properties
#
#             * The value of pij is 0 if i and j are not connected (on the ouput graph) , and wij if they are connected and
#              different from 0,it is equal to 1 - Sigma_{k connected to i} pik if i=j
#
#             * pii is contained in self.nodei.prob, and pjj is contained in self.nodej.prob
#
#             * pii and pjj are the the value of gain are the only values that changes during the execution of the algorithm
#
#
#     """
#     lbda = 0.01
#     __slots__ = ["mgain","nodei","nodej","wij","pij","pji","pii","pjj","gain","pii_new","pjj_new"]
#     def __init__(self, edge_info):
#         """
#         :param
#             edge_info: contains an iterable, with the two first elements (Node objects), and the last element the value
#             of the weight
#         """
#         #self.mgain, (self.nodei,self.nodej,self.wij ) \
#         self.mgain,((self.nodei,self.nodej,self.wij),index) = edge_info
#
#         self.pij = self.wij / self.nodei.w  # pij*ui is equal to pji*muj
#         self.pji = self.wij / self.nodej.w
#
#
#
#     def get_gain(self):
#         self.pii = self.nodei.prob
#         self.pjj = self.nodej.prob
#
#         gain = self.get_gain_H() + self.lbda * self.get_gain_B()
#         return gain
#
#     def get_m_gain(self):
#         return - self.get_gain()
#
#     def update(self):
#         """
#             apply the changes on the graph
#         """
#         self.nodei.prob = self.pii_new
#         self.nodej.prob = self.pjj_new
#         self.nodei.union(self.nodej)
#
#     @staticmethod
#     def partial_entropy(value):
#         return -value * np.log(value)
#
#     def get_gain_H(self):
#         """
#         compute the difference in cost by adding the edge linking nodei and nodej, for the function H
#         , in other words H(A U {edge}) - H(A), where A is the constructed graph so far
#         (not declared are this level)
#         """
#
#         mui = self.nodei.mu
#         muj = self.nodej.mu
#
#
#         self.pii_new = self.pii - self.pij
#         self.pjj_new = self.pjj - self.pji
#
#         part1 = mui * self.partial_entropy(self.pij) + muj * self.partial_entropy(self.pji)
#         part2 = mui * (self.partial_entropy(self.pii_new) - self.partial_entropy(self.pii))
#         part3 = muj * (self.partial_entropy(self.pjj_new) - self.partial_entropy(self.pjj))
#         res = part1 + part2 + part3
#
#         return res
#
#     def get_gain_B(self):
#         Si = self.nodei.linked_list_of_nodes
#         Sj = self.nodej.linked_list_of_nodes
#
#         if Si is Sj:
#             return 0
#
#         Sunion = Si.union(Sj)
#
#         card_Sunion = len(Sunion)
#         card_Si = len(Si)
#         card_Sj = len(Sj)
#
#         card_V = self.nodei.graph.number_of_nodes()
#
#
#         diff_HA = self.partial_entropy(card_Sunion/card_V)
#         diff_HA -= self.partial_entropy(card_Si/card_V) + self.partial_entropy(card_Sj/card_V)
#
#         diff_NA = -1 # NA is reduced by 1 if Si is different from Sj
#
#         gain = diff_HA - diff_NA
#         return gain
#
#
#
#
