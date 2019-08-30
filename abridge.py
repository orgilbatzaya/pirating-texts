'''
Created on May 31, 2018

@author: Lucian
'''
import os
import csv
import pickle
import string
from book import book
from fuzzywuzzy import fuzz, process

'''
IMPORTANT: make sure readCSV has been run and the pickle object exists before running this
This module cuts down extraneous pieces of text before and after the actual text of each book
Returns a modified final book dictionary that is used in all of our further analyses
'''

count=0
prefaceStart="ever private man"
novelStart = "born year 1632, city York"
novelEnd="farther account years part"
endText="the end"
secondLine="homely proverb England bone"
count = 0
endCount=0
bookDict={}

#unpickle saved book objects
with open("booksFinal.txt", "rb") as fp:
    bookDict=pickle.load(fp)
    
print(len(bookDict))
for code in bookDict:
    textList=bookDict[code].text.split('\n') #split by newlines
    endLoc=len(bookDict[code].text)
    endStr=""
    for part in textList:
        endScore=fuzz.token_set_ratio(secondLine, part) #levenshtein distance score
        
        if endScore>70 and len(part)>20 : #threshold
            endLoc=bookDict[code].text.find(part)
            endStr=part
            endCount+=1
            
    if endLoc/(len(bookDict[code].text)+1)>0.4:
        print(endStr+" "+bookDict[code].code+" "+str(endLoc/len(bookDict[code].text)))
        bookDict[code].hasBook2=True        
        bookDict[code].text=bookDict[code].text[:endLoc]
    for part in textList:
        
        prefaceScore = fuzz.token_set_ratio(prefaceStart, part)
        novelScore = fuzz.token_set_ratio(novelStart, part)
        if prefaceScore > 70 and len(part) > 12:
            bookDict[code].hasPreface=True
            
        elif novelScore> 60 and len(part) > 12:
            startLoc=bookDict[code].text.find(part)
            ##print(part+" "+book.code+" "+str(novelScore))
            bookDict[code].text=bookDict[code].text[startLoc:]
            count+=1
            break
        
print(count)
print(endCount)
with open("booksFinal.txt", "wb") as fp:   #Pickling
    pickle.dump(bookDict, fp)

