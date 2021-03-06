from dbconnection import DbConnection
from continent import Continent
from country import Country
from city import City
from region import Region
from geotoneo import GeoToNeo
import time
from waflog import WafLog
from spatialapi import SpatialApi
from classes.neo_classes.province import Province
  


class NeoLoader:
  

    def __init__(self):
        
        self.neodb = GeoToNeo()
        self.db = DbConnection()
        
    def initContinent(self, language ='en'):
        table_continent = "dn_continent_en_neo"
        fields_continent = "id, lower(name), lower(short_name), lower(language)"
        where_continent = """language = '{0}'  """.format(language)
        self.continent = self.db.execute(fields=fields_continent, table=table_continent, where=where_continent, one=False)
    
    def initRegion(self, language ='en'):
        table_continent = "dn_region_en_neo"
        fields_continent = "id, lower(name), lower(short_name), lower(country_list), lower(language)"
        where_continent = """language = '{0}' and root = 'True'  """.format(language)
        self.region = self.db.execute(fields=fields_continent, table=table_continent, where=where_continent, one=False)
        
    def initProvince(self, language ='en'):
        table_continent = "dn_province_en_neo"
        fields_continent = "id, lower(name), lower(country_code)"
        self.province = self.db.execute(fields=fields_continent, table=table_continent, where=None, one=False)
        
    def initCountry(self, language ='en'):
        if language  =='en':
            table_country = "dn_country_en_neo"
            fields_contry = "id, lower(country_code),lower(name), lower(continent)"
        elif language  =='hu':
            table_country = "dn_country_hu_neo"
            fields_contry = "country_code,country_hu"
        
        self.country = self.db.execute(fields=fields_contry, table=table_country, one=False)
        
    def initCity(self):
        table_city = "dn_city_en_neo"
        fields_city = "id, lower(name) ,lower(country_code), lat, lan, lower(province)"
        self.city_root = self.db.execute(fields=fields_city, table=table_city, one=False)
        
    def initCityHu(self):
        table_city = "dn_city_hu_neo"
        fields_city = "id, lower(name_hu) ,lower(country_code), lat, lan, name"
        self.city_hu = self.db.execute(fields=fields_city, table=table_city, one=False)
        
    def initNeighbours(self):
        table_country = "dn_country_en_neo"
        fields_contry = "lower(country_code), lower(neighbours)"
        self.country_neighbours = self.db.execute(fields=fields_contry, table=table_country, one=False)
        
    def loadContinent(self, list_cont):
        for actual in list_cont:
            self.initContinent(actual)
            WafLog().neologger.info('start to create continents')
            
            for cont in self.continent:
                conti = Continent(cont[0],cont[1],cont[2],  language= actual)
                self.neodb.createContinent(conti)
            
    
        
    def loadCountry(self, list_cont):
        for actual in list_cont:
            self.initCountry(actual)
            WafLog().neologger.info('start to create countries')
            i = 0
            for count in self.country:
                country = Country(count[0],count[1],count[2], continent = count[3], language = actual)
                self.neodb.createCountry(country)
                i+=1
                if i%50 ==0:
                    WafLog().neologger.info(i)
                    
    def loadRegion(self):
        WafLog().neologger.info('start to create regions')
        i = 0
        start_time = time.time()
        self.initRegion('en')
        
        for region in self.region:
            reg = Region(region[0],region[1], region[2], region[3],region[4])
            self.neodb.createRegion(reg)
            i+=1
            if i%500 ==0:
                elapsed_time = time.time() - start_time
                WafLog().neologger.info("n: {0} elapsed: {1}".format(i,elapsed_time))
                start_time = time.time()
    def loadProvince(self):
        self.initProvince()
        WafLog().neologger.info('start to create provinces')
        i = 0
        start_time = time.time()
        # your code
        
        for province in self.province:
            provi = Province(province[0],province[1], province[2])
            self.neodb.createProvince(provi)
            i+=1
            if i%500 ==0:
                elapsed_time = time.time() - start_time
                WafLog().neologger.info("n: {0} elapsed: {1}".format(i,elapsed_time))
                start_time = time.time()
                       
    def loadCity(self):
        self.initCity()
        WafLog().neologger.info('start to create cites')
        i = 0
        start_time = time.time()
        # your code
        
        for city in self.city_root:
            cit = City(city[0],city[1], city[2], city[3], city[4], city[5])
            self.neodb.createCity(cit)
            i+=1
            if i%500 ==0:
                elapsed_time = time.time() - start_time
                WafLog().neologger.info("n: {0} elapsed: {1}".format(i,elapsed_time))
                start_time = time.time()
                
    def loadCityHu(self):
        self.initCityHu()
        WafLog().neologger.info('start to create hun cites')
        i = 0
        start_time = time.time()
        # your code
        
        for city in self.city_hu:
            cit = City(city[0],city[1], city[2], city[3], city[4], language="hu", name_foreign =city[5] )
            self.neodb.createCity(cit)
            i+=1
            if i%500 ==0:
                elapsed_time = time.time() - start_time
                WafLog().neologger.info("n: {0} elapsed: {1}".format(i,elapsed_time))
                start_time = time.time()
    
    
    
    def connectCountries(self):
        self.initNeighbours()
        WafLog().neologger.info('start to create neighbours')
        for country in self.country_neighbours:
            if country[1] is not None:
                for neig in self.getNeighbourList(country[1]):
                    self.neodb.makeCountryConnection(country[0], neig)
                
    def getNeighbourList(self, liststring):
        resultlist = liststring.split(',')
        return resultlist
    
    def deleteDB(self):
        self.neodb.deleteDB()
        
    def createIndexOnCountry(self):
        self.neodb.createIndexOnCountry()
        
    def createIndexOnCity(self):
        self.neodb.createIndexOnCity()
    def createIndexOnGeo(self):
        self.neodb.createIndexOnGeo()
    def createIndexOnProvince(self):
        self.neodb.createIndexOnProvince()
           
if __name__ == "__main__":
    continents = {'en'}
    countries = {'en'}
    drop = False
    neotest = NeoLoader()
    spatialapi = SpatialApi()
    if drop: 
        neotest.deleteDB()
    #neotest.loadContinent(continents)
    
    #neotest.loadCountry(countries)
    #neotest.createIndexOnCountry()
    #neotest.connectCountries()
    
    #neotest.loadRegion()
    #neotest.loadProvince()
    #neotest.createIndexOnProvince()
    
    #neotest.loadCity()    
    #neotest.createIndexOnCity()  
    #neotest.createIndexOnGeo()  
    #neotest.loadCityHu()
    #spatialapi.addPointLayer("geomlayer")
    #spatialapi.addSpatialIndex("geomlayer")
    spatialapi.addAllNodeToIndex("geomlayer")
    
    