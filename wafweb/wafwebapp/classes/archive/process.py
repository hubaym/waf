from tweet2json import Tweet2Json
from twitterconnection import TwitterApi
import datetime
from mongolayer import MongoLayer
from processTweetBatch import processTweetBatch
from waflog import WafLog



twitter= TwitterApi()
mongodb = MongoLayer()

def ingestion(users, count = 1, insert = True, drop = False):

    if drop:
        WafLog().twitterlogger.info('drop database')
        mongodb.drop()
    WafLog().twitterlogger.info(datetime.datetime.utcnow())
    
    if insert:
        WafLog().twitterlogger.info('insert tweets to database')
        for tweet in twitter.timeline(count):
            jsontoinsert = Tweet2Json(tweet._json)
            mongodb.insertIfNew(jsontoinsert.getDefaultJson())
            WafLog().twitterlogger.info(datetime.datetime.utcnow())
            
def loadNearTweet(users, drop=False):
    
    
    if drop:
        WafLog().twitterlogger.info('drop database')
        mongodb.drop()
    WafLog().twitterlogger.info(datetime.datetime.utcnow())
    
    for user, oldid in users:
        i = 0
        for tweet in twitter.nearPastUserTimeline(user):
            mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
            i+=1
            if i %100==0:
                WafLog().twitterlogger.info(datetime.datetime.utcnow(), i, ' for user ', user)   
                         
def loadOldTweet(users, drop=False, delete = False,extraold=False):
    
    
    if drop:
        WafLog().twitterlogger.info('drop database')
        mongodb.drop()
    WafLog().twitterlogger.info(datetime.datetime.utcnow())
    if delete:
        for user in users:
            WafLog().twitterlogger.info('drop tweets for user ',user)
            mongodb.drop()
    WafLog().twitterlogger.info(datetime.datetime.utcnow())
    
    for user, oldid in users:
        i=0
        if not extraold:
            oldid =None
        for tweet in twitter.allTweetUserTimeline(user,oldid):
                mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
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
    
    
    processit =True
    #loadNearTweet(users)
    
    if getTweets:
        loadOldTweet(users,drop = False, delete= False, extraold=extraold)
        
 
    print('Done')
    