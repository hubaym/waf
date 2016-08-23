from pymongo import MongoClient
import classes.constant.wafconnection as wcon


    
class MongoConnection:
    
    def __init__(self, dbname= wcon.MONGO_DBNAME, 
                 collection=wcon.MONGO_TWITTER_COLLECTION):
        self._conn = MongoClient('localhost',2107)  
        self._db   = self._conn[dbname]
        self.__collection = self._db[collection]
        print (self.__collection)

        
        #for doc in self.__collection.find():
        #    print(doc)
        
    def insertOne(self, json):
        self.__collection.insert(json)
        
    def insertIfNew(self, json):
        filter = dict()
        filter["tweet_id"] = json["tweet_id"]
        if self.find(json = filter).count() ==0:
            self.insertOne(json)
            
        
    def find(self, json=None):
        return self.__collection.find(json)
    
    def drop(self):
        return self.__collection.drop()
    
    def delete(self, user):
        
        filter = dict()
        filter["source_level2"] = user
        return self.__collection.deleteMany(filter)

    def countcoll(self, json=None):
        resultcoll = self.__collection.find()
        return resultcoll
    
    def deleteOne(self, json):
        self.__collection.remove(json)
    
    def deleteOneById(self, id):
        filter = dict()
        filter["tweet_id"] = id
        self.deleteOne(filter)
        
if __name__ == '__main__':
    # you want to initialize the class
    database   = MongoConnection()
    for item in database.find(): print(item)
    #print(database.countcoll())
    #collcount= database.countcoll()
    #print( collcount)        
