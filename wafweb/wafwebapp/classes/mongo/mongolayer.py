from mongoconnection import MongoConnection
from classes.utils.status
class MongoLayer(MongoConnection):
    
    def __init__(self ):
        super().__init__()
        
        
    def getAllOffers(self):
        return self.find()
    
    def getOffersWithPlace(self):
        
        jsonfilter = {
        "$and":[
                {"arr":{"$ne":{}}
                },
                {"dept":{"$ne":{}}
                },
                {"arr":{"$ne":"DEFAULT"}
                },
                {"dept":{"$ne":"DEFAULT"}
                },
                {"language":"en"}
            ]
        }
    def getEvaluatedOffers(self):
        
        jsonfilter = dict()
        jsonfilter['status'] = status.TWITTER_EVALUATED
        
        return self.find(jsonfilter)
    
    def getOffersWithOnePlace(self):
        
        jsonfilter = {
        "$or":[
                {"arr":{"$ne":{}}
                },
                {"dept":{"$ne":{}}
                },
                {"arr":{"$ne":"DEFAULT"}
                },
                {"dept":{"$ne":"DEFAULT"}
                },
                {"language":"en"}
            ]
        }
        
        return self.find(jsonfilter)
    
    def getOffersforExtract(self, language = ' '):
        
        if language ==' ':
            jsonfilter = {
                          "$and":[
                                  {"dept":{"$eq":"DEFAULT"}
                                   },
                                  {"arr":{"$eq":"DEFAULT"}
                                   }
                                  ]
                          }
        else:
            jsonfilter = {
                          "$and":[
                                  {"dept":{"$eq":"DEFAULT"}
                                   },
                                  {"arr":{"$eq":"DEFAULT"}
                                   },
                                  {"language":{"$eq":"{0}s".format(language)}
                                   }
                                  ]
                          }
        return self.find(jsonfilter)
    
    def deleteTweet(self, tweet):
        self.deleteOneById(tweet['tweet_id'])
        
        
    def updateAllTweet(self, tweetlist):
        
        for tweet in tweetlist:
            self.deleteTweet(tweet)
            self.insertOne(tweet)
        
if __name__ == '__main__':
    mon = MongoLayer()
    print(len([each for each in mon.getOffersWithOnePlace()]))  
    
        