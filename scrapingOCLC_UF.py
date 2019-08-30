'''
Created on Jun 19, 2018

@author: orgil
'''
import pandas as pd
from bs4 import BeautifulSoup
import requests, pickle

path = 'ufmetadata2.csv'
tb = pd.read_csv(path)
codes = tb['UFDC code']
'''
oclcs = []

for x in codes:
    per = []
    url = x + '/00001/citation'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for y in soup.find_all("span", itemprop = "identifier"):
        per.append(y.get_text())
    oclcs.append(per)
    
pickle.dump(oclcs, open("OCLC.txt", "wb"))'''
list1 = pickle.load(open("OCLC.txt", "rb"))
print(len(list1))
almost = []
for x in list1:
    sub = []
    count = 0
    for y in x:
        if "oclc" in y.lower():
            sub.append(y)
            count += 1
    if count == 0:
        sub.append("")
    almost.append(sub)

clean = []
for x in almost:
    count = 0
    for y in x:
        if "oclc" in y.lower() and count < 1:
            st = ''.join(ch for ch in y if
                          ch.isdigit())
            clean.append(st.strip())
            count +=1 
    if count == 0:
        clean.append("")
tb['oclc'] = clean

  
print(tb)         
with open('ufmetadata3.csv', 'w') as f:
    tb.to_csv(f, index = False) 

    
    