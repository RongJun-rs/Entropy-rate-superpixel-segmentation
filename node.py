""" class to define a Node on the graph structure, it is included on a networkx graph"""


class Node:
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
    __slots__ = ['pos','w','mu','prob']
    def __init__(self,**kwargs):
        #assert len(args) == 3
        self.pos = kwargs['pos']
        self.w = kwargs['w']
        self.mu = kwargs['mu']
        self.prob = 1
        #self.listOfNodes = {self}
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