import subprocess
import shlex
import codecs
from geotext import GeoText
import settings
from waflog import WafLog

xchangepath = settings.BASE_DIR +'/xchange/'
scriptpath = settings.BASE_DIR +'/ner/commands/'
tweetfile = 'tweetfile.txt'
scriptname = 'waf_ner_en.sh'
evaluated = 'evaluated.tsv'
evaluatedtest = 'evaluatedtest.tsv'
sentencetoken = ' ENDSENTENCE '
depttoken = 'DEPT'
arrtoken = 'ARR'

class processTweetBatch:
    
    def __init__(self, tweetlist, language, test = False):
        self.__tweetdict= dict()
        self.evaluateddict = dict()
        self.__language = language
        print(len(tweetlist),' is to be processed')
        for tweetjson in tweetlist:
            self.__tweetdict[tweetjson.get('tweet_id')] = tweetjson
        
        if test:
            self.processEvaluatedFile(test)
        else:
            self.buildFile()
            self.processTweet()
            self.processEvaluatedFile()
 
            
    def buildFile(self):
        fileText = ''
        for key, tweet in self.__tweetdict.items():
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
                    tweetdict['arr'] = geotext.process(arr, self.__language)
                    tweetdict['dept'] = geotext.process(dept, self.__language)
                    self.evaluateddict[id] = tweetdict
                    arr = list()
                    dept = list()
                    continue
                
                else:
                    # O tag 
                    pass

    
if __name__ == '__main__':
    test = processTweetBatch(list(), 'en', True)
    WafLog().nerlogger.info(test.evaluateddict)
    