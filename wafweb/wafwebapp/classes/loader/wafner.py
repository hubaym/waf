from classes.constant.waflog import WafLog
import settings
import subprocess
import shlex
from mongolayer import MongoLayer
import codecs
import re


xchangepath = settings.BASE_DIR +'/xchange/'
scriptpath = settings.BASE_DIR +'/ner/commands/'
trainpath = settings.BASE_DIR +'/ner/trainfiles/'

trainfile = 'waf_twittertrain_en.tok'
trainscript = 'waf_nertrain_en.sh'
to_tokenize_file = 'to_tokenize.txt'
tokenized_file = 'tokenized.txt'

class WafNer():
    
    def __init__(self):
        self.mongodb = MongoLayer()
        pass
    
    def wafTrain(self):
        cdcommand = 'cd '+ scriptpath
        command = 'ls '
        #command = 'sh '+ trainscript 
        WafLog().nerlogger.info('calling: %s' %cdcommand)
        subprocess.check_call(shlex.split(cdcommand))
        
        WafLog().nerlogger.info('calling: %s' %command)
        subprocess.check_call(shlex.split(command))
        
    def getSuspicous(self):

        result = self.mongodb.find({"$and":[
                                        {"$or":[
                                                {"dept":{}},
                                                {"arr":{}}
                                                ] 
                                        },
                                        {"language":"en"}
                                        ] 
                                   })
            
        for item in result:
            WafLog().nerlogger.info(u'Text : {0: <150} \n {1: <40} Dept: {2: <20}  Arr  {3: <20} \n '.format(str(item.get("text")),
                                                                                                ' '    ,      
                                                                                                str(item.get("dept")),
                                                                                                str(item.get("arr"))
                                                                                                )
                                    )
                
        
    def toTokenize(self):
        file = codecs.open(xchangepath + to_tokenize_file, "r", "utf-8")
        newtext = ''
        for line in file:
            print(line)
            newtext += '\tO\n'.join(re.split(r'[ ,]', line))
        file.close
        
        file = codecs.open(xchangepath + tokenized_file, "r+", "utf-8")
        file.write(newtext)
        file.close

if __name__ == '__main__':
    test = WafNer()
    test.toTokenize()
    print('''Done''')
                            
                            