import subprocess
import shlex
import codecs
from geotext import GeoText
import settings
from waflog import WafLog
import classes.utils.tweetprocessstatus as status
from mongolayer import MongoLayer

xchangepath = settings.BASE_DIR +'/xchange/'
scriptpath = settings.BASE_DIR +'/ner/commands/'
tweetfile = 'tweetfile.txt'
scriptname = 'waf_ner_en.sh'
evaluated = 'evaluated.tsv'
evaluatedtest = 'evaluatedtest.tsv'
sentencetoken = ' ENDSENTENCE '
depttoken = 'DEPT'
arrtoken = 'ARR'
linktoken = 'LINK'

class ProcessTweetBatch:
    
    def __init__(self, language, test = False):
        self.__tweet_by_id_dict= dict()
        self.evaluateddict = dict()
        self.__language = language
        self.mongodb = MongoLayer()
        self.test = test
        
            
    def processFromDb(self):
        print('start to extract function')
        for lan in self.__language:
            tweets_to_process_l = list(self.mongodb.find({"language":"en"}))
            print(len(tweets_to_process_l),' is to be processed')
            for tweetjson in tweets_to_process_l:
                self.__tweet_by_id_dict[tweetjson.get('tweet_id')] = tweetjson
            
            if self.test:
                self.processEvaluatedFile(self.test)
            else:
                self.buildFile()
                self.processTweet()
                self.processEvaluatedFile()
                self.saveToDb()
            
            
 
    def saveToDb(self):
        
        print('update all tweet')
        self.mongodb.updateAllTweet(self.tweets_to_process_l)
            
    def buildFile(self):
        fileText = ''
        for key, tweet in self.__tweet_by_id_dict.items():
            fileText = fileText + key +' ' +  tweet.get('text') +  sentencetoken
            
        
        file = codecs.open(xchangepath + tweetfile, "w", "utf-8")
        file.write(fileText)
        file.close
    
    def processTweet(self ):
        command = 'sh '+ scriptpath +scriptname + ' ' + xchangepath+tweetfile +' '+ xchangepath + evaluated
        print('calling: ',command)
        subprocess.check_call(shlex.split(command))
        
    def processEvaluatedFile(self, test = False):
        arr = list()
        dept = list()
        links = list()
        geotext =   GeoText()
        searchForMoreDept = False
        searchForMoreArr = False
        textFirstPartDept = ''
        textFirstPartArr = ''
        if test:
            filepath =xchangepath + evaluatedtest
        else:
            filepath =xchangepath + evaluated
            
        for line in codecs.open(filepath, 'r', "utf-8"):
            if line =='\n':
                continue
            text , token= line.rstrip().split('\t')
            if token ==depttoken or token ==arrtoken:
                if token == depttoken:
                    if searchForMoreArr:
                        arr.append(textFirstPartArr)
                        textFirstPartArr = ''
                        searchForMoreArr = False
                    
                    if not searchForMoreDept:
                        textFirstPartDept = text
                        searchForMoreDept = True
                    else:
                        textFirstPartDept += ' ' + text
                        
                if token == arrtoken:
                    if searchForMoreDept:
                        dept.append(textFirstPartDept)
                        textFirstPartDept = ''
                        searchForMoreDept = False
                    
                    if not searchForMoreArr:
                        textFirstPartArr = text
                        searchForMoreArr = True
                    else:
                        textFirstPartArr += ' ' + text
                        
                    
            else:
                #Everything which is not ARR and DEPT, here they are saved to a list
                if searchForMoreDept:
                    dept.append(textFirstPartDept)
                    textFirstPartDept = ''
                    searchForMoreDept = False
                    
                if searchForMoreArr:
                    arr.append(textFirstPartArr)
                    textFirstPartArr = ''
                    searchForMoreArr = False
            
                if len(text) > 10 and text.isnumeric():
                    id = text
                    continue
                
                elif text == sentencetoken.rsplit()[0]:
                    # here we return with a dict with valid GEO names
                    
                    tweetdict = dict()
                    arr2 =[]
                    dept2 =[]
                    for each in arr:
                        arr2.append(each.replace('#',''))
                    for each in dept:
                        dept2.append(each.replace('#',''))
                    tweetdict['arr'] = geotext.process(arr2, self.__language)
                    tweetdict['dept'] = geotext.process(dept2, self.__language)
                    tweetdict['links'] = links
                    self.evaluateddict[id] = tweetdict
                    arr = list()
                    dept = list()
                    links = list()
                    continue
                
                else:
                    if token == linktoken:
                        links.append(text)
                    else:
                        # O tag 
                        pass
                    
        print('save back evaluated info to tweets_to_process')
        for tweet in self.tweets_to_process_l:
            tweet['arr'] = self.evaluateddict[tweet['tweet_id']]['arr']
            tweet['dept'] = self.evaluateddict[tweet['tweet_id']]['dept']
            tweet['links'] = self.evaluateddict[tweet['tweet_id']]['links']
            tweet['status'] = status.TWITTER_EVALUATED
            

    
if __name__ == '__main__':
    languages= ['en']
    process = processTweetBatch(languages)
    process.processFromDb()
    