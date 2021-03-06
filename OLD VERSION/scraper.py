import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def scraper(url, resp):
    print("THE URL: ",url, "THE END")
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    # if (resp.status >= 600 and resp.status <=606):
    #     print(resp.error)
    # else if (resp.status >=400 and resp.status <=599):
    #     print(resp.raw_response)
    # else if (resp.status >=200 and resp.status <=599):
    #     print(resp.error)
    print('*'*50)
    print(resp.url)
    print("*"*25)
    print (resp.status)
    print("*"*25)
    print(resp.error)
    print("*"*25)
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    print(soup.prettify())
    print("*"*50)
    #parse through the resp.raw_response.content and find http links to crawl
    #get the http link and add to link -- PRINT IT OUT FOR NOW
    #CHECKS
        #if link == url parameter
    #TO CHECK FOR EACH LINKE???: if the link is valid and is not leading to a trap, a similar page,
    # a dead url, a very large file with low info value...?

    return list()

def is_valid(url):
    print("Validating..")
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

