'''
Created on Jun 29, 2018

@author: orgil
'''
import csv 
import re
import string
from fuzzywuzzy import fuzz

'''
Cleaning the final CSV file that contains all editions we have, text or no text, in which 
columns are library-id, pubcity, pubyear, 
title, oclc, language, hasText, latitude, longitude
'''

def removeDupRows(inp):

    originalLen = 0
    with open(inp, newline = '', encoding = 'utf-8', errors = 'replace') as csvfile:
        readerObj = csv.reader(csvfile)
        uniqueRows = set()
        for i,row in enumerate(readerObj):
            if i == 0:# deal with first row separately (col names)
                originalLen += 1
                colNames = row
            else:
                originalLen += 1
                uniqueRows.add(tuple(row))
        print('There are {} unique rows. Removed {} rows from original.'.
              format(len(uniqueRows), originalLen-len(uniqueRows)))
        
        res = [tuple(colNames)] + list(uniqueRows)
        return res
            
            
def cleanPubYear(inp):
    
    doubleDashCount = 0
    singleDashCount = 0
    ambig = []
    res = []
    pattern = re.compile('^\d\d\d$')
    for x in inp:
        year = x[2]
        if year.count('-') == 1 or pattern.search(year) != None:
            print(year, x[4])
            year = year.replace('-', '5')
            lst = list(x)
            lst[2] = year
            x = tuple(lst)
            res.append(x)
            singleDashCount += 1 
        elif year.count('-') >= 2:
            print(year, x[4])
            doubleDashCount += 1
        else:
            res.append(x)
    print('Removed {} rows with unknown year. There are {} rows left. Corrected {} rows missing last digit.'
          .format(doubleDashCount, len(res), singleDashCount))
    
    return res
    
def getActualCrusoe(inp):
    count = 0
    almostcnt = 0
    res = []
    res.append(inp[0]) #column names
    for row in inp[1:]:
        title = row[3]
        if row[4] == '908981015': #special tamil rapinsan krusoe
            res.append(row)
        if "robinson" in title.lower():
            count += 1
            res.append(row)
        else:
            for word in title.lower().split():
                robSimilarity = fuzz.ratio(word, 'robinson')
                if robSimilarity > 60:
                    almostcnt += 1
                    res.append(row)
                    print(word, row[4], robSimilarity)
    print('''There are {} titles containing robinson and 
            {} that are close to robinson. We have {} acceptable titles'''
            .format(count, almostcnt+1, count+almostcnt+1))
    return res

def cleanPubCity(inp):
    uncleanCnt = 0
    res = []
    for row in inp:
        city = row[1]
        cleanCity = ''.join(c for c in city if c not in string.punctuation)
        if cleanCity != city:
            uncleanCnt += 1
        lst = list(row)
        lst[1] = cleanCity
        res.append(tuple(lst))
    print("Cleaned {} cities containing punctuation".format(uncleanCnt))
    return res

def cleanBigPubs(inp):
    for item in inp:
        pubinfo = item.split('|')
        
def writeNewCSV(inp, fp):
    with open(fp, 'w', newline = '', encoding = 'utf-8') as outCSVFile:
        writer = csv.writer(outCSVFile)
        for row in inp:
            writer.writerow(row)
            
if __name__ == '__main__':
    #csvfile = 'crusoeData.csv'#'RobinsonCrusoeEditionsPlus.csv'
    csvfile = 'RobinsonCrusoeEditions.csv'
    rows = removeDupRows(csvfile)
    rows = getActualCrusoe(rows)
    rows = cleanPubYear(rows)
    #rows = cleanPubCity(rows)
    #newCSV = 'trial1.csv'
    #writeNewCSV(rows, newCSV)
    
    
