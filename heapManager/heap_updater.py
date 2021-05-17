import numpy as np


try:
    from . import  edge_properties_updater
except:
    from heapManager import edge_properties_updater

class HeapUpdater:
    def __init__(self,heapMin):
        self.heapMin = heapMin
        self.edges = []
    def iterate(self):
        self.id_top_last = self.get_id_top()
        self.update_top()
        if self.id_top_last == self.get_id_top():
            self.edges.append(self.heappop())
    def heappop(self):
        pass
    def __call__(self):
        while True:
            self.iterate()
    def get_id_top(self):
        pass
    def update_top(self):
        self.heapIterator.computeGain()


if __name__ == '__main__':
    import pickle
    heapMin = pickle.load(open("../pickeld_data/heapMin", "rb"))