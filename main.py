import os,pickle,time,pdb,heapq
import matplotlib.pyplot as plt
from utils.decorator import *
try:
    from .utils import allUsefulModule
    from . import data_sampler
    from . import network_initializor
    from .heapManager import edge_properties_updaterold, heapInitializer,heap_updater
except:
    from utils import allUsefulModule
    import data_sampler
    from heapManager import  edge_properties_updaterold, heapInitializer,heap_updater
    from network_initialization import network_initializor

import numpy as np

NetworkInitializor = network_initializor.NetworkInitializor
dirFile = os.path.dirname(__file__)
# TODO: read ground truth from path_seg using seg_doc.txt
#TODO : check , efficient way to add edge to graph

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
        graph_init = NetworkInitializor(self.img)
        self.edges_with_nodes = graph_init.edges_with_nodes
        self.G = graph_init.G
        self.G.add_weighted_edges_from(self.edges_with_nodes,connected = False)

        self.heapMin = self.init_heap()

        self.heap_updater = heap_updater.HeapUpdater(self.heapMin,nbNodes = np.product(self.img.shape[:2]))
        self.heap_updater.iterate_until_end()
    #@debugit
    @timeit
    def get_list_of_edge_properties(self):
        list_of_edges_properties = [edge_properties_updaterold.EdgePropertiesUpdater(el) for el in self.heapMin]
        return list_of_edges_properties

    def save(self):
        pickle.dump(self,open(self.path,"wb"))

    @timeit
    def init_heap(self):
        """ returns the heap val"""
        self.heap_initializer = heapInitializer.HeapInitializer(self.edges_with_nodes)
        return self.heap_initializer.heapMin
    @classmethod
    def load(cls):
        return pickle.load(open(cls.path,"rb"))


if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)
    img = img.astype("float32")/255.0

    #img = img[:50,:50]
    #import pdb;alg = pdb.runcall(Main,img)
    alg = Main(img)

    #alg = Main.load()

    #self = alg