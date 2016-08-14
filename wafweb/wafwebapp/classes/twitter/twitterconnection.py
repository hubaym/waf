import wafconnection as wcon
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
NEARPAST= 200
MAXTWEETCOUNT=200

class TwitterApi:
    
    def __init__(self):
        auth = OAuthHandler(wcon.ckey, wcon.consumer_secret)
        auth.set_access_token(wcon.access_token_key, wcon.access_token_secret)
        self.__api = tweepy.API(auth)
 
    
    def timeline(self, items):
        return tweepy.Cursor(self.__api.home_timeline).items(items)
    
    def timelineOld(self, items, sincedate, todate):
        return tweepy.Cursor(self.__api.search,
                           q="error fare",
                           since="2015-01-01",
                           until="2015-01-09",
                           lang="en").items()
        
    def allTweetUserTimeline(self, username):
        
        #initialize a list to hold all the tweepy Tweets
        alltweets = []    
        new_tweets =  self.__api.user_timeline(screen_name = username,count=MAXTWEETCOUNT)
        #save most recent tweets
        alltweets.extend(new_tweets)
    
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
    
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print ("getting tweets before %s" % (oldest))
        
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.__api.user_timeline(screen_name = username,count=MAXTWEETCOUNT,max_id=oldest)
        
            #save most recent tweets
            alltweets.extend(new_tweets)
        
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        
            print ("...%s tweets downloaded so far" % (len(alltweets)))
        return alltweets
    
    def nearPastUserTimeline(self, username):
        
        #initialize a list to hold all the tweepy Tweets
        alltweets = []    
        new_tweets =  self.__api.user_timeline(screen_name = username,count=MAXTWEETCOUNT)
        #save most recent tweets
        alltweets.extend(new_tweets)
    
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        actual = NEARPAST -MAXTWEETCOUNT
        #keep grabbing tweets until there are no tweets left to grab
        while actual > 0:
            print ("getting tweets before %s" % (oldest))
        
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = self.__api.user_timeline(screen_name = username,count=MAXTWEETCOUNT,max_id=oldest)
        
            #save most recent tweets
            alltweets.extend(new_tweets)
        
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            actual = actual -MAXTWEETCOUNT
            print ("...%s tweets downloaded so far" % (len(alltweets)))
        return alltweets
        
if __name__ == '__main__':
    # you want to initialize the class
    twitter   = TwitterApi()
    for item in twitter.userTimeline('SecretFlying') : print(item._json["lang"],item._json["user"], item.id)    