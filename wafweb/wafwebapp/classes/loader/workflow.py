'''
Created on 2016. aug. 21.

@author: hubaymarton
'''
from classes.loader.twitterloader import TwitterLoader
from classes.twitter.processTweetBatch import ProcessTweetBatch
from classes.loader.offerloader import OfferLoader

class Workflow():
    def __init__(self):
        self.languages = ['en']
        self.users = [('SecretFlying',678946054218346495),
             ('Fly4freecom',667036797105528831),
             ('FareDealAlert',505071205221937151)]
        pass
    
    
    def start(self):
        
        # get Tweet from Twitter
        
        TwitterLoader().loadNearTweet(self.users, drop = False)
        
        #get evaluatd by ner
        ProcessTweetBatch().processFromDb(self.languages)
        
        #load processed tweets into neo
        OfferLoader().loadOffer()
        
        #
        
        
        