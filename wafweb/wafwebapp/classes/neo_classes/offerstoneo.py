from neoquery import NeoQuery
import classes.constant.neoconstant as neoc



class OffersToNeo(NeoQuery):
    
    def __init__(self):
        super().__init__()
        
    def createOffer(self, offer):
        
        
        node = self.db.nodes.create(
                        connections =  str(offer.dept) + str(offer.arr) ,
                        tweet_id = offer.tweetid,
                        mongo_id = offer.mongoid,
                        created_at = offer.created_at,
                        text = offer.text,
                        language = offer.language,
                        source_lev_1 = offer.source_lev_1,
                        source_lev_2 = offer.source_lev_2,
                        links = offer.links if 0<len(offer.links) else None,
                        status = offer.status
                        )
        
        offerlabel = self.db.labels.create(neoc.LABEL_OFFER)
        offerlabel.add(node)

        
        for geoid in self.getListOfAll(offer.dept):
            geo = self.getGeoByID(geoid)
            if geo is not None:
                node.relationships.create(neoc.LABEL_DEPARTURE, geo)
                #print("relationship conti {0}".format(continent))
        for geoid in self.getListOfAll(offer.arr):
            geo = self.getGeoByID(geoid)
            if geo is not None:
                node.relationships.create(neoc.LABEL_ARRIVAL, geo)
                #print("relationship conti {0}".format(continent))
          
        return  
    
    ##----------old stuff-------------------------------
        for conti in self.getListOf(offer.dept, 'CONTINENT'):
            continent = self.getContinentRootByCode(conti)
            if continent is not None:
                node.relationships.create("departure", continent)
                #print("relationship conti {0}".format(continent))
                
        for conti in self.getListOf(offer.arr, 'CONTINENT'):
            continent = self.getContinentRootByCode(conti)
            if continent is not None:
                node.relationships.create("arrival", continent)
                #print("relationship conti {0}".format(continent))
        
        for country_code in self.getListOf(offer.dept, 'COUNTRY'):
            country = self.getCountryRootByCode(country_code)
            if country is not None:
                node.relationships.create("departure", country)
                #print("relationship country {0}".format(country))
                
        for country_code in self.getListOf(offer.arr, 'COUNTRY'):
            country = self.getCountryRootByCode(country_code)
            if country is not None:
                node.relationships.create("arrival", country)
                #print("relationship country {0}".format(country))
        
        for region_code in self.getListOf(offer.dept, 'REGION'):
            region = self.getRegionRootByCode(region_code)
            if region is not None:
                node.relationships.create("departure", region)
                #print("relationship region {0}".format(region))
                
        for region_code in self.getListOf(offer.arr, 'REGION'):
            region = self.getRegionRootByCode(region_code)
            if region is not None:
                node.relationships.create("arrival", region)
                #print("relationship region {0}".format(region))       
                
        for city_name in self.getListOf(offer.dept, 'CITY'):
            city = self.getCityRootByName(city_name)
            if city is not None:
                node.relationships.create("departure", city)
                #print("relationship city {0}".format(city))   
                     
        for city_name in self.getListOf(offer.arr, 'CITY'):
            city = self.getCityRootByName(city_name)
            if city is not None:
                node.relationships.create("arrival", city)
                #print("relationship city {0}".format(city))   
                
      
    def getListOf(self,dictionary, geoplace):
        
        returnlist = list()
        if dictionary is None:
            return returnlist
        for key, value in dictionary.items():
            token, number  = key.split('_')
            if token == geoplace:
                returnlist.append(value.lower())
        return returnlist
    
    def getListOfAll(self,dictionary):
        
        returnlist = list()
        if dictionary is None:
            return returnlist
        for key, value in dictionary.items():
            returnlist.append(value)
        return returnlist
      
 
