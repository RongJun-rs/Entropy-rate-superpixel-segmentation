# Entropy-rate-superpixel-segmentation


implementation of the article "https://ieeexplore.ieee.org/document/5995323" . 
The code is implemented with the framework Networkx, and thus, it is very slow (as Networkx is pure python), in future version, I will replace Networkx  with graph_tool or igrah (for which the main code is in C++),
which is faster.


The syntax to call the code is the following:
python main.py -img path_image -sp N
where:
path_image is the path to the image to be partitionned
N is the number of superpixels for the partitionning of the image

choose a small image for tests 
