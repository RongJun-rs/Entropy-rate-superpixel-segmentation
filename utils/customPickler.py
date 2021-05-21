import pickle,time,os

dirFile = os.path.dirname(__file__)


path = os.path.join(dirFile)

def save(instance):
    name = instance.__class__.__name__
    timestamp = time.time()
    name_instance = name + "_" + str(timestamp)
    path_instance = os.path.join(path,name_instance)
    pickle.dump(instance ,open(path_instance ,"wb"))

@classmethod
def load(cls):
    return pickle.load(open(cls.path ,"rb"))
