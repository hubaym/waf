from tweet2json import Tweet2Json
from twitterconnection import TwitterApi
import datetime
from mongolayer import MongoLayer
from processTweetBatch import processTweetBatch
from waflog import WafLog



twitter= TwitterApi()
mongodb = MongoLayer()

def ingestion(count = 1, insert = True, drop = False):

    if drop:
        print('drop database')
        mongodb.drop()
    print(datetime.datetime.utcnow())
    
    if insert:
        print('insert tweets to database')
        for tweet in twitter.timeline(count):
            jsontoinsert = Tweet2Json(tweet._json)
            mongodb.insertIfNew(jsontoinsert.getDefaultJson())
            print(datetime.datetime.utcnow())
            
def loadNearTweet(users, drop=False):
    
    
    if drop:
        print('drop database')
        mongodb.drop()
    print(datetime.datetime.utcnow())
    
    for user in users:
        i = 0
        for tweet in twitter.nearPastUserTimeline(user):
            mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
            i+=1
            if i %100==0:
                print(datetime.datetime.utcnow(), i, ' for user ', user)   
                         
def loadOldTweet(users, drop=False, delete = False):
    
    
    if drop:
        print('drop database')
        mongodb.drop()
    print(datetime.datetime.utcnow())
    if delete:
        for user in users:
            print('drop tweets for user ',user)
            mongodb.drop()
    print(datetime.datetime.utcnow())
    
    for user in users:
        i = 0
        for tweet in twitter.allTweetUserTimeline(user):
            mongodb.insertIfNew(Tweet2Json(tweet._json, user).getDefaultJson())
            i+=1
            if i %100==0:
                print(datetime.datetime.utcnow(), i, ' for user ', user)

def extractInfo(languages):
    print('start to extract function')
    for lan in languages:
        tweets_to_process = mongodb.find({"language":"en"})
        tweets_to_process_l = list(tweets_to_process)
        #print('start to processTweetBatch',len(list(tweets_to_process)))
        process_batch = processTweetBatch(list(tweets_to_process_l), lan)
        
        print('extract infos')
        for tweet in tweets_to_process_l:
            tweet['arr'] = process_batch.evaluateddict[tweet['tweet_id']]['arr']
            tweet['dept'] = process_batch.evaluateddict[tweet['tweet_id']]['dept']
        
        
        print('update all tweet')
        mongodb.updateAllTweet(tweets_to_process_l)
        
        
            
    
        
def stat():

    result = mongodb.find(
                                {"language":"en"}
                                
                          )
    print(result.count())
    result = mongodb.find({"$and":[
                                {"$and":[
                                        {"dep_country":"DEFAULT"},
                                        {"arr_country":"DEFAULT"}
                                        ] 
                                },
                                {"language":"en"}
                                ] 
                           })
    print(result.count())
    for item in result:
        print (item.get("text"))
        print ("------------------------------------")
        
        
if __name__ == '__main__':
    languages = ['en']
    users = ['SecretFlying','Fly4freecom']
    #users = ['Fly4freecom']
    #ingestion(100, True, False)
    
    #stat()
    
    #loadOldTweet(users,True)
    extractInfo(languages)
    