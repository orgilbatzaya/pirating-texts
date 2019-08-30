


from fuzzywuzzy import fuzz 
import nltk
nltk.download('punkt')
from nltk import sent_tokenize
from book import book
import pickle

def getBooks(pickledFile):
    #bookList = []
    with open(pickledFile, "rb") as fp:
            bookList = pickle.load(fp)
    #canon = ""
    for book in bookList:
        if book.code == "canonical2":
            canon = book.text
    return bookList, canon

def doStuff(bookList, canon):
    canonSents = sent_tokenize(canon)
    for i, book in enumerate(bookList):
        bLength = len(book.text)
        hasSent = [0] * len(canonSents)
        for x in range(0, len(canonSents)):
            parts = [book.text[i:i+int(bLength/15)] for i in range(0, bLength, int(bLength/15))]
            for p in parts:  
                part = fuzz.partial_ratio(canonSents[x], p)
                if(part > 80):
                    hasSent[x] = 1
                    #print(canonSents[x])
        print('{} finished comparing sentences of 1919 Gutenberg to {}'.format(i,book.code))
        print(hasSent)
        book.sentList = hasSent

    with open("bookAbridged.txt", "wb") as fp:   #Pickling
        pickle.dump(bookList, fp)

if __name__ == '__main__':
    f = "bookAbridged.txt"
    #lst, canon = getBooks(f)
    #doStuff(lst, canon)
    
        