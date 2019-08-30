'''
Created on May 29, 2018

@author: orgil
'''
import os, shutil, zipfile

# Set the directory you want to start from
rootDir = 'C:\Users\orgil\Downloads\PT\my_dataset\\'
for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname.endswith(".zip"):
            zip_ref = zipfile.ZipFile(dirName + "\\" + fname)
            book = 'C:\Users\orgil\Downloads\PT\\' + dirName.split('\\')[6] +'.'+dirName.split('\\')[-1]
            zip_ref.extractall(book)
            zip_ref.close()


    



        
    