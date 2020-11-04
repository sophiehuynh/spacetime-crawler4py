import re
from bs4 import BeautifulSoup 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

class Token:
    def __init__(self):
        self.tokenList = []
        self.tokenDict = {}
        self.top3Freq = 0

    #creates list of words in html content
    def tokenizeFile(self,soup):
        myRE = re.compile(r"[A-Za-z]+")
        currList = re.findall(myRE, soup.get_text()) 
        for word in currList:
            word = word.lower()
            if len(word)>=2 and (word not in stopwords.words('english')):  
                self.tokenList.append(word)

    #count amt of unique words into dictionary AND sets the top 3 most frequent words in html content
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