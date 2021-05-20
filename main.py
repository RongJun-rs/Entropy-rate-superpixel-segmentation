import os,pickle,time,pdb,heapq
import matplotlib.pyplot as plt
from utils.decorator import *
try:
    from .utils import allUsefulModule
    from . import data_sampler
    from . import network_initializor
    from .heapManager import  heapInitializer,heap_updater
except:
    from utils import allUsefulModule
    import data_sampler
    from heapManager import   heapInitializer,heap_updater
    from network_initialization import network_edge_initializor
import utils.utils
import numpy as np
import skimage.measure
from  networkx.algorithms.traversal.edgebfs import edge_bfs

NetworkEdgeInitializor = network_edge_initializor.NetworkEdgeInitializor
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
        self.shape_img = self.img.shape[:2]
        self.nbNodes = np.product(self.img.shape[:2])
        graph_init = NetworkEdgeInitializor(self.img)
        self.edges_with_nodes = graph_init.edges_with_nodes
        self.G = graph_init.G
        self.G.add_weighted_edges_from(self.edges_with_nodes,connected = False)

        self.edges_with_nodes = np.array(list(self.G.edges.data()))
        self.heapMin = self.init_heap()
        self.heap_updater = heap_updater.HeapUpdater(self.heapMin,nbNodes = self.nbNodes)
        self.edges_linked = self.update_heap()


        self.list_linked_nodes = self.get_linked_nodes()

        self.labelling = self.label_nodes()

        self.labelling = utils.utils.blend_img_with_semgmentation_map(self.img,self.labelling)

    def get_linked_nodes(self):
        s1 = [id(el.linked_list_of_nodes) for el in self.G.nodes]
        a, b = np.unique(s1, return_index=True)
        s2 = np.array([el.linked_list_of_nodes for el in self.G.nodes])
        s3 = s2[b]
        return s3

    @timeit
    def update_heap(self):
        self.heap_updater.iterate_until_end()
        return self.heap_updater.edges
    @timeit
    def init_heap(self):
        """ returns the heap val"""
        self.heap_initializer = heapInitializer.HeapInitializer(self.edges_with_nodes)
        return self.heap_initializer.heapMin

    def save(self):
        pickle.dump(self,open(self.path,"wb"))
    @classmethod
    def load(cls):
        return pickle.load(open(cls.path,"rb"))

    #TODO : add mixin for saving and loading of instance of class at particular state
    #TODO : add module to label the nodes
    def label_nodes(self):
        s4 = [([el1.pos for el1 in el],np.min([el1.pos for el1 in el])) for el in self.list_linked_nodes]
        s5 = []
        s6 = []
        for el in s4:
            s5.extend(el[0])
            s6.extend([el[1]] * len(el[0]))
        g = np.argsort(s5)
        return np.array(s6)[g].reshape(self.shape_img)
    def show_image_with_res(self):
        plt.imshow(np.hstack((self.img, self.labelling)), cmap="gray");
        plt.show()
if __name__ == '__main__':
    index = 134
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)[:20,:20]
    #img = plt.imread(path_img)
    img = img.astype("float32")/255.0

    #img = img[:50,:50]
    #import pdb;alg = pdb.runcall(Main,img)
    alg = Main(img)
    self = alg


    from heapManager.totalCostComputer import TotalCostComputer
    s = TotalCostComputer(alg.heap_updater, alg.G, alg.list_linked_nodes)
