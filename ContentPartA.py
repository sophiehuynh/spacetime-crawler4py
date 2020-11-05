import re
from bs4 import BeautifulSoup 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

class Token:
    def __init__(self):
        self.tokenList = []
        self.urlList   = []
        self.tokenDict = {}
        self.top3Freq  = 0

    # Creates list of words in html content
    def tokenizeFile(self,soup):
        myRE = re.compile(r"[A-Za-z]+")
        currList = re.findall(myRE, soup.get_text()) 
        for word in currList:
            word = word.lower()
            if len(word)>=2 and (word not in stopwords.words('english')):  
                self.tokenList.append(word)

    # Create list of URLs found in text of document
    def findTextURLs(self,soup):
        # https://www.w3resource.com/python-exercises/re/python-re-exercise-42.php REGEX Expression
        self.urlList = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', soup.get_text())


    # Count amt of unique words into dictionary AND sets the top 3 most frequent words in html content
    def computeWordFreq(self):
        for t in self.tokenList:                     
            if t not in self.tokenDict.keys():        
                self.tokenDict[t] = 1
            else:                                               
                self.tokenDict[t] += 1
        try:
            sortedTD = sorted(self.tokenDict.values(),reverse = True)
            self.top3Freq += sortedTD[0]
            self.top3Freq += sortedTD[1]
            self.top3Freq += sortedTD[2]
        except:
            pass