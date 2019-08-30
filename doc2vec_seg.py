'''
Created on Jun 19, 2018

@author: orgil
'''
import pickle
import nltk
import csv
import random
import re
from nltk.corpus import stopwords
from gensim.models import doc2vec as d2v
from collections import namedtuple
from book import book
#from matplotlib import pyplot as plt
#from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
#from ete3 import TreeStyle

np.set_printoptions(precision=5, suppress=True)
# LOADING BOOKS AND PREPROCESSING
def clean(file):
    corpus=[]
    with (open(file, "rb")) as openfile:
        corpus=pickle.load(openfile)
    for book in corpus:
        print(len(book.segList))
        
            
    
    stop_words = set(stopwords.words('english'))
    cleaned = []
    for book in corpus:
        book.text=""
        print(book.title)
        for x in range(0,len(book.segList)):
            
            noPunc = re.sub("[^a-zA-Z]"," ", book.segList[x][1])
            noPunc = noPunc.lower()
            toks = nltk.word_tokenize(noPunc)
            toks = [t for t in toks if t not in stop_words and len(t) > 2]
            toks=tuple(toks)
            cleaned.append((book.title, book.code, book.date,  toks, x))
        print("done cleaning {}".format(book.code))

    
    pickle.dump(cleaned, open('d2v_UFseg.txt', 'wb'))
    

def showMetrics(listOfBookTups):
    
    token_count = sum([len(text[3]) for text in listOfBookTups])
    print("The Hathi corpus + Canon contains {0:,} tokens".format(token_count))
    unique_tokens = set()
    for x in listOfBookTups:
        
        print(x[3])
        unique_tokens.update(set(x[3]))
    print("The Hathi corpus + Canon contains {0:,} unique tokens".format(len(unique_tokens)))


def createLabeledDocs(unlabeled):
    ldocs = []
    analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
    for i, text in enumerate(unlabeled):
        words = text
        tags = [i]
        tags=tuple(tags)
        ldocs.append(analyzedDocument(words, tags))
    
    return ldocs


def createTrainedModel(labeledDocs):
    model = d2v.Doc2Vec(size = 300, window = 15, min_count = 1, dm = 1, workers = 4)
    model.build_vocab(labeledDocs)
    
    for epoch in range(100):
        print("training iteration {}".format(epoch))
        random.shuffle(labeledDocs)
        model.train(labeledDocs, total_examples =model.corpus_count, epochs=model.epochs)
    
    model.save('ufSeg_dm.model')


def viewSimBooks(raw_d, model):
    f = open('sims_ufSeg_dm.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['Source','Target','Weight','Type'])
    
    for i, book in enumerate(raw_d):
        print("the most similar books to [{}] ({}) ({}) are:".
              format(book[0],book[2],book[1]))
        sim_books = model.docvecs.most_similar(i, topn = 100)
        sim_list= []
        for sim_book in sim_books:
            csvinfo = []
            book_id = sim_book[0]
            sim_score = sim_book[1]
            
            for idx, info in enumerate(raw_d):
                if book_id == idx:
                    sim_title = info[0]
                    sim_code = info[1]
                    sim_date = info[2]
            if sim_score > 0.6:
                sim_list.append((sim_score, sim_title, sim_date, sim_code))
                csvinfo.append(book[1])
                csvinfo.append(sim_code)
                csvinfo.append(sim_score)
                csvinfo.append("undirected")
                writer.writerow(csvinfo)

        for x in sim_list:
            print(x)
        print()
    
def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata
from scipy.cluster import hierarchy
def getNewick(node, newick, parentdist, leaf_names):
    if node.is_leaf():
        return "%s:%.2f%s" % (leaf_names[node.id], parentdist - node.dist, newick)
    else:
        if len(newick) > 0:
            newick = "):%.2f%s" % (parentdist - node.dist, newick)
        else:
            newick = ");"
        newick = getNewick(node.get_left(), newick, node.dist, leaf_names)
        newick = getNewick(node.get_right(), ",%s" % (newick), node.dist, leaf_names)
        newick = "(%s" % (newick)
        return newick


if __name__ == '__main__':
    #addCanon()
    #bookObjs = "booksUF.txt"
    
    #books = pickle.load(open("books.txt", "rb"))
    #clean(bookObjs)
    #raw_docs = []
    
    
    with (open('d2v_UFseg.txt', "rb")) as openfile:
        raw_docs=pickle.load(openfile)
        
        
        
   
    
    #showMetrics(raw_docs)
    listOfTextToks = [x[3] for x in raw_docs]
    #listOfTextToks=tuple(listOfTextToks)
    
    docs = createLabeledDocs(listOfTextToks)
    createTrainedModel(docs)
    
    #model = d2v.Doc2Vec.load('uf_dbow.model')
    '''
    stuff=model.docvecs
    print(len(stuff))
    
    dates=[]
    for doc in raw_docs:
        dates.append(doc[2])

    vectors=[]
    for x in range(0,len(stuff)):
        print(stuff[x])
        vectors.append(stuff[x])
    
    matrix = np.array(vectors)
    print(matrix.shape)
    Z = linkage(matrix, 'ward')
    print(Z)
    from scipy.cluster.hierarchy import cophenet
    from scipy.spatial.distance import pdist

    c, coph_dists = cophenet(Z, pdist(matrix))
    print(c)
    from scipy.cluster.hierarchy import fcluster
    max_d = 110
    clusters = fcluster(Z, max_d, criterion='distance')
    print(clusters)
    
    for x in range(0, len(books)):
        books[x].cluster=clusters[x]
    
    with open("books.txt", "wb") as st:
        pickle.dump(books, st)
    
    tree = hierarchy.to_tree(Z,False)
    
    t=ClusterTree(getNewick(tree, "", tree.dist, dates))
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.mode = "c"
    ts.arc_start = -180 # 0 degrees = 3 o'clock
    ts.arc_span = 360
    
    t.show(tree_style=ts)
    
   
    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('date')
    plt.ylabel('distance')
    fancy_dendrogram(
        Z,
        #truncate_mode='lastp',
        #p=40,
        labels=dates,
        orientation="top",
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
        annotate_above=10,  # useful in small plots so annotations don't overlap
    )
    plt.show()
   '''
    #viewSimBooks(raw_docs, model)
