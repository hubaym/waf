from neoquery import NeoQuery
from waflog import WafLog
import classes.constant.neoconstant as neoc

class GeoToNeo(NeoQuery):
    
    def __init__(self):
        super().__init__()
        
    def createContinent(self, continent):
        node = self.db.nodes.create(name = continent.name, pgid=continent.pgid,
                        code = continent.cont_code,
                        language = continent.language)
        geo = self.db.labels.create(neoc.LABEL_GEO)
        geo.add(node)   
        conti = self.db.labels.create(continent.label)
        conti.add(node)
        
    def createRegion(self, region):
        node = self.db.nodes.create(name = region.name, pgid=region.pgid,
                        code = region.short_name,
                        language = region.language
                        )
        geo = self.db.labels.create(neoc.LABEL_GEO)
        geo.add(node)
        regionlabel = self.db.labels.create(region.label)
        regionlabel.add(node)
        
        for country_code in region.country_list.replace("\"","").split(','):
            country = self.getCountryByCode(country_code)
            if country is not None:
                node.relationships.create(neoc.LABEL_CONTAINS, country)
                    
    def createCountry(self, country):
        node = self.db.nodes.create(name=country.name, pgid=country.pgid,
                        code=country.country_code,
                        language=country.language)
        
        geo = self.db.labels.create(neoc.LABEL_GEO)
        geo.add(node)
        countrylabel = self.db.labels.create(country.label)
        countrylabel.add(node)
        WafLog().neologger.info("Country created {0} {1} ".format(country.name, country.country_code))
        
        if country.continent is not None and country.continent is not ' ':
            conti = self.getContinentByCode(country.continent)
         
            if conti is None:
                WafLog().neologger.info ("could not make connection {0} {1}".format(country.name, country.continent))
            else:
                    conti.relationships.create(neoc.LABEL_CONTAINS, node)
                    #WafLog().neologger.info ("relationship created")
                
        
    def makeCountryConnection(self, home, country_code):
        
        if not self.isNeighbourExists(home, country_code):
            node = self.getCountryByCode(home)
            neig = self.getCountryByCode(country_code)
            if node is None or neig is None:
                WafLog().neologger.info("neighbours cannot find {0} {1}".format(home,country_code))
            else:
                node.relationships.create(neoc.LABEL_NEIGHBOUR, neig)
        
    def createCity(self, city):
        node = self.db.nodes.create(name = city.name, 
                                     pgid=city.pgid,
                        country_code = city.country_code,
                        language = city.language,
                        lat = city.lat,
                        lan = city.lan)
        geo = self.db.labels.create(neoc.LABEL_GEO)
        geo.add(node)   
        citylabel = self.db.labels.create(city.label)
        citylabel.add(node)
        
        if city.country_code is not None and city.country_code is not ' ':
            country = self.getCountryByCode(city.country_code)
            if country is not None:
                country.relationships.create(neoc.LABEL_CONTAINS, node)
        
               
      
 