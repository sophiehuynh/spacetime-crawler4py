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
        #TOP 50 Common Words written to file -------------------------
        f = open("top50.txt", "w")
        f.write("Top 50 Words and their frequency\n")
        f.write("-"*80)
        f.write("\n")
        top50 = ""
        for worker in self.workers:
            tempDict = {k: v for k, v in sorted(worker.mostCommonWords.items(), key=lambda item: item[1], reverse=True)}
            keyList = list(tempDict.keys())
            valueList = list(tempDict.values())
            for i in range(50): #get top 50 common words and their frequencies and write to file
                wordStr = format(keyList[i]).ljust(45) + "===" + format(str(valueList[i])).rjust(10) + "\n"
                f.write(wordStr)
        f.close()
        #-------------------------------------------------------------


    def join(self):
        for worker in self.workers:
            worker.join()

