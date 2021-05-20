import networkx as nx
import os,itertools
import numpy as np
import matplotlib.pyplot as plt
try:
    from utils import data_sampler
    from . import  edge_neighor_adder
    from . import node
except:
    import data_sampler
    from network_initialization import edge_neighor_adder
    from network_initialization import node


dirFile = os.path.dirname(__file__)




#Node = collections.namedtuple('Node',['pos','wi','mui'])

class NetworkEdgeInitializor:
    """
        from an image img, construct a graph,for which nodes are pixels of "img" , and edges links each pair
        of pixels

        Attributes:
            img :
                must be of float type with values between 0 and 1, with 3 channel
            allEdges :
                    a 2D array of shape (...,3)
                    the first dimension indexes the edges
                    the second dimension indexes the position of the init pixel,then  the position of the second pixel
                    then the value of the data.
            wi :
                    a 2D array of shape (2,Np), where Np is the number of nodes (pixels)
                    each row,contains the index of the node , and the sum of its linked edge (at second position)
                    (there is as many node as pixels in the image)

            G : a networkx graph structure, containing in fact two graph:
                one with weights wij as defined on the paper, and a second graph with weights pij, it'is moroe convening
                to use the same graph, as in networkx, each node, can contains multiple
        Remarks:
                the positions of nodes (a.k.a pixels) are the positions on the associated buffer of the image (1D view of an image)

    """
    def __init__(self,img):
        self.img = img
        self.G = nx.Graph() #init graph

        self.edge_neighbor_adder = edge_neighor_adder.EdgeNeighborAdder(self.img)

        self.shifts = list(itertools.product(range(-1,2),repeat=2))
        self.shifts.remove((0,0))

        self.alledges = self.get_edges_for_all_shifts()

        self.nodes = self.construct_nodes_instances()

        self.edges_with_nodes = self.get_edges_and_nodes()


        self.add_nodes_to_graph()

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
    def get_edges_and_nodes(self):
        """
            computes a 2D array containing values of the weight for each edge, of the graph to be constructed
            with a reference to its nodes (with filtering of the edges equla to 0)

        :return:
            edges_with_nodes : a 2D array, of shape (...,3)
            The second dimensions indexes the edges
            The first dimensions indexes three element :
            The first and second index , gives two linked nodes
            the last index indexes the weight value between the two nodes

        remarks:
            * must be called after the function 'get_edges_for_all_shifts' and after the instantiation
            of the nodes

             * get_edges_with_nodes_for_shift takes as input a 'shift', and do the 'job' for the particular value
             of shift (iterable of two elements i and j with values equal to 0 or 1)

        """
        nodes_as_array = np.array(self.nodes).reshape(self.img.shape[:2])
        def get_edges_with_nodes_for_shift(index_shift,shift):
            #extract edge values
            edges = self.alledges[index_shift]
            edge_values = edges[2]

            #remove elements for which edge_value is equal 0 (equivalent to value with no edge)
            ROI = (edge_values != 0)

            # stack the node instance, with shifted versions and edge
            shifted_nodes_as_array = np.roll(nodes_as_array, shift=shift, axis=(0, 1))
            s = [nodes_as_array,shifted_nodes_as_array,edge_values]
            res = np.stack([el[ROI] for el in s],axis=1)
            return res
        edges_with_nodes = [ get_edges_with_nodes_for_shift(index_shift,shift) for (index_shift,shift) in enumerate(self.shifts)]
        return np.vstack(edges_with_nodes)
    def construct_nodes_instances(self):
        """

        :return:
                nodes : a list of nodes to be integrated onthe graph
        remarks:
                nodeInfo :
                    a 2D array of shape (Np,3), where Np is the number of nodes (pixels)
                    each row,contains the index of the node ,  the sum of its linked edge (at second position)
                    (there is as many node as pixels in the image) , then the last value divided byt eh sum of all the edges

        """
        node.Node.dNa = 0
        wi =  np.sum(self.alledges[:,2],axis=0)
        mui = wi/np.sum(wi)
        nodeInfo = np.transpose(np.stack([self.edge_neighbor_adder.pos_pixel_as_buff, wi,mui]).reshape(3, -1))

        nodes = [node.Node(pos = el[0], w = el[1], mu = el[2], graph = self.G) for el in nodeInfo]
        return nodes
    def add_nodes_to_graph(self):
        self.G.add_nodes_from(self.nodes)
    #TODO : takes into account the warper of minHeap provided by networkx in its utils.heaps package,
    #TODO : on edgeneighbor class don't ouput positions at index :,0:2,:,:, but Nodes instance

    #it might be more convenient
if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)
    img = img.astype("float32")/255.0

    alg = NetworkEdgeInitializor(img)

    self = alg

    import sys
    sys.exit()

    G = nx.Graph()

    G.add_weighted_edges_from(self.edges_with_nodes)

    s = G.edges.data()

    s1 = list(s)

    s2 = [{'weight': el[2]['weight'], 'node0': el[0], 'node1': el[1]} for el in s1]