'''
Created on Jun 19, 2018

@author: orgil
'''
from gensim.models import doc2vec as d2v
import pickle, string, nltk, re
#import matplotlib.pyplot as plt
#import seaborn as sns
#import sklearn.manifold
from fuzzywuzzy import fuzz
'''
all_book_vectors_matrix = model.wv.syn0
tsne = sklearn.manifold.TSNE(n_components = 2, 
                             early_exaggeration = 6,
                             learning_rate = 500,
                             n_iter = 20,
                             verbose = True,
                             random_state = 2)
all_book_vectors_matrix_2d = tsne.fit_transform(all_book_vectors_matrix)

# Create a dataframe to record each word and its coordinates.
points = pd.DataFrame(
    [(word, coords[0], coords[1])
        for word, coords in [
            (word, all_book_vectors_matrix_2d[model.vocab[word].index])
            for word in model.vocab
            ]], columns=["book", "x", "y"])

# Preview the points
points.head()

# Display the layout of all of the points.
sns.set_context("poster")
points.plot.scatter("x", "y", s=10, figsize=(10, 6))

def plot_region(x_bounds, y_bounds):
    Plot a limited region with points annotated by the word they represent.
    slice1 = points[(x_bounds[0] <= points.x) & (points.x <= x_bounds[1]) & 
                   (y_bounds[0] <= points.y) & (points.y <= y_bounds[1])]
    
    ax = slice1.plot.scatter("x", "y", s=35, figsize=(10, 6))
    for i, point in slice.iterrows():
        ax.text(point.x + 0.005, point.y + 0.005, point.word, fontsize=11)

plot_region(x_bounds=(-3.3, -2.7), y_bounds=(0.2, 0.4))

# Find the coordinates for (Tom) Sawyer - The Adventures of Tom Sawyer


#points[points.word == 'Sawyer']

plot_region(x_bounds=(-4.5, -3.5), y_bounds=(0.5, 1))'''
'''books = pickle.load(open("bookAbridged.txt", "rb"))
for x in books:
    if x.code == "UF00073604":
        print(x.text[:-100])'''
'''
Created on Jun 22, 2018

@author: Lucian
'''
        
'''
import csv
weights=[]
with open('sims_uf_dbow.csv', 'r') as inp, open('sims_uf_dbow1.csv', 'w') as out:
   writer = csv.writer(out,lineterminator = '\n')
   for row in csv.reader(inp):
       
       if row[0]+row[1] not in weights:
           writer.writerow(row)
           
       else:
           print(row)
       weights.append(row[1]+row[0])
'''
books = pickle.load(open('bookAbridged.txt', 'rb'))
print(len(books))

