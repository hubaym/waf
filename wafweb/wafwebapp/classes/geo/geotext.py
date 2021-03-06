from geotextcoreen import GeoTextCoreEn
from classes.constant.waflog import WafLog
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class GeoText(object):

    def __init__(self ):
        self.generateDropdown()
    
    def generateDropdown(self, language='en'):
        if language =='en':
            geo = GeoTextCoreEn()
        with open(geo.dropdownfile, 'w+') as fp:
            json.dump(geo.dropdown,fp)
        pass
        
    def process(self, listcan, language='en', typo=False):
        candidates = []
        for each in listcan:
            candidates.extend(each.split("/"))
        copy = list(listcan)
        
        if language =='en':
            geo = GeoTextCoreEn()
            
        countries = []
        country_adj = []
        cities = []
        cities_ascii = []
        cities_variant = []
        city_ids =[]
        regions =[]
        regions_adj = []
        province=[]
        continents = []
        continents_adj =[]
        
        for elem in list(candidates):
            search(elem, candidates,geo.index.cont_adj,continents_adj, typo )
        for elem in list(candidates):
            search(elem, candidates,geo.index.continents,continents, typo )
        for elem in list(candidates):
            search(elem, candidates,geo.index.regions,regions, typo )
        for elem in list(candidates):
            search(elem, candidates,geo.index.regions_adj,regions_adj, typo )
        for elem in list(candidates):
            search(elem, candidates,geo.index.country_adj,country_adj, typo )
        for elem in list(candidates):
            search(elem, candidates,geo.index.countries,countries, typo )
        
        #------------------------------------------------
        
        countries_short = [geo.index.countries_code[each.lower()] for each in countries]
        countries_short += [geo.index.country_adj_code[each.lower()] for each in country_adj]
        countries_minus= []
        if len(countries_short) > 0:
            for elem in list(candidates):
                if elem.lower() in [each.name.lower() for each in geo.index.city_more_country]:
                    
                    
                        if sum( x in countries_short for x in 
                                [each.country_code.lower() for each in geo.index.city_more_country 
                                 if each.name.lower() == elem.lower() ]) ==1:
                            for each in geo.index.city_more_country:
                                if each.name.lower() == elem.lower() and each.country_code.lower() in countries_short:
                                    city_ids.append(each.id)
                                    try:
                                        candidates.remove(elem)
                                    except ValueError as a:
                                        print(a, elem, candidates, countries_short, copy)
                                    countries_minus.append(each.country_code.lower())
                                    continue
                        else:
                            if searchCity(elem, candidates, geo.index.cities,geo.index.cities_code, cities, countries_minus):
                                continue
                            if searchCity(elem, candidates, geo.index.cities_ascii,geo.index.cities_ascii_code, cities_ascii, countries_minus):
                                continue
                            if searchCity(elem, candidates, geo.index.cities_variant,geo.index.cities_variant_code, cities_variant, countries_minus):
                                continue
                            
                else:

                    if searchCity(elem, candidates, geo.index.cities,geo.index.cities_code, cities, countries_minus):
                        continue
                    if searchCity(elem, candidates, geo.index.cities_ascii,geo.index.cities_ascii_code, cities_ascii, countries_minus):
                        continue
                    if searchCity(elem, candidates, geo.index.cities_variant,geo.index.cities_variant_code, cities_variant, countries_minus):
                        continue
                    
        else:
            for elem in list(candidates):
                searchCity(elem, candidates, geo.index.cities,geo.index.cities_code, cities, countries_minus)
            for elem in list(candidates):
                searchCity(elem, candidates, geo.index.cities_ascii,geo.index.cities_ascii_code, cities_ascii, countries_minus)
            for elem in list(candidates):
                searchCity(elem, candidates, geo.index.cities_variant,geo.index.cities_variant_code, cities_variant, countries_minus)
        
        #Check province lastly
        for elem in list(candidates):
            search(elem, candidates,geo.index.province,province, typo )          
        # only city if possible
        countries_short =list(set(countries_short) - set(countries_minus))
        #for each in list(set(countries_minus)):
        #    if each in countries_short:
        #        countries_short.remove(each)
        
        countries_id = [geo.index.countries_id[each.lower()] for each in countries_short]
        # only city if possible
        #for city in cities_ascii:
        #    if geo.index.cities_ascii[city.lower()] in countries_short:
        #        countries_short.remove( geo.index.cities_ascii[city.lower()] )
        #for city in cities:
         #   if geo.index.cities[city.lower()] in countries_short:
         #       countries_short.remove( geo.index.cities[city.lower()] )
         
        for city in cities_ascii:
            city_ids.append(geo.index.cities_ascii[city.lower()])
        for city in cities_variant:
            city_ids.append(geo.index.cities_variant[city.lower()])
        for city in cities:
            city_ids.append(geo.index.cities[city.lower()])
        cities += cities_ascii
        cities = list(set(cities))
        cities += [geo.index.cities_variant[each.lower()] for each in cities_variant]
        city_ids = list(set(city_ids))
        regions_short = [geo.index.regions[each.lower()] for each in regions]
        regions_short += [geo.index.regions_adj[each.lower()] for each in regions_adj]
        province_id = [geo.index.province[each.lower()] for each in province]
        continents_short = [geo.index.continents[each.lower()] for each in continents]
        continents_short += [geo.index.cont_adj[each.lower()] for each in continents_adj]
        
        resultdict=dict()
        if len(city_ids) > 0:
            resultdict.update(dict(zip( getVector(len(city_ids) ,'CITY'), city_ids  )))
        if len(province_id) > 0:
            resultdict.update(dict(zip(getVector(len(province_id) ,'PROVINCE'  ),province_id  )))
        if len(countries_id) > 0:
            resultdict.update(dict(zip(getVector(len(countries_id) ,'COUNTRY'  ),countries_id  )))
        if len(regions_short) > 0:
            resultdict.update(dict(zip(getVector(len(regions_short) ,'REGION'  ),regions_short  )))
        if len(continents_short) > 0:
            resultdict.update(dict(zip(getVector(len(continents_short) ,'CONTINENT'  ),continents_short  )))
        
        if 0==len(resultdict):
            if len(candidates)!=0 :
                if not typo:
                    return self.process(listcan, language, True)
                else:
                    WafLog().nerlogger.info('Could not find any geo name: %s'% candidates)
        return resultdict

def getVector( count ,text):
    result = []
    for i in range(count):
        result.append(text +'_' + str(i) if i> 9 else text + '_0'+ str(i))
    return result

def checkByFuzzy( word ,geolist):
    fuzzyword = [ (geo,fuzz.ratio(word,geo))    for geo in geolist if fuzz.ratio(word,geo)> 75 ]
    if len(fuzzyword)> 0:
        fuzzywordmax = max(fuzzyword, key=lambda x:x[1])
        WafLog().nerlogger.info('%s returned with  %s %s ' % (word, fuzzywordmax[0],fuzzywordmax[1]))
        return fuzzywordmax[0]
    else:
        return None
    
def checkByFuzzy2( word ,geolist):
    fuzzyword = process.extractOne(word, geolist.keys())
    if fuzzyword[1]> 81:
        
        WafLog().nerlogger.info('%s returned with  %s %s ' % (word, fuzzyword[0],fuzzyword[1]))
        return fuzzyword[0]
    else:
        return None
def search(element, candi, geolist, locallist, typo):
    if typo:
        fuzzyresult = checkByFuzzy(element.lower(),geolist)
        if fuzzyresult is not None:
            locallist.append(fuzzyresult)
            candi.remove(element)
    else:
        if element.lower() in geolist:
                locallist.append(element)
                candi.remove(element)
def searchCity(element, candi, geolist,geolistcode, locallist, countries_minus):
    if element.lower() in geolist:
        locallist.append(element)
        candi.remove(element)
        countries_minus.append(geolistcode[element.lower()])
        return True
    else:
        return False
   
        
if __name__ == '__main__':
    print(GeoText().process(['baltics'],language="en"))
    #print(places)
    #print('cities',places.cities).process(*['Berlin', 'Budapest'],language="en")
    #print('countries',places.countries_short)
    #print('regions',places.regions_short)
    #print('continents', places.continents_short)
    #print(fuzz.ratio('easter island','heard island and mcdonald islands'))
    #print(fuzz.ratio('caicos islands','turks and caicos islands'))
    #print(fuzz.ratio('baltic','baltics'))
   
