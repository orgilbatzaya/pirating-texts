'''
Created on Jul 9, 2018

@author: orgil
'''
import gensim.models.doc2vec as d2v
import doc2vec
import re
from nltk.corpus import stopwords
import nltk
from scipy import spatial
import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


def doPCA(fp):
    model = d2v.Doc2Vec.load(fp)
    segmentVectors = model.docvecs
    pca = PCA(n_components = 2)
    stuff = pca.fit(segmentVectors).transform(segmentVectors)
    for x in model.docvecs:
        print(x)
def testingSplitHypothesis(f):
    '''V(first half of book) + V(second half of book) ~ V(entire book)'''
    stop_words = set(stopwords.words('english'))
    cleaned = []
    with open(f, 'r') as book:
        text = book.read()
    noPunc = re.sub("[^a-zA-Z]"," ", text).lower()
    toks = nltk.word_tokenize(noPunc)
    toks = [t for t in toks if t not in stop_words and len(t) > 2]
    half = int(len(toks)/2)
    cleaned.append(toks[:half])
    cleaned.append(toks[half:])
    cleaned.append(toks)
        
    docs = doc2vec.createLabeledDocs(cleaned)
    doc2vec.createTrainedModel(docs)
    model = d2v.Doc2Vec.load('d2vModels/test.model')
    total = model.docvecs[0] + model.docvecs[1]
    
    x = spatial.distance.cosine(total, model.docvecs[2])
    print(math.cos(x))

if __name__ == '__main__':
    f = 'uf/canonical2.txt'
    #testingSplitHypothesis(f)
    fmodel = 'C:\Users\orgil\Downloads\segmentation_doc2vec\hathi_dbow.model'
