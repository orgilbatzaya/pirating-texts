'''
Created on Jul 11, 2018

@author: orgil
'''
import csv
import re
import xml.etree.ElementTree
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def named_entities(text):
    # word_tokenize should work well for most non-CJK languages
    words = nltk.word_tokenize(text)
    
    # TODO: this works only for english. Stanford's pos tagger supports
    # more languages
    # http://www.nltk.org/api/nltk.tag.html#module-nltk.tag.stanford
    # http://stackoverflow.com/questions/1639855/pos-tagging-in-german
    # PT corpus http://aelius.sourceforge.net/manual.html
    # 
    pos_tag = nltk.pos_tag(words)
    
    nes = nltk.ne_chunk(pos_tag)
    return nes
    

def find_entities(text):
    """Parse text and tokenize it.
    """
    nes = named_entities(text)

    places = []
    for ne in nes:
        if type(ne) is nltk.tree.Tree:
            if ne.label() in ['GPE', 'PERSON', 'ORGANIZATION']:
                places.append(u' '.join([i[0] for i in ne.leaves()]))

    return places

e = xml.etree.ElementTree.parse('Crusoe_Titles.xml').getroot()

metadata_tags = ['oclc','language','author','title','publisher']
tag_nums = ['035','040','100','245','260']
book_metadata = [['oclc','language','author','title','publisher']]

count = 0

for child in e:
    book_meta = ['None']*5
    for chil in child:
        meta = []
        #if 'tag' in chil.attrib:
        #    print(chil.tag, chil.attrib['tag'])
        if 'datafield' in chil.tag:
            if chil.attrib['tag'] in tag_nums:
                for chi in chil:
                    meta.append(chi.text)
                if chil.attrib['tag'] == '040':
                    meta = meta[1]
                if chil.attrib['tag'] == '035':
                    meta = meta[0][meta[0].find(')')+1:]
                if chil.attrib['tag'] == '100':
                    meta = ' | '.join(meta)
                if chil.attrib['tag'] == '245':
                    meta = ' '.join(meta)
                if chil.attrib['tag'] == '260':
                    print("publishing info: ", meta)
                    meta = ' | '.join(meta)
                print(chil.attrib['tag'] + '\t' + str(meta))
                book_meta[tag_nums.index(chil.attrib['tag'])] = meta
    book_metadata.append(book_meta)
    #if count == 3:
    #    break
    count+=1
    print(count)

#for lst in book_metadata:
#    for item in lst:
#        for it in item:
#            if 'crusoe' in it.lower():
#                print(it)
#    print('next book \n')

ct = 0
for x in book_metadata:
    if re.search('(17|18|19|20)(\\d{2}|\\d(-|\\?))', x[4]):
        i = re.search('(17|18|19|20)(\\d{2}|\\d(-|\\?))', x[4]).start()
        #print(x[4][i:i+4])
    else:
        continue
        #print(x[4])

#print(ct)

for x in book_metadata[1:]:
    locations = find_entities(x[4])
    print(x[4], locations)

with open('crusoeData1.csv', 'w', encoding='utf8', newline='') as myCSV:
    writer = csv.writer(myCSV)
    writer.writerows(book_metadata)