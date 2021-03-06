from tweet2json import Tweet2Json
from twitterconnection import TwitterApi
import datetime
from mongolayer import MongoLayer
from processTweetBatch import processTweetBatch
from waflog import WafLog



class TwitterLoader():
    def __init__(self):
        self.twitter= TwitterApi()
        self.mongodb = MongoLayer()

    def ingestion(self, users, count = 1, insert = True, drop = False):
    
        if drop:
            WafLog().twitterlogger.info('drop database')
            self.mongodb.drop()
        WafLog().twitterlogger.info(datetime.datetime.utcnow())
        
        if insert:
            WafLog().twitterlogger.info('insert tweets to database')
            for tweet in self.twitter.timeline(count):
                jsontoinsert = Tweet2Json(tweet._json)
                self.mongodb.insertIfNew(jsontoinsert.getDefaultJson())
                WafLog().twitterlogger.info(datetime.datetime.utcnow())
            
    def loadNearTweet(self,users, drop=False):
        
        
        if drop:
            WafLog().twitterlogger.info('drop database')
            self.mongodb.drop()
        WafLog().twitterlogger.info(datetime.datetime.utcnow())
        
        for user, oldid in users:
            i = 0
            for tweet in self.twitter.nearPastUserTimeline(user):
                self.mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
                i+=1
                if i %100==0:
                    WafLog().twitterlogger.info(datetime.datetime.utcnow(), i, ' for user ', user)   
                         
    def loadOldTweet(self,users, drop=False, delete = False,extraold=False):
        
        
        if drop:
            WafLog().twitterlogger.info('drop database')
            self.mongodb.drop()
        WafLog().twitterlogger.info(datetime.datetime.utcnow())
        if delete:
            for user in users:
                WafLog().twitterlogger.info('drop tweets for user ',user)
                self.mongodb.drop()
        WafLog().twitterlogger.info(datetime.datetime.utcnow())
        
        for user, oldid in users:
            i=0
            if not extraold:
                oldid =None
            for tweet in self.twitter.allTweetUserTimeline(user,oldid):
                    self.mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
                    i+=1
                    if i %100==0:
                        WafLog().twitterlogger.info('saved already %s for user %s' % (str(i), user))


        
if __name__ == '__main__':
    languages = ['en']
    users = [('SecretFlying',678946054218346495),
             ('Fly4freecom',667036797105528831),
             ('FareDealAlert',505071205221937151)]
    getTweets =False
    extraold = False
    twloader = TwitterLoader()
    
    
    processit =True
    #loadNearTweet(users)
    
    if getTweets:
        twloader.loadOldTweet(users,drop = False, delete= False, extraold=extraold)

    print('Done')
    