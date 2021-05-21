import os,pickle,time,pdb,heapq
import matplotlib.pyplot as plt
from utils.decorator import *
try:
    from .utils import allUsefulModule
    from . import data_sampler
    from . import network_initializor
    from .heapManager import  heapInitializer,heap_updater
    from . import imageLabeler
except:
    from utils import allUsefulModule
    import data_sampler
    from heapManager import   heapInitializer,heap_updater
    from network_initialization import network_edge_initializor
    import imageLabeler
import utils.utils
import numpy as np
import skimage.measure
from  networkx.algorithms.traversal.edgebfs import edge_bfs

NetworkEdgeInitializor = network_edge_initializor.NetworkEdgeInitializor
dirFile = os.path.dirname(__file__)
# TODO: read ground truth from path_seg using seg_doc.txt
#TODO : check , efficient way to add edge to graph

from enum import Enum
class IterationMode(Enum):
    UntilConvergence = 1

    #TODO : get back here to continue

class Main:
    """
        implementation of the ERS (entropy rate superpixel algorithm)
        From an image, we seek to construct a superpixel segmentation
        two graph are constructed during the process, and first graph (the initial graph) where each pixel
        is linked to its neighbor, and a second graph (the ouput graph), where only the pixels belonging to each
        other are linked.

    """

    path = os.path.join(dirFile,"pickeld_data/pickled_main.pkl") #file where a serialized copy of the instance is saved
    path = os.path.abspath(path)
    def __init__(self,img):
        self.img = img
        self.shape_img = self.img.shape[:2]
        self.nbNodes = np.product(self.img.shape[:2])
        graph_init = NetworkEdgeInitializor(self.img)
        self.edges_with_nodes = self.graph_init.edges_with_nodes
        self.G = graph_init.G
        self.G.add_weighted_edges_from(self.edges_with_nodes,connected = False)

        self.edges_with_nodes = np.array(list(self.G.edges.data()))
        self.heapMin = self.init_heap()
        self.heap_updater = heap_updater.HeapUpdater(self.heapMin,nbNodes = self.nbNodes)
        self.edges_linked = self.update_heap()


        self.list_linked_nodes = self.get_linked_nodes()

        self.imageLabeler = imageLabeler.ImageLabeler(self.img,self.list_linked_nodes)

    def get_linked_nodes(self):
        s1 = [id(el.linked_list_of_nodes) for el in self.G.nodes]
        a, b = np.unique(s1, return_index=True)
        s2 = np.array([el.linked_list_of_nodes for el in self.G.nodes])
        s3 = s2[b]
        return s3
    @timeit
    def update_heap(self,nbIteration = None):
        if nbIteration is None:
            self.heap_updater.iterate_until_end()
        else:
            self.heap_updater.iterate_multiple(nbIteration)
        return self.heap_updater.edges
    @timeit
    def init_heap(self):
        """ returns the heap val"""
        self.heap_initializer = heapInitializer.HeapInitializer(self.edges_with_nodes)
        return self.heap_initializer.heapMin


if __name__ == '__main__':
    index = 134
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)#[:50,:50]
    #img = plt.imread(path_img)
    img = img.astype("float32")/255.0
    alg = Main(img)
    self = alg


    from heapManager.totalCostComputer import TotalCostComputer
    s = TotalCostComputer(alg.heap_updater, alg.G, alg.list_linked_nodes)


    print(f"accumulated_gain {alg.heap_updater.heap_updater_iterator.accumulated_gain}")
    print(f"gain computed at end {s()}")
    #assert alg.heap_updater.heap_updater_iterator.accumulated_gain == s()