import networkx as nx
import os,itertools
import numpy as np
from utils import image_viewer
import matplotlib.pyplot as plt
from heapq import heappop, heappush, heapify

try:
    from . import data_sampler
    from . import  edge_neighor_adder
except:
    import data_sampler
    import edge_neighor_adder

dirFile = os.path.dirname(__file__)



class NetworkConstructor:
    """
        from an image img, construct a graph,for which nodes are pixels of "img" , and edges links each pair
        of pixels

        Attributes:
            allEdges :
                    a 2D array of shape (...,3)
                    the first dimension indexes the edges
                    the second dimension indexes the position of the init pixel,then  the position of the second pixel
                    then the value of the data.
            wi :
                    a 2D array of shape (2,Np), where Np is the number of nodes (pixels)
                    each row,contains the index of the node , and the sum of its linked edge (at second position)
                    (there is as many node as pixels in the image)

        Remarks:
                the positions of nodes (a.k.a pixels) are the positions on the associated buffer of the image (1D view of an image)

    """
    def __init__(self,img):
        self.img = img
        self.edge_neighbor_adder = edge_neighor_adder.EdgeNeighborAdder(self.img)

        self.shifts = list(itertools.product(range(-1,2),repeat=2))
        self.shifts.remove((0,0))

        self.alledges = self.get_edges_for_all_shifts()

        self.wi = self.get_sum_of_linked_edges_with_index()

        self.alledges = self.filter_and_reshape_edges()

        self.G = self.feed_to_graph()

        #self.mui = self.wi/np.sum(self.wi)
        #self.max_heap = self.construct_maxheap()

    def get_edges_for_all_shifts(self):
        """
            returns:
                allEdges :
                    a 4D array os shape (Nc,3,*self.img.shape),
                    the first dimension indexes the value of the shift (Nc= len(self.shifts) )
                    the second dimension indexes the position of the init pixel,then  the position of the second pixel
                    then the value of the data.
                    the two last positions indexes the positions on the image


            Remarks : we consider in this method only the edge that joins two distinct nodes ,
                    in the ERS algorithm, it is considered
        """
        tmp = [self.edge_neighbor_adder(shift) for shift in self.shifts]
        alledges = np.stack(tmp,axis=0)
        return alledges
    def get_sum_of_linked_edges_with_index(self):
        """

        :return:

                wi :
                    a 2D array of shape (2,Np), where Np is the number of nodes (pixels)
                    each row,contains the index of the node , and the sum of its linked edge (at second position)
                    (there is as many node as pixels in the image)
        """
        wi =  np.sum(self.alledges[:,2],axis=0)
        res = np.transpose(np.stack([self.edge_neighbor_adder.pos_pixel_as_buff, wi]).reshape(2, -1))
        return res
    def filter_and_reshape_edges(self):
        """
            should be applied after the method 'get_edges_for_all_shifts' to transform the self.alledges to a 2D array
            where second (last) dimension indexes , the positions (on image as buffer) of the two nodes (pixels) of the graph, then
            the value of the edge,
            an the the first dimension indexes an edge

            We remove all the edges whose value is purely equal 0


        :return:
        allEdges : a 2D array of shape (...,3), the two first elements must be ints, the last one is a value between 0 and 1
        """

        s = np.moveaxis(self.alledges, 0, 1).reshape(3, -1)
        ROI = (s[2] != 0)
        s1 = s[:, ROI]
        alledges = np.transpose(s1)
        return alledges
    def feed_to_graph(self):
        G = nx.Graph()
        G.add_weighted_edges_from(self.alledges)
        G.add_weighted_edges_from(self.alledges,weight="proba")
        return G

    #TODO : takes into account the warper of minHeap provided by networkx in its utils.heaps package,
    #it might be more convenient
if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)
    img = img.astype("float32")/255.0

    alg = NetworkConstructor(img)

    self = alg