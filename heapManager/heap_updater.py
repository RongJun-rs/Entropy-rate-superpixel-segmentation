import numpy as np
import time
from utils.decorator import timeit
try:
    from . import  edge_properties_updaterold
except:
    from heapManager import edge_properties_updaterold

from heapq import heappop,heappush

class HeapUpdater:
    def __init__(self,heapMin,nbNodes,K=100):
        self.heapMin = heapMin
        self.nbNodes = nbNodes
        self.K = K
        self.edges = [heappop(self.heapMin)]
        self.edges[0].update_gain()
        self.edges[0].update()
        self.timestamp_adding = time.time()
    def iterate(self):
        gain_not_updated_since_last_adding =  (self.heapMin[0].timestamp < self.timestamp_adding ) # is aways True as first iteration
        nodeiandnodejoftopHeapAreLinked = (self.heapMin[0].nodei.linked_list_of_nodes is self.heapMin[0].nodej.linked_list_of_nodes)
        if nodeiandnodejoftopHeapAreLinked:
            heappop(self.heapMin)
        elif gain_not_updated_since_last_adding:
        #if gain_not_updated_since_last_adding:
            self.heapMin[0].update_gain() #update the top heap
            top_heap = heappop(self.heapMin) #pop and push to update the heap
            heappush(self.heapMin,top_heap)

        else: # the top heap is already updated, jut need to pop it
            self.edges.append(heappop(self.heapMin))
            self.edges[-1].update()
            self.timestamp_adding = time.time() #TODO: timestamp is not convenient ..., because
            #to mark the instant of last time an edge is popped from the heap, in order to update if necessary

    def iterate_multiple(self,nb,print_rate=1000):
        for i in range(nb):
            self.iterate()
            if len(self.heapMin) % print_rate == 0:
                print(len(self.heapMin))

    @timeit
    def iterate_until_end(self):
        d = len(self.heapMin)
        while d>0 and self.check_condition():
            self.iterate()
            if  d % 100000 == 0:
                print(d)
            d = len(self.heapMin)

    def check_condition(self):
        self.nb_super_pixels = self.heapMin[0].nodei.dNa + self.nbNodes
        return self.nb_super_pixels > self.K



if __name__ == '__main__':
    import pickle
    heapMin = pickle.load(open("../pickeld_data/heapMin", "rb"))