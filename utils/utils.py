import skimage.measure
import numpy as np
from .allUsefulModule  import *

def color_label(segmentation_layout):
    """
    takes as input a segmentation layout, for which each segment is represented by a value,
    and transform it to another segment layout , with 3 channels, for which the values on each channel,
    are int, in [|0,n|[, where n is the number of segments

    :param segmentation_layout: 2 dimensionnal array of shape (N,M)
    :return: res : 3 dimensionnal array of shape (N,M,3)
    """
    labelling = skimage.measure.label(segmentation_layout)

    a = np.linspace(0, labelling.max(), labelling.max() + 1)/labelling.max()
    b = a.copy()
    c = a.copy()
    np.random.shuffle(a)
    np.random.shuffle(b)
    np.random.shuffle(c)
    new_labelling = np.stack([a[labelling],b[labelling],c[labelling]],axis=-1)
    return new_labelling

def blend_img_with_semgmentation_map(image,segmentation_layout,alpha=0.5):
    """"""

    res = alpha * image + (1-alpha) * color_label(segmentation_layout)
    return res
