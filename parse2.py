import os,json 
import cPickle as pickle
import nltk

datadir = "/home/additivity/tweets/data/js/tweets"

class_str_lst = []
classification = []
twts = []
texttwts = []

def get_classifier_str():
    for afile in sorted(os.listdir(datadir)):

        if ((afile != "parse.js") and (afile != "parse.py")):
            bfile = open(datadir + os.sep + afile, 'r').read()
            bfile = bfile.split("\n")[1:]
            cfile = []
            for line in bfile:
                cfile.append(line + "\n") 
            bfile = "".join(cfile)

            data = json.loads(bfile.encode('utf-8'))
            for i in data:
                a = dict()
                a[i['user']['screen_name']] = i["text"]
                class_str_lst.append((a, "good"))

def get_bad_tweets():
    twts = pickle.load(open("savetwts.p", "rb"))
    for i in twts:
        #texttwts.append((i['text'], "bad"))
        a = dict()
        a[i['user']['screen_name']] = i["text"]
        class_str_lst.append((a, "bad"))

                
if __name__ == "__main__":
    get_classifier_str()
    get_bad_tweets()
    classifier = nltk.NaiveBayesClassifier.train(class_str_lst)
    print classifier.classify({"somestr": "This is a test"})
