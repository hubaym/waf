from neoquery import NeoQuery
from waflog import WafLog
import classes.constant.neoconstant as neoc

class CriteriaToNeo(NeoQuery):
    
    def __init__(self):
        super().__init__()
        
    
    def createCriteria(self, criteria ):
        node = self.db.nodes.create(departure = criteria.departure,
                        arrival = criteria.arrival,
                        deptDistance = criteria.deptDistance,
                        arrDistance = criteria.arrDistance,
                        userStatus = criteria.userStatus,
                        saveStatus = criteria.saveStatus,
                        bothWay = criteria.bothWay,
                        userid = criteria.userid
                        )
        root = self.db.labels.create(neoc.LABEL_CRITERIA)
        root.add(node)
        WafLog().neologger.info("{0}  id criteria node is created".format(node.id))
        if criteria.departureid is not None:
                geo_dep = self.getGeoByID(criteria.departureid)
                WafLog().neologger.info("{0}  departure relation subcription ".format(geo_dep))
                if geo_dep is not None:
                    node.relationships.create(neoc.LABEL_SUBSCRIBE_DEPARTURE, geo_dep)
        if criteria.arrivalid is not None:
                geo_arr = self.getGeoByID(criteria.arrivalid)
                
                WafLog().neologger.info("{0}  arrival relation subcription ".format(geo_arr))
                if geo_arr is not None:
                    node.relationships.create(neoc.LABEL_SUBSCRIBE_ARRIVAL, geo_arr)
                    
                    
        
                    
        #User connection todo
        if criteria.userid is not None:
            user = self.getUserById(criteria.userid)
            if user is not None:
                user.relationships.create(neoc.LABEL_SEARCH, node)
                
        WafLog().neologger.info(node)
        
        return node.id
        
if __name__ == "__main__":
    pass
 
    
    