'''
Created on Jun 28, 2018

@author: orgil
'''
import pickle
import re
import nltk
from gensim.models import ldamodel
from nltk.corpus import stopwords
from gensim import corpora
from h11._readers import chunk_size
stop_words = set(stopwords.words('english'))
stop_words.update("would could upon made one two great came might much us man men time little go found well".split())

books = pickle.load(open("bookAbridged_hathi.txt", "rb"))
texts = []
for book in books:
    noPunc = re.sub("[^a-zA-Z]"," ", book.text)
    noPunc = noPunc.lower()
    toks = nltk.word_tokenize(noPunc)
    toks = [t for t in toks if t not in stop_words and len(t) > 2 ]
    texts.append(toks)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

print("starting model creation")
lda = ldamodel.LdaModel(corpus = corpus, num_topics = 50, id2word=dictionary, chunksize = 50, passes = 8)
x = lda.print_topics(-1)
for t in x:
    print(t)