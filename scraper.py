import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup
from ContentPartA import Token

def scraper(url, resp, mostCommonWords,icsSubDomains,longestPage,similarURLs):
    links = extract_next_links(url, resp, mostCommonWords,icsSubDomains,longestPage,similarURLs)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp,mostCommonWords,icsSubDomains,longestPage,similarURLs):
    foundLinks = list()
    if (".ics.uci.edu" in url) or (".cs.uci.edu" in url) or (".informatics.uci.edu" in url) or (".stat.uci.edu" in url) or ("today.uci.edu/department/information_computer_sciences" in url):
        if (resp.status >= 600 and resp.status <=606):
            print(resp.error)
        if (resp.status >=200 and resp.status <=599):
            if (resp.status >=400 and resp.status <=599):
                frontURL = url.split("?")[0]
                if frontURL not in similarURLs:
                    similarURLs[frontURL] = 1
                else:
                    similarURLs[frontURL] += 1
            else:
                if (resp.raw_response is not None):
                    #Beautiful Soup Object --------------------------------------------------------------------------------------------------
                    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                    content = Token()                                   #our Token Object
                    content.tokenizeFile(soup)                          #tokenize to get list of tokens
                    contentLen = len(content.tokenList)                 #amount of words/tokens in that link's html content
                    #Checks
                    if (contentLen >= 300 and contentLen <= 5000):      #filtering out webpages with too little info or too much(very large) info
                        content.computeWordFreq()                     
                        if(content.top3Freq/contentLen <= 0.5):         #assert top 3 words dont make up more than 50% of page text/content
                            ##### UPDATE INSTANCE VARIABLES
                            mostCommonWords.update(content.tokenDict)   #update most common words with tokens from current url
                            #FIND LONGEST PAGE
                            if (contentLen > longestPage[1]):
                                longestPage[0] = url
                                longestPage[1] = contentLen
                            ###### CHECK SUBDOMAIN: If the prev 5 chars is not '//www' & not part of query
                            if ('.ics.uci.edu' in url) and (url.split('.ics.uci.edu')[0][-5:] != '//www') and ('?' not in url.split('.ics.uci.edu')[0]):
                                subDomainURL = url.split('.ics.uci.edu')[0] + '.ics.uci.edu'
                                if subDomainURL in icsSubDomains.keys():
                                    icsSubDomains[subDomainURL] += 1
                                else:
                                    icsSubDomains[subDomainURL] = 1
                            
                            #BEGIN TO FIND ALL URLS ON THIS CURRENT WEBPAGE -----------------------------------------------------------------
                            possibleURLs = []
                            # Links: CONTENT TEXT
                            content.findTextURLs(soup)
                            possibleURLs += content.urlList
                            # Links: HREF
                            for aTag in soup.find_all('a'):
                                hreflink = aTag.get('href')
                                if (hreflink is not None) and (hreflink != "#"):
                                    possibleURLs.append(hreflink)
                            ### Go through all found URLs and check if valid
                            curLinkParsed = urlparse(url)
                            for link in possibleURLs:
                                URL = urldefrag(link)[0]                    # Remove FRAGMENT        
                                ### Check for relative links         
                                splitLink = urlparse(link)
                                if splitLink.netloc=="":                    # If netloc missing, add parent netloc
                                    URL = "//"+curLinkParsed.netloc + URL
                                if splitLink.scheme  == "":                 # If scheme missing, add parent scheme
                                    URL = curLinkParsed.scheme + ":" + URL
                                frontURL = URL.split("?")[0]            # Remove QUERY section to check if domain valid
                                if (".ics.uci.edu" in frontURL) or (".cs.uci.edu" in frontURL) or (".informatics.uci.edu" in frontURL) or (".stat.uci.edu" in frontURL) or ("today.uci.edu/department/information_computer_sciences" in frontURL):
                                    ### CHECK FOR URL SIMILARITY HERE
                                    if frontURL not in similarURLs:
                                        similarURLs[frontURL] = 1
                                    else:
                                        similarURLs[frontURL] += 1
                                    
                                    if similarURLs[frontURL] <= 100:        #we have gone to similar ones before, don't go to it again!
                                        foundLinks.append(URL)
                                    else:
                                        print("GREATER THAN 100 ++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                    
    return foundLinks
    #add to a list of subdomains for ics.uci url and increment count for that subdomain
    #TO CHECK :if the link is valid and is not leading to a trap, a similar page,
    # a dead url, a very large file with low info value...?

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if "/pdf" in parsed.path.lower():
            return False
        if "/xml" in parsed.path.lower():
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4|war"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|odc|xml"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

