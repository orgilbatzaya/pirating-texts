'''
Created on Jul 5, 2018

@author: orgil
'''
'''
Created on Jun 29, 2018

@author: orgil
'''
import re
import pickle
import requests
import pandas as pd
from bs4 import BeautifulSoup

def writeToCSV(outfile, table):
    with open(outfile, 'w') as f:
        table.to_csv(f, index = False)

def getUFLang(inp):
    langs = []
    for i,url in enumerate(inp):
        url = url + '/00001/citation'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        langtext = soup.find_all(class_= "sbk_CivLANGUAGE_Element")
        if len(langtext) > 1:
            langs.append(langtext[1].get_text())
        else:
            langs.append("")
        print("{} done getting lang from {}, {}".format(i,url,langs[i]))
    print('the length of col is, ',len(langs))
    return langs
    

def getUFCity(inp):
    cities = []
    for i,url in enumerate(inp):
        citiesPerBook = []
        url = url + '/00001/citation'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        citytag = soup.find(class_= "sbk_CivPLACE_OF_PUBLICATION_Element",style="margin-left:180px;")
        if citytag != None:
            for x in citytag:
                citiesPerBook.append(x.get_text().replace(';','').strip())
        cities.append("+".join(citiesPerBook))
        print("{} done getting pubcity from {}, {}".format(i,url,cities[i]))
    
    print('the length of col is, ',len(cities))
    return cities    
    
def getUFOCLC(inp):
    oclcs = []
    for i,url in enumerate(inp):
        url = url + '/00001/citation'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        resourceTag = soup.find(class_= "sbk_CivRESOURCE_IDENTIFIER_Element",style="margin-left:180px;")
        if resourceTag != None:
            containsOCLC = 0
            for x in resourceTag:
                if 'oclc' in x.get_text().lower() and containsOCLC < 1:
                    x = re.sub('[^\d.]+','',x.get_text())
                    oclcs.append(x)
                    containsOCLC += 1
            if containsOCLC == 0:
                oclcs.append('')
        else:
            oclcs.append('')
        print("{} done getting oclc from {}, {}".format(i,url,oclcs[i]))
    
    print('the length of col is, ',len(oclcs))
    return oclcs
            
if __name__ == '__main__':
    ufcsv = 'ufmetadata1.csv'
    tb = pd.read_csv(ufcsv)
    urls = tb['UFDC code']
    langs = getUFLang(urls)
    cities = getUFCity(urls)
    oclcs = getUFOCLC(urls)
    tb['location'] = cities
    tb['oclc'] = oclcs
    tb['language'] = langs
    #pickle.dump(tb, open('table.txt', 'wb'))
    print(tb)
    #tb = pickle.load(open('table.txt', 'rb'))
    outf = 'UFMetadataMaster.csv'
    writeToCSV(outf, tb)
