"""
    module used to color each segment of an image, such that the segmentation ig given by
    a list of linked pixels (nodes)
"""
import numpy as np
import matplotlib.pyplot as plt
import utils.utils
class ImageLabeler:
    def __init__(self,img,linked_list_of_nodes):
        """

        :param img: mage of 3 channels : 3D array of shape (...,3)
        :param linked_list_of_nodes: list of list of Node object
        """
        self.img = img
        self.shape_img = self.get_shape_img()
        self.linked_list_of_nodes = linked_list_of_nodes

        self.labelling = self.label_nodes()
        self.labelling = self.transform_values()
    # TODO : add module to label the nodes
        self.shape_img = self.get_shape_img()

    def get_shape_img(self):
        """ return the shape of self.img"""
        shape_img = self.img.shape[:2]
        return shape_img
    def label_nodes(self):
        """

        :return: 2D image for which each pixels of same values are linked (belong to the same segment), the value, is
        the minimal position among the linked pixels of a group
        """
        s4 = [([el1.pos for el1 in el], np.min([el1.pos for el1 in el])) for el in self.linked_list_of_nodes]
        s5 = []
        s6 = []
        for el in s4:
            s5.extend(el[0])
            s6.extend([el[1]] * len(el[0]))
        g = np.argsort(s5)
        return np.array(s6)[g].reshape(self.shape_img)

    def transform_values(self,alpha=0.5):
        """ transform the values of the labelling map to a map with flaot values,between 0 and 1, uniformly
        spaced , then merge it with the input image, using the alpha coefficient
            :returns
            labelling : the ouput labelling
        """
        #TODO : add boundary highliting
        labelling = utils.utils.blend_img_with_semgmentation_map(self.img,self.labelling,alpha=alpha)
        return labelling

    def show_image_with_res(self):
        plt.imshow(np.hstack((self.img, self.labelling)), cmap="gray");
        plt.show()