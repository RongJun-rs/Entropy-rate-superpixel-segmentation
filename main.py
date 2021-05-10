import os,glob,sys
import matplotlib.pyplot as plt
import numpy as np
from utils import image_viewer
import networkx as nx
try:
    from . import data_sampler
    from . import network_initializor
except:
    import data_sampler
    import network_initializor

NetworkInitializor = network_initializor.NetworkInitializor
dirFile = os.path.dirname(__file__)
# TODO: read ground truth from path_seg using seg_doc.txt


class Main:
    def __init__(self,img):
        self.img = img
        graph_init = NetworkInitializor(self.img)
        self.G = graph_init.init_graph()
        self.list_of_edges = self.G.edges.data()


    def get_G(self,edge):
        """ compute the difference in cost by adding a particular edge"""
        nodei = edge[0]
        nodej = edge[1]
        wij = edge[2]['weight']

        wi = nodei.w
        wj = nodej.w

        mui = nodei.mu
        muj = nodej.mu

        pij = wij / wi  # pij*ui is equal to pji*muj
        pji = wij / wj

        pii = nodei.prob
        pjj = nodej.prob

        part1 = -mui * pij * np.log(pij) - muj * pji * np.log(pji)
        pii_new = pii - pij
        pjj_new = pjj - pji
        part2 = - pii_new * np.log(pii_new) - pjj_new * np.log(pjj_new)
        part3 = pii * np.log(pii) + pjj * np.log(pjj)
        res = part1 + part2 + part3
        return res
if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)
    img = img.astype("float32")/255.0

    alg = Main(img)

    sys.exit()
    self = alg

    G = nx.Graph()

    G.add_weighted_edges_from(self.edges_with_nodes)

    s = G.edges.data()

    s1 = list(s)

    s2 = [{'weight': el[2]['weight'], 'node0': el[0], 'node1': el[1]} for el in s1]