'''
Created on May 30, 2018

@author: orgil
'''
import glob
import os
import codecs
from os import listdir

upperNames = os.listdir("C:\Users\orgil\Downloads\PT\my_dataset_books")
print(upperNames)
for fileName in upperNames:
    filenames=os.listdir("C:\Users\orgil\Downloads\PT\my_dataset_books\\"+fileName+"\\"+fileName.split(".")[1])
    print(filenames)
    with open("C:\Users\orgil\Downloads\PT\\books_combined\\"+fileName+".txt", 'w') as outfile:
        for fname in filenames:
            print(fname)
            fullName="C:\Users\orgil\Downloads\PT\my_dataset_books\\"+fileName+"\\"+fileName.split(".")[1]+"\\"+fname
            with codecs.open(fullName, "r",encoding='utf-8', errors='ignore') as infile:
                for line in infile:
                    try:
                        outfile.write(line)
                    except UnicodeEncodeError:
                        charList=list(line)
                        
                        for char in charList:
                            try:
                               outfile.write(char) 
                            except UnicodeEncodeError:
                               pass
                        pass

