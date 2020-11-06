from threading import Thread

from utils.download import download
from utils import get_logger
from scraper import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        #OUR INSTANCE VARIABLES
        self.discoveredURLs = set()         #1 - all urls scraped (discard fragment) (unique)
        self.longestPage = [None,0]         #2 - (url, maxwordcount)
        self.mostCommonWords = dict()       #3 - (word:frequency)  
        self.icsSubDomains = dict()         #4 - (subdomain:count)
        self.similarURLs = dict()           #Don't crawl to a link once have met a URLs threshold
        
    def run(self):
        count = 0
        while True:
            try:
                tbd_url = self.frontier.get_tbd_url()
                if not tbd_url:
                    self.logger.info("Frontier is empty. Stopping Crawler.")
                    break
                resp = download(tbd_url, self.config, self.logger)
                self.logger.info(
                    f"Downloaded {tbd_url}, status <{resp.status}>, "
                    f"using cache {self.config.cache_server}.")
                scraped_urls = scraper(tbd_url, resp,self.mostCommonWords,self.icsSubDomains,self.longestPage,self.similarURLs)
                for scraped_url in scraped_urls:                    #For each scraped url, add only if not discovered
                    if (scraped_url not in self.discoveredURLs):      
                        self.discoveredURLs.add(scraped_url)
                        self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)
                time.sleep(self.config.time_delay)
                count +=1
                print("\n",count,"\n")
            except:
                print("IT BLEW UPPPPPPPP")
                pass
            
