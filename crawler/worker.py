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
        self.discoveredURLs = set()         #all urls scraped (discard fragment) (unique)
        self.longestPage = [None,0]         #(url, maxwordcount)
        self.icsSubDomains = dict()         #(subdomain:count)
        self.mostCommonWords = dict()       #(word:frequency)   
        
    def run(self):
        count = 0
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper(tbd_url, resp,self.mostCommonWords,self.icsSubDomains,self.longestPage)
            ###CHECKING IF INSTANCE VARIABLES WORKING

            #IMPLEMENT
            print("THE SIZE OF THE FRONTIERRLS IS NOW: ",len(self.frontier.to_be_downloaded))
            print("THE SIZE OF THE DISCOVERED URLS IS NOW: ",len(self.discoveredURLs))
            for scraped_url in scraped_urls:                                                    #for each scraped url, visit only if unvisited before
                if (scraped_url not in self.discoveredURLs):                                       #and add to visitedurl set and frontier
                    self.discoveredURLs.add(scraped_url)
                    self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
            count += 1
            print("\n\n",count,"\n\n")
        #once out of while loop, that means crawler has stopped and now 
            if count == 100:
                print()
                break
            
