import sys
import re
import bs4 from BeautifulSoup

#My Token Class with variables and methods
class Token:
    def __init__(self):
        self.tokenList = []
        self.tokenDict = {}
        self.maxFreq = 0

    '''
        Linear Complexity of O(n) 
            -> two for loops but still just reads through file once so O(n)
                -> First for-loop loops through each line
                -> Second for-loop loops through each word, split by spaces
            -> append is O(1)
            -> lower,strip  is O(n)
    '''
    def tokenizeFile(self,soup):
        myRE = re.compile(r"[A-Za-z0-9]+")                   #compiles my RE for faster runtime for later use
        for line in soup.get_text():
            currentLine = line.strip()                   #remove empty space at begin and end of line
            currList = re.findall(myRE, currentLine)     #find all tokens that match my RE, splitting at nonalphanum chars
            for word in currList:
                word = word.lower()
                if len(word)>=2:                 #ensure no empty strings added to tokenList
                    self.tokenList.append(word)


    '''
        Linear Complexity O(n) 
            -> one for-loop that iterates through each item/word in list is O(n)
            -> not in dictionary.keys() worst case is O(n)
            -> index is O(1)
    '''
    def computeWordFreq(self):
        for t in self.tokenList:                                 #for each token in list
            if t not in self.tokenDict.keys():                   #if DNE yet in dict, add and set value = 1
                self.tokenDict[t] = 1
            else:                                                #if Exists in dict already, add 1 to its value (freq)
                self.tokenDict[t] = self.tokenDict[t] + 1
        maxFreq = sorted(tokenDict.values(),reverse = True)[0]






        





        
