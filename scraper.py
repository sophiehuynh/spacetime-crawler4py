import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup
from ContentPartA import Token

def scraper(url, resp, mostCommonWords,icsSubDomains,longestPage):
    links = extract_next_links(url, resp, mostCommonWords,icsSubDomains,longestPage)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp,mostCommonWords,icsSubDomains,longestPage):
    foundLinks = list()
    if (".ics.uci.edu" in url) or (".cs.uci.edu" in url) or (".informatics.uci.edu" in url) or (".stat.uci.edu" in url) or ("today.uci.edu/department/information_computer_sciences" in url):
        if (resp.status >= 600 and resp.status <=606):
            print(resp.error)
        if (resp.status >=200 and resp.status <=599):
            if (resp.status >=400 and resp.status <=599):
                pass
            else:
                if (resp.raw_response is not None):
                    #Beautiful Soup Object
                    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                    content = Token()                                   #our Token Object
                    content.tokenizeFile(soup)                          #tokenize to get list of tokens
                    contentLen = len(content.tokenList)                 #amount of words/tokens in that link's html content
                    #Checks
                    if (contentLen >= 200 and contentLen <= 5000):      #filtering out webpages with too little info or too much(very large) info
                        content.computeWordFreq()                     
                        if(content.top3Freq/contentLen <= 0.5):         #assert top 3 words dont make up more than 50% of page text/content
                            # print("ADDING NEW LINKS")


                            for link in soup.find_all('a'):
                                if (link.get('href') is not None) and (link.get('href') != "#"):    # 'href' might be NONE or might just be a "#", ignore those cases
                                    URL = urldefrag(link.get('href'))[0]                            # Remove FRAGMENT                                    
                                    if URL[:4] != "http":                                           # Add https to any "relative links"
                                        URL = "https:"+URL
                                    frontURL = URL.split("?")[0]                                    # Remove QUERY section to check if domain valid
                                    if (".ics.uci.edu" in frontURL) or (".cs.uci.edu" in frontURL) or (".informatics.uci.edu" in frontURL) or (".stat.uci.edu" in frontURL) or ("today.uci.edu/department/information_computer_sciences" in frontURL):
                                        foundLinks.append(URL)
                                        ##### UPDATE INSTANCE VARIABLES
                                        mostCommonWords.update(content.tokenDict)   #update most common words with tokens from current url

                                        #FIND LONGEST PAGE
                                        if (contentLen > longestPage[1]):
                                            longestPage[0] = URL
                                            longestPage[1] = contentLen

                                        #ADD TO 


                                        # AT THIS POINT URL IS DEFRAGGED AND HTTPS: ADDED
                                        ###### CHECK SUBDOMAIN: If the prev 5 chars is not '//www', is subdomain & not part of query
                                        if ('.ics.uci.edu' in URL) and (URL.split('.ics.uci.edu')[0][-5:] != '//www') and ('?' not in URL.split('.ics.uci.edu')[0]):
                                            subDomainURL = URL.split('.ics.uci.edu')[0] + '.ics.uci.edu'
                                            if subDomainURL in icsSubDomains.keys():
                                                icsSubDomains[subDomainURL] += 1
                                            else:
                                                icsSubDomains[subDomainURL] = 1

                                        
                    else:
                        pass
                        # print("LITTLEBIGLITTLEBIGLITTLEBIGLITTLEBIGLITTLEBIG ---------------")
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
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
