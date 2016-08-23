'''
Created on 2016. aug. 21.

@author: hubaymarton
'''


class liveAgent():
    '''
    This class is responsible for the near-real time twitter ingestion into mongo 
    and NER processing
    '''
    
    def __init__(self, twitter_st = 60, ner_sl = 60):
        self.twitter_sleep_time = twitter_st
        self.ner_sleep_time = ner_sl
    
    def runTwitterAgent(self):
        pass
    
    def runNerAgent(self):
        pass