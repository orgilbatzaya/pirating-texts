'''
Created on May 30, 2018

@author: Lucian
'''
import os
from fnmatch import fnmatch
import zipfile
##location of database
root = 'C:/Users/Lucian/Desktop/nongoogle'
pattern = "*.zip"
count=0

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            print(os.path.join(path, name));
            library=os.path.join(path, name).split("\\")[1]
            fileNum=os.path.basename(os.path.join(path, name)).split(".")[0]
            zip_ref = zipfile.ZipFile(os.path.join(path, name), 'r')
            ##location where you want unzipped files to go, use same location for concatenateFiles
            zip_ref.extractall("C:/Users/Lucian/Desktop/unzipped2/"+library+"."+fileNum)
            zip_ref.close()
            
            count+=1
            
print(count)

'''
import glob
import zipfile
path = 'C:/Users/Lucian/Desktop/google'
print(os.listdir(path))
def traversePath(filepath):
    
    if glob.glob(os.path.join(path, '*.zip')):
        return glob.glob(os.path.join(path, '*.zip'))
    else
        return
        
print("test")
for filename in glob.glob(os.path.join(path, '*.zip')): 
    print(filename)
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall("C:/Users/Lucian/Desktop/unzipped"+filename)
    zip_ref.close()
'''
