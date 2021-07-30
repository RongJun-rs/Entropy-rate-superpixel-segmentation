import time
from utils.decorator import timeit

import numpy as np
import lbdaAndSigmaComputer
from heapq import heappop,heappush


class HeapUpdaterIterator:
    def __init__(self,heapMin,instant_first_edge_add,edges):
        self.heapMin = heapMin
        self.instant_last_graph_edit = instant_first_edge_add
        self.edges = edges

        self.edges[0].update_gain()
        self.accumulated_gain = self.init_acumulated_gain()

    def init_acumulated_gain(self):
        nbNodes = self.heapMin[0].nodei.graph.number_of_nodes()
        lbda = lbdaAndSigmaComputer.LbdaComputer().lbda
        accumulated_gain = self.edges[0].gain + lbda * ( np.log(nbNodes) - nbNodes)
        return accumulated_gain

    def check_if_gain_minHeap_updated_since_graph_edit(self):
        """
             check if the top of minHeap is 'updated' i.e if the gain of adding the associated edge is computed
             (updated), taking into account the current state of the graph.

             it is True if the instant when the 'gain' has been computed is superior, to the instant the last time,
             the min Heap is changed, which is equivalent to the instant, when the graph is changed

             Remarks : if the order of the elements on the min Heap, without a change of the number of the element

             the order of elements in the min Heap, can change without adding any new elements  to the graph,
             if one of child node, of the top node, have the same value.
             In this case, we consider, that the min Heap didn't change, so the returned value is False



        """
        gain_updated_since_last_graph_edit = (self.heapMin[0].timestamp > self.instant_last_graph_edit )  # is aways True as first iteration
        return gain_updated_since_last_graph_edit

    def check_if_nodei_and_j_are_linked(self):
        """
            check if the nodes of the edge at the top of the minHeap, are already linked
            Remarks:
                each node have an attribute named 'linked_list_of_nodes' : that is updated, sequentially each time
                two nodes are merged
        """
        nodeiandnodejoftopHeapAreLinked = (self.heapMin[0].nodei.linked_list_of_nodes is self.heapMin[0].nodej.linked_list_of_nodes)
        return nodeiandnodejoftopHeapAreLinked
    # @profile
    def __call__(self):
        """
            if nodes of the top of minHeap are linked pop, then remove it from the heap,
            else check if the gain of the top of the min heap is updated since last time graph is edited
            If not update the gain, then the min heap
            if the top heap is already updated, just  pop it from the heap, and add the 'edge' to the graph
            """
        nodeiandnodejoftopHeapAreLinked = self.check_if_nodei_and_j_are_linked()
        if nodeiandnodejoftopHeapAreLinked: #if nodes of the top of minHeap are linked pop, then remove it from the heap,
            heappop(self.heapMin)
            return
        gain_not_updated_since_last_adding = not(self.check_if_gain_minHeap_updated_since_graph_edit())
        if gain_not_updated_since_last_adding: # else check if the gain of the top of the min heap is updated since last time graph is edited
            self.heapMin[0].update_gain()  # update the gain of the top heap
            top_heap = heappop(self.heapMin) # then the min heap, by pop_and_push of top node
            heappush(self.heapMin,top_heap)
        else:  # if the top heap is already updated, jut need to pop it from the heap, and 'update' the edge
            edge = heappop(self.heapMin)
            edge.add_edge_to_graph() # add the edge to the graph
            self.edges.append(edge)
            self.instant_last_graph_edit = time.time()
            self.accumulated_gain += self.heapMin[0].gain
