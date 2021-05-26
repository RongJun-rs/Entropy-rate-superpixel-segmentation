import networkx as nx
import os,pdb
import numpy as np
from utils import image_viewer
import matplotlib.pyplot as plt

from utils.decorator import *

try:
    from . import data_sampler
    from .. import lbdaAndSigmaComputer
except:
    import data_sampler
    import lbdaAndSigmaComputer

class EdgeNeighborAdder:
    """
        a class used to feed a networkx  graph structure (see NetworkConstructor)
        It takes as input an image, and compute a 2D array
        for which each row contains the positions of two pair of neighboring pixels
        and the edge 'value' depending on the intensities.

        Attribute:
        img : image (of ch channel : 3D array) of shape (n,m,ch)
        n,m : respectively the number of rows and collumns of an image
        cols_grid : 2D array for that contains the col index of each pixel
        rows_grid : 2D array for that contains the row index of each pixel
        img_with_pos : a 3D array of shape (n,m,ch+2), that concatenates 'img', cols_grid and rows_grid, along the last axis

        shift : 2-tuple argument that is initialized (and updated) each time __call__ method is
            called , it preforrms the main computation (class description), considering only the
             neighbors that are separated by shift value

        graph_data_to_add : 2D array, containing on each row, the index (on buffer), of
                            the first node, then the index of the second node, then the value
                            of the edge linking them
        pos_pixel_as_buff : outputs of get_buffer_pos_of_fixed_image
        Methods:
            get_image_with_pos : constructs the 'img_with_pos' attribute
            __call__ : get a shift argument (2-tuple of ints),
                        and compute an edge value of each neighboring pixels that is separated
                        by 'shift'
            construct_mesh_grid : construct the self.cols_grid and self.rows_grid attributes
            get_shifted_image : shift self.img_with_pos with a value of self.shift
            (the shift is not applied on the channels)
            get_edges_for_shift : get a 2D array containing the data to add to the graph
                                it returns self.graph_data_to_add
            get_buffer_pos_of_fixed_image : get a 2D array (same shape of self.img), where each elements, represents the
                            position of the pixel of the image on its buffer representation (as a 1D array, rows stacked horizontally)
    """
    def __init__(self,img):
        self.img = img
        self.n,self.m = self.img.shape[:2]
        self.cols_grid,self.rows_grid = self.construct_mesh_grid()
        self.img_with_pos = self.get_image_with_pos()

        self.pos_pixel_as_buff = self.get_buffer_pos_of_fixed_image()
        self.sigma = lbdaAndSigmaComputer.SigmaReader()()

    def get_image_with_pos(self):
        """
            concatenates 'img', cols_grid and rows_grid (along the last axis) to form
            an image of shape (n,m,ch+2)
        """
        img_with_pos = np.stack([self.rows_grid,self.cols_grid,*np.moveaxis(self.img,2,0)],axis=-1)
        return img_with_pos
    def construct_mesh_grid(self):
        """
            construct two arrays of same shape as self.img, for which each element represents respectively
            the collumn index and the row index on the original image
        """
        cols = np.linspace(0,self.m-1,self.m)
        rows = np.linspace(0,self.n-1,self.n)
        return np.meshgrid(cols,rows)

    def get_shifted_image(self):
        img_shifted = np.roll(self.img_with_pos, shift=[*self.shift, 0], axis=(0, 1, 2))
        return img_shifted

    def get_buffer_pos_of_fixed_image(self):
        pos_pixel_as_buff = self.convert_pixel_to_buffer_pos(self.img_with_pos[...,:2])
        return pos_pixel_as_buff
    def  __call__(self,shift):
        self.shift = shift
        self.graph_data_to_add = self.get_edges_for_shift()
        return self.graph_data_to_add


    def convert_pixel_to_buffer_pos(self,pixel_pos):
        """
            convert positions of pixels, to their positions on
            a buffer

             pixel_pos : a 2D array of shape (Npixel,2)
             for which each line contains the  (row position, and collumn position )
             of each pixel
        """
        buffer_pos = pixel_pos[...,0]*self.m + pixel_pos[...,1]
        return buffer_pos
    #@debugit
    def get_edges_for_shift(self):
        """
            return 2D array representing the value of each edge on the graph to construct
            ----
            returns
                graph_data_to_add : a 2D array, for which each row has the syntax (idx0,idx1,value)
                idx0, is the index of the first node,
                idx1 is the index of the second node,
                value, is the value of the edge linking the twwo nodes
        """
        img_shifted = self.get_shifted_image()
        diff = img_shifted - self.img_with_pos

        diff_pos = diff[...,:2]
        diff_intensity_values = diff[...,2:]
        ROI = np.product(np.abs(diff_pos) <= 1,axis=-1).astype("bool")

        norm_diff_pos = np.sqrt(np.sum(diff_pos**2,axis=-1))
        data = np.exp(-(np.sum(diff_intensity_values ** 2, axis=-1)*norm_diff_pos**2)/(2*(self.sigma**2))) * ROI

        init_pos = self.convert_pixel_to_buffer_pos(img_shifted[...,:2])
        dst_pos = self.pos_pixel_as_buff
        graph_data_to_add = np.stack((init_pos,dst_pos,data),axis=0)
        return graph_data_to_add


if __name__ == '__main__':
    index = 15
    path_img,path_seg = data_sampler.get_path_img_and_seg_from_id(index)
    img = plt.imread(path_img)[:50,:50]
    img = img.astype("float32")/255.0
    out = np.roll(img,shift=[1,1,0],axis=(0,1,2))
    diff = (out-img)

    alg = EdgeNeighborAdder(img)

    self = alg