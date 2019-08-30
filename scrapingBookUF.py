'''
Created on Jun 6, 2018

@author: orgil
'''
# encoding: utf-8
from bs4 import BeautifulSoup
from unidecode import unidecode
import requests, os, pickle, pytesseract
import OCRcleaning
import sys

sys.stdout.flush()
'''
Requires Tesseract OCR engine and pytesseract wrapper.
Scrapes books from http://ufdc.ufl.edu/defoe/all/thumbs/
and downloads pages as .txt files
end result is a 'uf' directory which has a subdirectory for each book in the collection
each subdirectory contains all of the pages for the book as .txt files
'''

def get_links(url):
    #Goes through 15 pages of linked thumb nails and returns a list of links   
    links = []
    for i in range(1,15):
        if i == 1:
            page = requests.get(url)
        else:
            newurl = url + str(i) 
            page = requests.get(newurl)
            
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find(class_= 'sbkPrsw_ResultsPanel')
        tags = table.findAll('a')
        for tag in tags:
            x = tag.get('href', None)
            links.append(x + "/00001" )
            print(x)

    print(len(links)) #verify 279
    return links

def get_pages(url):
    #for each book's url, return a list of image filepaths which each represent a page from the book
    pages = [] #stores the links to get to the page's page
    pictures = [] #stores urls for the actual full size images 
    newurl = url +"/thumbs?nt=-1" #view all thumbs on the same page
    page = requests.get(newurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    thumbs = soup.find_all(class_= "sbkRi_Thumbnail")
    
    for x in range(len(thumbs)):
        if 'http://ufdc.ufl.edu/UF00053424/00001/thumbs?nt=-1' == newurl and x == 220:
            break #this book was over 1000 pages and contained different novels so its cut off
        site = thumbs[x].find('a')
        fimg = site.get('href')
        pages.append(fimg)
            
    for i in range(len(pages)):
        page = requests.get(pages[i])
        soup = BeautifulSoup(page.content, 'html.parser')
        pic = soup.find(itemprop = "primaryImageOfPage")
        piclink = pic.get('src')
        pictures.append(piclink)
    
    print("done getting pages - " +url)
    return pictures

def download_files(pageUrls):
    #downloads the pages for ONE book into its own directory
    #calls OCRCleaning which cleans and preprocesses the image in prep for OCR
    #
    target = 'uf' #folder which will contain all UF books sub-folders
    f1 = pageUrls[0].split(".edu/")
    f2 = f1[1].split('/')
    f3 = "".join(f2[:5])
    print("starting download/ocr - " + f3)
    os.mkdir(target + '/' + f3)
    
    for pg in pageUrls:
        picpath = f2[6]
        print(picpath)
        with open(target + '/' + f3 + '/' + picpath, "wb") as img_handle:
            img_data = requests.get(pg)
            img_handle.write(img_data.content)
            img_handle.close()
        
        with open(img_handle.name, "rb") as f:
            try:
                cleaned = OCRcleaning.process_image_for_ocr(f)
            except OSError:
                cleaned = f
            img_handle.close()
        
        with open(img_handle.name.split('.')[0] + '.txt', 'w') as clean_handle:
            os.remove(img_handle.name)
            text = pytesseract.image_to_string(cleaned) # Uses Tesseract OCR to convert image's contents to string
            text = unidecode(text)
            clean_handle.write(text)

    print("done downloading/ocr - " + f3)
    
if __name__ == '__main__':

    url = 'http://ufdc.ufl.edu/defoe/all/thumbs/'

    links = get_links(url)
    
    pickle.dump(links, open("picklelinks.txt", "wb"))
    
    booklinks = pickle.load(open('picklelinks.txt','rb'))
    
    #books is a list of lists of image file paths
    books = [get_pages(booklinks[x]) for x in range(len(booklinks))]
    
    for b in books:
        download_files(b)
            
    
                        
    
