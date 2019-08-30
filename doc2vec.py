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
nltk.download('stopwords')

def clean(file, library):
    # cleans book.text and saves to pickle a dictionary of {book code : [title, date, location, tokens, lat, long]}
    cleaned = {}
    corpus = pickle.load(open(file, "rb"))
    stop_words = set(stopwords.words('english'))
    
    for i,bk in enumerate(corpus):
        book = corpus[bk]
        if book.language.lower() in ['en','eng','english']:
            noPunc = re.sub("[^a-zA-Z]"," ", book.text.lower()) #remove non-alphabetic chars, lowercase
            toks = nltk.word_tokenize(noPunc)
            toks = [t for t in toks if t not in stop_words and len(t) > 2] #remove very short words and stop words
            #if not book.date.isnumeric():
                #book.date = 9999
            cleaned[book.code] = [book.title, book.date, book.location, toks, book.lat, book.long]
            print("done cleaning {} {}- {}".format(book.code,book.language,i))
    
        
    outf = 'd2v_premodel/d2v_' + library + '1.txt'
    pickle.dump(cleaned, open(outf, 'wb'))


def showMetrics(raw_d, library):
    token_count = sum([len(x[3]) for x in raw_d.values()])
    print("The " + library.upper() + " corpus contains {0:,} tokens".format(token_count))
    unique_tokens = set()
    for x in raw_d.values():
        unique_tokens.update(set(x[3]))
    print("The " + library.upper() + " corpus contains {0:,} unique tokens".format(len(unique_tokens)))


def createLabeledDocs(unlabeled):
    # creates required input for gensim's doc2vec algorithm
    # each document must be tagged by its book code 
    ldocs = []
    analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
    for key in unlabeled.keys():
        words = unlabeled[key][3]
        
        tags = [key]
        ldocs.append(analyzedDocument(words, tags))
    return ldocs

from gensim.models.callbacks import CallbackAny2Vec

class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''
    def __init__(self):
        self.epoch = 0
    def on_epoch_end(self,model):
        print("Epoch #{} end".format(self.epoch))
        self.epoch += 1

def createTrainedModel(labeledDocs, model_type, iters, library):
    # saves to pickle a d2v model object 
    if model_type == 'dm':
        mtype = 1
    else:
        mtype = 0
    random.shuffle(labeledDocs)
    epoch_logger = EpochLogger()
    model = d2v.Doc2Vec(documents=labeledDocs,size = 300, epochs = iters,window = 10, 
                        min_count = 10, dm = mtype, workers = 4, callbacks=[epoch_logger])
    
    
    outf = 'd2v_models/' + library + '_' + model_type + '1.model'
    model.save(outf)


def viewSimBooks(raw_d, model, sim_thresh, library, model_type, graph_type, make_nodes):
    # creates a similarity dictionary and builds network csv
    # then for each book, print the similar books which is at least sim_threshold
    sim_dict = getSimDict(raw_d, model)
    createNetworkCSV(sim_dict, sim_thresh, library, model_type, graph_type, make_nodes)
    
    for code in sim_dict.keys():
        title = sim_dict[code][0]
        date = sim_dict[code][1]
        print("the most similar books to [{}] ({}) ({}) with a threshold of {} are:".
              format(code,title,date,sim_thresh))
        for sim in sim_dict[code][-1]:
            if sim[1] >= sim_thresh:
                print(sim,sim_dict[sim[0]][:2])
        print()
    
    
def getSimDict(raw_d, model):
    # returns an augmented dictionary in which a list of similar books is appended
    # to each book's list (value), all else is a deepcopy
    # the list has the form [(sim_code, sim_score),...] 
    import copy 
    sim_dict = copy.deepcopy(raw_d)
    
    for key in sim_dict.keys():
        sim_books = []
        for sim_book in model.docvecs.most_similar(key, topn = 1000):
            sim_code = sim_book[0]
            sim_score = sim_book[1]
            sim_books.append((sim_code, sim_score))
        sim_dict[key].append(sim_books)
    return sim_dict
 
    
def createNetworkCSV(sim_dict, sim_thresh, library, model_type, graph_type, make_nodes):
    #creates two csv's one is an edges table, the other is a nodes table, providing
    #metadata for the books for labelling/visualization purposes
    parts = ['sims', library, model_type, graph_type, str(100*sim_thresh)] 
    outf = open('d2v_results/' + '_'.join(parts) + '.csv', 'w', newline = '')
    writer = csv.writer(outf)
    writer.writerow(['Source', 'Target', 'Weight', 'Type']) #first add header row

    for book in sim_dict.keys():
        date = sim_dict[book][1] #used in directed graphs to compare to earlier/later editions
        for sim_book in sim_dict[book][-1]:
            row = []
            sim_code = sim_book[0]
            sim_score = sim_book[1]
            sim_date = sim_dict[sim_code][1]
            if sim_score >= sim_thresh: # create network csv based on user-specified similarity threshold
            
                if graph_type == 'undirected' or date == sim_date: 
                    row.append(book)
                    row.append(sim_code)
                elif sim_date < date:
                    row.append(sim_code)
                    row.append(book)
                elif date < sim_date: 
                    row.append(book)
                    row.append(sim_code)
    
                row.append(sim_score) # weight
                row.append(graph_type) # 'directed' or 'undirected'
                writer.writerow(row)
    if make_nodes:
        outf = open('d2v_results/' + '_'.join(parts) + '_nodes.csv', 'w', newline = '', encoding='utf-8')
        writer = csv.writer(outf)
        writer.writerow(['ID', 'Label','Title','Date','Lat','Long']) #first add header row
        for book in sim_dict.keys():
            location = sim_dict[book][2]
            title = sim_dict[book][0]
            date = sim_dict[book][1][:4]
            lat = sim_dict[book][4]
            long = sim_dict[book][5]
            writer.writerow([book, location,title, date, lat, long]) # row: code, location, date

def add_country_codes(bigcsv,nodescsv):
    import pandas as pd 
    master = pd.read_csv(bigcsv).set_index('htrc-id')
    nodes = pd.read_csv(nodescsv)
    stuff = []
    for row in nodes['ID']:
        try:
            stuff.append(master['country'][row])
        except KeyError:
            country = ""
            stuff.append(country)
        
    nodes['country'] = stuff
    nodes.to_csv(nodescsv,encoding='utf-8')

if __name__ == '__main__':
    epoch_logger = EpochLogger()

    library = 'all' #'hathi'
    model_type = 'dm' #'dbow'
    iterations = 20
    graph_type = 'directed'
    threshold = .90
    bookObjs = "booksFinal1.txt"
    make_nodes = True
    
    clean(bookObjs, library)
    
    premodel = 'd2v_premodel/d2v_' + library + '1.txt'
    bookDict = pickle.load(open(premodel, 'rb'))
    showMetrics(bookDict, library)
    
    labeledDocs = createLabeledDocs(bookDict)
    
    import time
    start = time.time()
    
    createTrainedModel(labeledDocs, model_type, iterations, library)
    
    mdl = 'd2v_models/' + library + '_' + model_type + '1.model'
    model = d2v.Doc2Vec.load(mdl)
    
    viewSimBooks(bookDict, model, threshold, library, model_type, graph_type, make_nodes)
    
    end = time.time()
    print(end-start)
    
    
    big = 'metadata/crusoeMaster3.csv' #our base dataset which contains country codes
    small = 'd2v_results/sims_all_dm_directed_90.0_nodes.csv' #created from viewSimBooks

    add_country_codes(big, small)
    
    

    


