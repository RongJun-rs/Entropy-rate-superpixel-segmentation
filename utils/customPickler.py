import pickle

def save(self):
    pickle.dump(self ,open(self.path ,"wb"))
@classmethod
def load(cls):
    return pickle.load(open(cls.path ,"rb"))
# TODO : add mixin for saving and loading of instance of class at particular state