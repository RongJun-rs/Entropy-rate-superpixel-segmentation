import os,glob,sys
import matplotlib.pyplot as plt
import numpy as np
from utils import image_viewer
import networkx as nx
try:
    from . import data_sampler
except:
    import data_sampler

dirFile = os.path.dirname(__file__)
# TODO: read ground truth from path_seg using seg_doc.txt


if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)
    out = np.roll(img,shift=[10,10,0],axis=(0,1,2))
    image_viewer.show_multiple_images([img,out])
