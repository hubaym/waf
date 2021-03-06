from collections import OrderedDict
import reghu as rhu
import re
from time import mktime
import time
from datetime import datetime
import classes.utils.status 

SOURCE_TWITTER = 'twitter'
FIELD_DEFAULT = 'DEFAULT'
DATEFORMAT_TWITTER = "%a %b %d %H:%M:%S +0000 %Y"

# In[11]:

class Tweet2Json(object):
    
    def createJson(self):
        self.extended_tweet = OrderedDict()
        self.extended_tweet['dep_city'] = self.dep_city
        self.extended_tweet['dep_country'] = self.dep_country
        self.extended_tweet['arr_city'] = self.arr_city
        self.extended_tweet['arr_country'] = self.arr_country
        self.extended_tweet['language'] = self.language
        self.extended_tweet = {**self.extended_tweet , **OrderedDict(self.tweet.items()) }
        return dict(self.extended_tweet)
    
    def createJsonShort(self):
        self.extended_tweet = OrderedDict()
        self.extended_tweet['dep_city'] = self.dep_city
        self.extended_tweet['dep_country'] = self.dep_country
        self.extended_tweet['arr_city'] = self.arr_city
        self.extended_tweet['arr_country'] = self.arr_country
        self.extended_tweet['language'] = self.language
        self.extended_tweet['text'] = self.text
        return dict(self.extended_tweet)
    
    
    def __process(self):
        extrecteddata = ExtractData(self.text)
        self.dep_city = extrecteddata.dep_city
        self.dep_country = extrecteddata.dep_country
        self.arr_city = extrecteddata.arr_city
        self.arr_country = extrecteddata.arr_country
        self.language = extrecteddata.language
    
    def __init__(self, tweet, user):
        self.tweet = tweet
        self.text = tweet.get('text')
        self.id = tweet.get('id_str')
        self.lang = tweet.get('lang')
        self.created_at = tweet.get('created_at')
        self.user = user
    
    def getDefaultJson(self):
        self.extended_tweet = OrderedDict()
        self.extended_tweet['tweet_id'] = self.id
        self.extended_tweet['dept'] = FIELD_DEFAULT
        self.extended_tweet['arr'] =  FIELD_DEFAULT
        self.extended_tweet['lang'] =  self.lang
        self.extended_tweet['language'] = self.setLanguage(self.text)
        self.extended_tweet['text'] = self.text
        self.extended_tweet['created_at'] = self.convert2Date(self.created_at)
        self.extended_tweet['source_level1'] = SOURCE_TWITTER
        self.extended_tweet['source_level2'] = self.user
        self.extended_tweet['status'] = status.TWITTER_NOT_PROCESSED
        return dict(self.extended_tweet)
        
    def printIfWrong(self):
        if self.dep_city == FIELD_DEFAULT and self.dep_country ==FIELD_DEFAULT and self.arr_city == FIELD_DEFAULT and self.arr_country ==FIELD_DEFAULT:
            if self.language == 'en':
                self.printFeatures()
            
    def printFeatures(self):
        print(self.text)
        print(self.dep_city)
        print(self.dep_country)
        print(self.arr_city)
        print(self.arr_country)
    
    def setLanguage(self, text):
        result = re.findall(rhu.reg_is_HU_accent, text)
        if len(result) > 0:
            return 'hu'
        result = re.findall(rhu.reg_is_DE_accent, text)
        if len(result) > 0:
            return 'de'
        
        return 'en'
    
    def convert2Date(self, createdtime):
        return str(datetime.fromtimestamp(mktime(time.strptime(createdtime,DATEFORMAT_TWITTER))))
        
if __name__ == '__main__':
    #text = "Budapestről New Yorkba óóócsóó"
    #test_tweet = dict()
    #test_tweet['text'] = text
    #obj = Tweet2Json(test_tweet)
    #print(obj.createJsonShort())
    created_at = "Wed Aug 29 17:12:58 +0000 2012"
    dt = datetime.fromtimestamp(mktime(time.strptime(created_at,DATEFORMAT_TWITTER)))
    print (str(dt) )

        