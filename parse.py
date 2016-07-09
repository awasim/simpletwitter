import os,json 
import numpy as np
import cPickle as pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from pprint import pprint

datadir = "/home/additivity/tweets/data/js/tweets"

class_str_lst = []
classification = []
def get_classifier_str():
    for afile in sorted(os.listdir(datadir)):

        #if ((afile != "parse.js") and (afile != "parse.py")):
        print afile
        if "2015" in afile:
            bfile = open(datadir + os.sep + afile, 'r').read()
            bfile = bfile.split("\n")[1:]
            cfile = []
            for line in bfile:
                cfile.append(line + "\n") 
            bfile = "".join(cfile)

            data = json.loads(bfile.encode('utf-8'))
            for i in data:
                print i["text"]
                clas = input("Classify: ")
                classification.append(clas)
                class_str_lst.append(i["text"])
        
if __name__ == "__main__":
    get_classifier_str()
    print len(class_str_lst)
    cv = CountVectorizer(input="content")
    features = cv.fit_transform(class_str_lst).toarray()
    predictable = ["Coffee is the best"]
    predictable_feature = np.array(cv.transform(predictable).toarray())
    clf = GaussianNB()
    clf.fit(features, classification)

    prediction = clf.predict(predictable_feature)
    print prediction
