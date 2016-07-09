import cPickle as pickle
import os.path

def dumptwts(twts, green):
    pickle.dump(twts, open("savetwts.p", "wb"))
    pickle.dump(green, open("greentwts.p", "wb"))
    
def loadtwts():
    twts = []
    if os.path.isfile("savetwts.p"):
        twts = pickle.load(open("savetwts.p", "rb"))
    if os.path.isfile("greentwts.p"):
        greentwts = pickle.load(open("greentwts.p", "rb"))
    return twts
