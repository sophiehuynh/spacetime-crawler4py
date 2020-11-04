import re
from bs4 import BeautifulSoup 


class Token:
    def __init__(self):
        self.tokenList = []
        self.tokenDict = {}
        self.top3Freq = 0


    def tokenizeFile(self,soup):
        myRE = re.compile(r"[A-Za-z]+")
        ### Call re.findall on the whole big string
        currList = re.findall(myRE, soup.get_text()) 
        for word in currList:
            word = word.lower()
            if len(word)>=2:  
                self.tokenList.append(word)
        ######## IGNORE STOP WORDS


    def computeWordFreq(self):
        for t in self.tokenList:                     
            if t not in self.tokenDict.keys():        
                self.tokenDict[t] = 1
            else:                                               
                self.tokenDict[t] = self.tokenDict[t] + 1
        try:
            self.top3Freq += sorted(self.tokenDict.values(),reverse = True)[0]
            self.top3Freq += sorted(self.tokenDict.values(),reverse = True)[1]
            self.top3Freq += sorted(self.tokenDict.values(),reverse = True)[2]
        except:
            pass