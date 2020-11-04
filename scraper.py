import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from ContentPartA import Token

def scraper(url, resp):
    print("THE URL: ",url, "THE END")
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    foundLinks = list()
    if (".ics.uci.edu" in url) or (".cs.uci.edu" in url) or (".informatics.uci.edu" in url) or (".stat.uci.edu" in url) or ("today.uci.edu/department/information_computer_sciences" in url):
        print("----------------------------------------------------",url)
        if (resp.status >= 600 and resp.status <=606):
            print("ERROR ERROR ERROR ERROR ERROR:                 ",resp.error)
        if (resp.status >=200 and resp.status <=599):
            if (resp.status >=400 and resp.status <=599):
                print("SKIPPED")
            else:
                print("GOOD LINK")
                soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
                #ensure that the webpg has valid amount of information
                content = Token()
                content.tokenizeFile(soup)
                contentLen = len(content.tokenList)
                if (contentLen >= 200 and contentLen <= 3000):
                    content.computeWordFreq()
                    if(content.maxFreq/contentLen >= 0.35):
                        for link in soup.find_all('a'):
                            foundLinks.append(link.get('href'))
                else:
                    print("LITTLEBIGLITTLEBIGLITTLEBIGLITTLEBIGLITTLEBIG ---------------")


    return foundLinks
            
    #     print(currlink)
    #     if (".ics.uci.edu/" in currlink):
    #         print("******LINK IS SUBDOMAIN OF .ICS.UCI.EDU******")
            #add to a list of subdomains for ics.uci url and increment count for that subdomain
        #use soup.get_text() to extract all text from a page
   
    #parse through the resp.raw_response.content and find http links to crawl
    #get the http link and add to link -- PRINT IT OUT FOR NOW
    #CHECKS
        #if link == url parameter
    #TO CHECK FOR EACH LINKE???: if the link is valid and is not leading to a trap, a similar page,
    # a dead url, a very large file with low info value...?

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
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

