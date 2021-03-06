from searchcriteria import SearchCriteria
from neosearchquery import NeoSearchQuery
from searchResult import SearchResult
from wronggeonameexception import WrongGeoNameException
import datetime
import math
from time import mktime
import time

class SearchManager():
    
    def __init__(self):
        self.result =list()
        self.neosearch = NeoSearchQuery()
    
    def search(self, criteria):
        
     
        self.gatherResults(self.neosearch.seachByCriteria(criteria)  )
        if 0==len(self.result):
            print("no any result -try again")
            criteria.deptDistance = 500
            criteria.arrDistance = 600
            self.gatherResults(self.neosearch.seachByCriteria(criteria)  )
        self.result = sorted(self.result, key=lambda x: x.point, reverse = True)
      
            
    def gatherResults(self, results):
        for elemdict in results:
            elem = elemdict[0].get('data')
            point = elemdict[1]
            pluspoint = self.getPointBasedOnDate(elem.get('created_at'))
            if self.canAppend(elem, pluspoint +point):
                self.result.append(SearchResult(elem.get('created_at'), elem.get('text'), elem.get('language'),elem.get('source_lev_1'),elem.get('source_lev_2'), point +pluspoint))
    
    def canAppend(self, resultelem,point ):
        for elem in self.result:
            if elem.text == resultelem.get('text'):
                if elem.point < point:
                    print("deleted from list %s" % elem.text)
                    del self.result[self.result.index(elem)]
                    return True
                else:
                    return False
        return True
    
    def getPointBasedOnDate(self, created_at):
        ts = datetime.datetime.fromtimestamp(mktime(time.strptime(created_at,"%Y-%m-%d %H:%M:%S")))
        diff = datetime.datetime.now()-ts
        h = diff.total_seconds() / 3600  
        
        point = -4.680503237  *math.log(h) + 47.80489309
        point = 50.0 if point >50.0 else 0.0 if point <0.0 else point
        return point
    
    def printResult(self):
        
        for elem in self.result:
            elem.pretty()
            
    def returnResult(self):
        
        return self.result
    
    def getDictList(self):
        
        return [each.__dict__ for each in self.result]
        
if __name__ == "__main__":
    
    point = -8.393345779  *math.log(1000) + 51.55543035
    ##point = 50 if point >50 else 0 if point <0 else point
    #print(point)
    search = SearchManager()
    criteria = SearchCriteria('Paris','Sacramento', deptDistance=300, arrDistance=300)
    try:
        search.search(criteria)
        print([each for each in search.getDictList()])
        
    except WrongGeoNameException as a:
        print (a)