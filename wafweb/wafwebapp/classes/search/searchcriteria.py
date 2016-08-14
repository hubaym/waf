from geotext import GeoText
from criteriatoneo import CriteriaToNeo
from criteria import Criteria
from waflog import WafLog

class SearchCriteria():
    
    def __init__(self, departure, arrival,
                 deptDistance=150.0, arrDistance=150.0, userid =None, language = 'en'):
        self.departure = departure
        self.arrival = arrival
        self.departureid =None
        self.arrivalid = None
        self.deptDistance = deptDistance
        self.arrDistance = arrDistance
        self.userid = userid
        self.userStatus = 'TEMP'
        self.saveStatus = 'NEW'
        
        if arrival is None or departure is None:
            self.bothWay = False
        else:
            self.bothWay = True
        
        if self.departure is not None:
            result = GeoText().process([self.departure] )
            self.departureid = self.getID(result)
            if self.departureid is None:
                WafLog().neologger.error("gebasz a keresesnel")
            WafLog().neologger.info("{0} found ".format(self.departureid))
        if self.arrival is not None:
            result = GeoText().process([self.arrival])
            self.arrivalid = self.getID(result)
            if self.arrivalid is None:
                WafLog().neologger.error("gebasz a keresesnel")
            WafLog().neologger.info("{0} found ".format(self.arrivalid))
        
        neocriteria = Criteria(departure = self.departure,
                               arrival = self.arrival,
                               departureid= self.departureid,
                               arrivalid = self.arrivalid,
                               deptDistance = self.deptDistance,
                               arrDistance = self.arrDistance,
                               userStatus = self.userStatus,
                               saveStatus = self.saveStatus,
                               bothWay =self.bothWay,
                               userid = self.userid)
        createcriteria = CriteriaToNeo()
        self.criteriaid = createcriteria.createCriteria(neocriteria)
 
    
    def getID(self,dictionary):
        
        if dictionary is None or len(dictionary) ==0:
            return None
        for key, value in dictionary.items():
            return value