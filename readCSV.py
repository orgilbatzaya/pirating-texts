'''
Created on May 31, 2018

@author: Lucian, Orgil
'''
import os
import csv
import pickle
import string
from book import book
from fuzzywuzzy import fuzz, process
'''
Given a master CSV containing metadata for editions of Robinson Crusoe and a 
directory of all our .txt editions, builds a dictionary of book objects through cross-reference.
If a book doesn't exist in the CSV(controlling for duplicates), it will not be processed.
Also writes to new CSV a copy of the old but with a new and improved hasText column
Returns a PICKLED DICTIONARY of BOOK OBJECTS.
IMPORTANT: after running this module, run abridge.py to cut out extraneous text before and after the 
"actual" text such as publisher's info and different books
'''
bookDir = "editions1500" #directory of our entire collection of scraped books from UF, Hathi, and Internet Archive
codeList = os.listdir(bookDir) 

bookList = []
bookDict = {}

strictWL = string.ascii_letters + "\'"
whiteList = string.ascii_letters + string.digits+ " "+"."+"\n"+"\'"
noCodeCount = 0
text = ""

with open("metadata/crusoeMaster3.csv", 'r',encoding='utf-8', ) as csvfile, open('crusoeMaster3HasText.csv', 'w',encoding='utf-8') as out:
    writer = csv.writer(out,lineterminator = '\n')
    reader=csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in reader: #first iterates through all rows in csv
        hasCode=False 
        row[6] = 0 # by default hasText entry
        csvCode=row[0].replace("\"", "")
        for code in codeList: #then for each row, iterate through entire collection, checking if we have it
            codeFirst = code.split(".txt")[0]
            codeFirst=codeFirst.replace("+",":") # difference in file system naming and csv
            codeFirst=codeFirst.replace("=","/")
                
            if csvCode==codeFirst:#copies CSV contents to book object if code matches 
                hasCode=True
                row[6]=1
                title=row[3].replace("\"", "")
                date=row[2].replace("\"", "")
                language=row[5].replace("\"", "")
                lat=row[7].replace("\"", "")
                long=row[8].replace("\"", "")
                oclc=row[4].replace("\"", "")
                city=row[1].replace("\"", "")
                try:
                    country=row[9]
                except:
                    country="none"
                    print("not found")
                    
        writer.writerow(row)
        if not hasCode and csvCode != "None":
            print("not found ", csvCode)
            noCodeCount+=1
            continue
            
        if hasCode:
            codeFileSys = csvCode.replace(":","+").replace("/","=") + '.txt'
            with open(bookDir+"/"+codeFileSys, encoding='utf-8', errors='ignore') as myfile:
                data = myfile.read().lower() # set to lowercase
            d = {}
            final = ' '
            count = 0
            #Uses ted underwood common errors to correct text
            with open('CorrectionRules.txt', 'r', encoding='utf-8') as myfile:
                fixes = myfile.read()
                lst = fixes.split('\n')
    
                for item in lst:
                    x = item.split()
                    d[x[0]] = x[1]
    
            fix=data.split(" ")
            for x, word in enumerate(fix):
                if word in d:
                    count+=1
                    fix[x] = d[word]
            fixed=' '.join(fix)
            data = ''.join(c if c in whiteList else " " for c in fixed)
            
            currentBook=book(title, date, city, language, csvCode, lat, long, oclc, country, data)
            bookList.append(currentBook)
            currentBook.printMe()
            print(count)
            
    #convert bookList to dict
    for book in bookList:
        bookDict[book.code]=book
    
    print(noCodeCount) #creates new pickle file and saves bookDict for future use
    with open("booksFinal.txt", "wb") as fp:   #Pickling
        pickle.dump(bookDict, fp)
        
