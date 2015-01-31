import cPickle as pickle
import os.path

def dumptwts(twts):
    pickle.dump(twts, open("savetwts.p", "wb"))

def loadtwts():
    twts = []
    if os.path.isfile("savetwts.p"):
        twts = pickle.load(open("savetwts.p", "rb"))
    return twts
