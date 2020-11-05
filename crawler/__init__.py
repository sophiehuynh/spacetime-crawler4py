from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker

class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier, worker_factory=Worker):
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.workers = list()
        self.worker_factory = worker_factory
        ### IMPLEMENTED
        

    def start_async(self):
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier)
            for worker_id in range(self.config.threads_count)]
        for worker in self.workers:
            worker.start()

    def start(self):
        self.start_async()
        self.join()

        #TOP 50 Common Words Frequency -----------------------------------------------------------
        f = open("3_top50.txt", "w")
        f.write("Top 50 Words and their frequency\n")
        f.write("-"*80)
        f.write("\n")
        #ICS.UCI.EDU SUBDOMAIN + COUNT -----------------------------------------------------------
        sd = open("4_SubDomains.txt", "w")
        sd.write("ics.uci.edu SubDomains and their frequency\n")
        sd.write("-"*80)
        sd.write("\n")
        #LONGEST PAGE ----------------------------------------------------------------------------
        p = open("2_LongestPage.txt","w")
        p.write("Longest Page in terms of number of words\n")
        p.write("-"*80)
        p.write("\n")
        #NUMBER OF UNIQUE PAGES ------------------------------------------------------------------
        u = open("1_UniquePages.txt","w")
        u.write("Number of Unique Pages\n")
        u.write("-"*80)
        u.write("\n")

        #FOR LOOP WRITING TO FILE
        for worker in self.workers:
            #-----------------------top50
            t50Dict = {k: v for k, v in sorted(worker.mostCommonWords.items(), key=lambda item: item[1], reverse=True)}
            keyList = list(t50Dict.keys())
            valueList = list(t50Dict.values())
            for i in range(50): 
                try:
                    wordStr = format(keyList[i]).ljust(45) + "===" + format(str(valueList[i])).rjust(10) + "\n"
                    f.write(wordStr)
                except:
                    break
            f.write("\n")
            #-----------------------subdomains
            sdDict = {k: v for k, v in sorted(worker.icsSubDomains.items(), key=lambda item: item[0])}
            for k,v in sdDict.items():
                sd.write(k + ", " + str(v) +"\n")
            #-----------------------longestPage
            p.write(str(worker.longestPage[0]) + "\t\t\tNumber of Words: " + str(worker.longestPage[1]))
            p.write("\n")
            #-----------------------unqiuePages
            u.write(str(len(worker.discoveredURLs)))
            u.write("\n")
        f.close()
        sd.close()
        p.close()
        u.close()
        #Combine the 4 files into 1 Report File
        with open("Report.txt", "w") as repfile:
            repfile.write("CRAWLING REPORT\n\n")
            repfile.write("="*140)
            repfile.write("\n\n")
            with open("1_UniquePages.txt", "r") as ufile:
                repfile.write(ufile.read())
                repfile.write("-"*140)
                repfile.write("\n\n")
            with open("2_LongestPage.txt", "r") as pfile:
                repfile.write(pfile.read())
                repfile.write("-"*140)
                repfile.write("\n\n")
            with open("3_top50.txt", "r") as ffile:
                repfile.write(ffile.read())
                repfile.write("-"*140)
                repfile.write("\n\n")
            with open("4_SubDomains.txt", "r") as sdfile:
                repfile.write(sdfile.read())
                repfile.write("\n")


   
        

    def join(self):
        for worker in self.workers:
            worker.join()

