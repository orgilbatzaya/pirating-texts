


import glob
import os
import codecs
from fuzzywuzzy import fuzz, process

##your file location of unzipped folders
path = r"C:\Users\orgil\p_projects\rc\uf\uf-combined"
books = os.listdir(path)

for book in books:
    textfiles = os.listdir(path + "\\" + book)
    firstLineList = []
    
    ##file location where you want to place the concatenated txt files
    with open("uf"+ "/" + book + ".txt", 'w') as outfile:
        for txtfile in textfiles:
            print(txtfile)
            fullName = path + "/" + book + "/" + txtfile
            headerStatus=False
            
            with codecs.open(fullName, "r",encoding='utf-8', errors='ignore') as infile:
                lineNum=0
                for line in infile:
                    if(lineNum==0):
                        for firstLine in firstLineList:
                            if(fuzz.ratio(firstLine,line)>60 and len(line)>5):
                                headerStatus=True
                                print(line)
                                break
                           
                        firstLineList.append(line)
                    try:
                        if(lineNum==0):
                            if(headerStatus==False):
                                outfile.write(line)
                        else:
                            outfile.write(line)
                    except UnicodeEncodeError:
                        if(lineNum==0):
                            if(headerStatus==False):
                                charList=list(line)
                                
                                for char in charList:
                                    try:
                                       outfile.write(char) 
                                    except UnicodeEncodeError:
                                       pass
                                pass
                        else:
                            charList=list(line)
                            for char in charList:
                                try:
                                    outfile.write(char) 
                                except UnicodeEncodeError:
                                    pass
                                pass
                    lineNum+=1