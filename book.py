'''
Created on May 31, 2018

@author: Lucian
'''

class book:
    '''
    For each book, create an object
    '''


    def __init__(self, title, date, location, code, oclc, text, sents):
        '''
        Constructor
        '''
        self.title=title
        self.date=date
        self.location=location
        self.code=code
        self.oclc=oclc
        self.text=text
        self.sentList = sents
        self.segList = []
        
    def printMe(self):
        print("Title: "+self.title)
        print("Location: "+self.location)
        print("Code: "+ self.code)
        print("Date: "+self.date)
        print("OCLC: "+self.oclc)