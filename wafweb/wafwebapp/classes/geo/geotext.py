from geotextcoreen import GeoTextCoreEn

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
        pass
        
    def process(self, listcan, language='en'):
        candidates = listcan
        copy = list(listcan)
        
        if language =='en':
            geo = GeoTextCoreEn()
            
        
        countries = []
        country_adj = []
        cities = []
        cities_ascii = []
        cities_variant = []
        regions = []
        continents = []
        continents_adj = []
        countries_short = []
        
        city_ids = []
        
        for elem in list(candidates):
            if elem.lower() in geo.index.cont_adj:
                continents_adj.append(elem)
                candidates.remove(elem)
        for elem in list(candidates):
            if elem.lower() in geo.index.continents:
                continents.append(elem)
                candidates.remove(elem)
        for elem in list(candidates):
            if elem.lower() in geo.index.regions:
                regions.append(elem)
                candidates.remove(elem)
        for elem in list(candidates):
            if elem.lower() in geo.index.country_adj:
                country_adj.append(elem)
                candidates.remove(elem)
        for elem in list(candidates):
            if elem.lower() in geo.index.countries:
                countries.append(elem)
                candidates.remove(elem)
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
                            if elem.lower() in geo.index.cities:
                                cities.append(elem)
                                candidates.remove(elem)
                                countries_minus.append(geo.index.cities_code[elem.lower()])
                                continue
                            if elem.lower() in geo.index.cities_ascii:
                                cities_ascii.append(elem)
                                candidates.remove(elem)
                                countries_minus.append(geo.index.cities_ascii_code[elem.lower()])
                                continue
                            if elem.lower() in geo.index.cities_variant:
                                cities_variant.append(elem)
                                candidates.remove(elem)
                                countries_minus.append(geo.index.cities_variant_code[elem.lower()])
                                continue
                            
                else:

                    if elem.lower() in geo.index.cities:
                        cities.append(elem)
                        candidates.remove(elem)
                        countries_minus.append(geo.index.cities_code[elem.lower()])
                        continue
                    if elem.lower() in geo.index.cities_ascii:
                        cities_ascii.append(elem)
                        candidates.remove(elem)
                        countries_minus.append(geo.index.cities_ascii_code[elem.lower()])
                        continue
                    if elem.lower() in geo.index.cities_variant:
                        cities_variant.append(elem)
                        candidates.remove(elem)
                        countries_minus.append(geo.index.cities_variant_code[elem.lower()])
                        continue
                    
        else:
            for elem in list(candidates):
                if elem.lower() in geo.index.cities:
                    cities.append(elem)
                    candidates.remove(elem)
                    countries_minus.append(geo.index.cities_code[elem.lower()])
            for elem in list(candidates):
                if elem.lower() in geo.index.cities_ascii:
                    cities_ascii.append(elem)
                    candidates.remove(elem)
                    countries_minus.append(geo.index.cities_ascii_code[elem.lower()])
            for elem in list(candidates):
                if elem.lower() in geo.index.cities_variant:
                    cities_variant.append(elem)
                    candidates.remove(elem)
                    countries_minus.append(geo.index.cities_variant_code[elem.lower()])
                    
         # only city if possible
        for each in list(set(countries_minus)):
            if each in countries_short:
                countries_short.remove(each)
        
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
        continents_short = [geo.index.continents[each.lower()] for each in continents]
        continents_short += [geo.index.cont_adj[each.lower()] for each in continents_adj]
        
        #
        # countries = self.countries_short
        # city = self.cities
        # regions = self.regions
        # continetns = self.continents
        #
        resultdict=dict()
        if len(city_ids) > 0:
            city_dict = dict(zip( getVector(len(city_ids) ,'CITY'), city_ids  ))
            resultdict.update(city_dict)
        if len(countries_short) > 0:
            country_dict = dict(zip(getVector(len(countries_id) ,'COUNTRY'  ),countries_id  ))
            resultdict.update(country_dict)
        if len(regions_short) > 0:
            country_dict = dict(zip(getVector(len(regions_short) ,'REGION'  ),regions_short  ))
            resultdict.update(country_dict)
        if len(continents_short) > 0:
            country_dict = dict(zip(getVector(len(continents_short) ,'CONTINENT'  ),continents_short  ))
            resultdict.update(country_dict)
        return resultdict

def getVector( count ,text):
    result = []
    for i in range(count):
        result.append(text +'_' + str(i) if i> 9 else text + '_0'+ str(i))
    return result
    
    
   
        
if __name__ == '__main__':
    print(GeoText().process(['köln'],language="en"))
    #print(places)
    #print('cities',places.cities).process(*['Berlin', 'Budapest'],language="en")
    #print('countries',places.countries_short)
    #print('regions',places.regions_short)
    #print('continents', places.continents_short)