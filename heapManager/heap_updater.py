import numpy as np
import time
from utils.decorator import timeit
try:
    from . import  heap_updater_iterator
except:
    from heapManager import heap_updater_iterator

from heapq import heappop,heappush

class HeapUpdater:
    def __init__(self,heapMin,nbNodes,K):
        self.heapMin = heapMin
        self.nbNodes = nbNodes
        self.K = K
        self.edges, self.instant_first_edge_add = self.init_graph()
        self.heap_updater_iterator = heap_updater_iterator.HeapUpdaterIterator(self.heapMin,self.instant_first_edge_add,self.edges)

    def init_graph(self):
        edges = [heappop(self.heapMin)]
        edges[0].update_gain()
        edges[0].add_edge_to_graph()
        instant_first_edge_add = time.time()
        return edges,instant_first_edge_add

    def iterate(self):
        self.heap_updater_iterator()
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