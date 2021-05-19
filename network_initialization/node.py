""" class to define a Node on the graph structure, it is included on a networkx graph"""

try:
    from ..utils.allUsefulModule import *
except:
    from utils.allUsefulModule import *

class SetAndLabel:
    __slots__ = ["theSet","theLabel"]
    def __init__(self,theSet,theLabel):
        self.theSet = theSet
        self.theLabel = theLabel

    def union(self,other):
        self.theSet |= other.theSet
        self.theLabel = min(self.theLabel,other.theLabel)
        return self
    def __len__(self):
        return len(self.theSet)

    def __iter__(self):
        return (el for el in self.theSet)
class Node:
    dNa = 0 # the difference between the number of  suepr pixels of  images , and the numbers of pixels (equaal to 0 at beginning)
    # is reduced by one, each time a merging occurs
    """
        class representing nodes, contains only 4 elements (fixed ):
            pos : the position of the node (pixel) , on the buffer (representation) of an image
            w : the sum of the values of the neighboring pixels of the graph (doesn't change depends on the connectivity)
            mu : w/(sum(w)) : w divided by the sum of all the elements
            prob : set to 1, must be changed during the construction of the addition sparser memory usage, it is the the
                value of the self loop edge of the node

        Remarks :
            pii, is the only mutable elements, we use slots also, for s
    """
    __slots__ = ['pos','w','mu','prob','graph','linked_list_of_nodes','label']
    def __init__(self,**kwargs):
        #assert len(args) == 3
        self.pos = kwargs['pos']
        self.w = kwargs['w']
        self.mu = kwargs['mu']
        self.graph = kwargs['graph']
        self.prob = 1
        #self.label = self.pos
        self.linked_list_of_nodes = {self} #begin with empty set, then add the element
        #self.linked_list_of_nodes = SetAndLabel({self},self.pos) #begin with empty set, then add the element
    def __repr__(self):
        keys = self.__slots__
        values = [self.pos,self.w,self.mu,self.prob]
        s =  dict(zip(keys,values))
        out = f"{self.__class__.__name__}("
        for key,value in s.items():
            out += f" {key} = {value} , "
        out = out[:-3]
        out += f")"
        return out

    def union(self,other_node):
        """
            returns the union of the linked_list_of_nodes and update both of them
        """

        n1 = len(self.linked_list_of_nodes)
        n2 = len(other_node.linked_list_of_nodes)

        if n1 > n2:
            self.linked_list_of_nodes |= other_node.linked_list_of_nodes
            for el in other_node.linked_list_of_nodes:
                el.linked_list_of_nodes = self.linked_list_of_nodes
        else:
            other_node.linked_list_of_nodes |= self.linked_list_of_nodes
            for el in self.linked_list_of_nodes:
                el.linked_list_of_nodes = other_node.linked_list_of_nodes

        Node.dNa -= 1