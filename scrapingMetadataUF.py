'''
Created on Jun 5, 2018

@author: orgil
'''
import requests, re
from bs4 import BeautifulSoup
import pandas as pd 


url = 'http://ufdc.ufl.edu/defoe/all/brief'
codes = []
titles = []
dates = []
locs = []


for p in range(1,15):
    if p == 1:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        newurl = url + '/' + str(p) 
        page = requests.get(newurl)
        soup = BeautifulSoup(page.content, 'html.parser')
   
    for x in soup.find_all(class_= 'briefResultsTitle'):
        titles.append(x.get_text())
        anchor = x.find('a')
        code = anchor.get('href', None)
        codes.append(code)
        
    for x in soup.find_all(class_="sbkBrv_SingleResultDescList"):
        stuff = "".join(x.get_text())
        label = stuff.split("\n")[1].split(": ")[0]
        val = stuff.split("\n")[1].split(": ")[1]
        if not label == "Publication Date":
            dates.append("")
        else:
            val = val.replace("-?", "5")
            val = re.sub("\D"," ", val)
            if len(val.split()) > 1:
                cnt = 0
                for v in val.split():
                    cnt += int(v)
                val = cnt/len(val.split())
            dates.append(val)
        
    for x in soup.find_all(class_="sbkBrv_SingleResultDescList"):
        stuff = "".join(x.get_text())
        if len(stuff.split("\n")) > 3:
            pubinfo = stuff.split("\n")[3]
        else:
            pubinfo = ""
        
        if pubinfo.split(":")[0] == "Publisher":
            loc = re.findall('\(([^\)]+)\)', pubinfo.split(":")[1])
            for x in range(len(loc)):
                loc[x] = loc[x].split('(')[0]
            locs.append(loc)
        else:
            locs.append("")
        
   
brief = pd.DataFrame({
    "UFDC code": codes,
    "title": titles,
    "publication date": dates,
    "location": locs})
brief.to_csv(r'C:\Users\orgil\RC\newrc\ufmetadata1.csv')

def clean_dates(csv):
    tbl = pd.read_csv(csv)
    tbl = pd.DataFrame(tbl)
    dates = tbl["publication date"]
    for d in dates:
        d = d.replace("-?", "5")
        d = re.sub("\D"," ", d)
        print(d)
    #tbl.to_csv('ufmetadata1.csv')
            
    









    
    
    