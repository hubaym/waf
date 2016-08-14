import logging
import settings

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class WafLog():
    
    def __init__(self):
        
        
        self.nerlogger = self.setup_logger('ner', settings.BASE_DIR + '/logs/ner.log', logging.INFO)
        self.neologger = self.setup_logger('neo', settings.BASE_DIR + '/logs/neo.log', logging.INFO)
        
    def setup_logger(self,logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='a')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
    
        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)
        return l 
        
if __name__=="__main__":
    WafLog().neologger.error('test')
    WafLog().neologger.info('test')
    