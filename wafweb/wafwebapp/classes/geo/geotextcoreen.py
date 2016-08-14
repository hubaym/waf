from collections import namedtuple
from dbconnection import DbConnection

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class GeoTextCoreEn(object):

   
    def __init__(self ):
        
        self.dbcon = DbConnection()
        
        language = "en"
        
        #lead city 2   not lead city
        #lead city 1   lead city
        #lead city 0   simple city
        
        
        city_fields_variant = 'lower(name_variant), id'
        city_variant_where = 'name_variant is not null and lead_city =1 and valid_to > CURRENT_TIMESTAMP'
        city_table = 'dn_city'
        region_fields = 'lower(name), id'
        region_table = 'dn_region'
        continent_fields = 'lower(name), id'
        continent_table = 'dn_continent'
        country_adj_fields = 'lower(adjective), id'
        country_adj_table =  'dn_country_en'
        cont_adj_fields = 'lower(adjective), id'
        cont_adj_table =  'dn_continent'
        cont_adj_where = '''language = 'en' and valid_to > CURRENT_TIMESTAMP'''
   
        countries = dict(self.dbcon.execute(fields=' lower(name), id', 
                                            table='dn_country_en', 
                                            where = 'valid_to > CURRENT_TIMESTAMP', one=False))
                         
        countries_code = dict(self.dbcon.execute(fields='lower(name), lower(iso2)',
                                                 table='dn_country_en', 
                                                 where = 'valid_to > CURRENT_TIMESTAMP', one=False))
        
        countries_id = dict(self.dbcon.execute(fields='lower(iso2), id',
                                                table='dn_country_en', 
                                                where = 'valid_to > CURRENT_TIMESTAMP', one=False))
                         
        cities = dict(self.dbcon.execute(fields='lower(name), id', 
                                         table=city_table,
                                          where = 'lead_city in (1,0)  AND valid_to > CURRENT_TIMESTAMP',
                                           one=False))
        
        cities_code = dict(self.dbcon.execute(fields='lower(name), lower(country_code)', 
                                         table=city_table,
                                          where = 'lead_city in (1,0)  AND valid_to > CURRENT_TIMESTAMP',
                                           one=False))
                         
        cities_ascii_code = dict(self.dbcon.execute(fields='lower(name_ascii), lower(country_code)', 
                                               table=city_table,
                                               where = 'lead_city in (1,0)  AND valid_to > CURRENT_TIMESTAMP',
                                                one=False))
        cities_ascii = dict(self.dbcon.execute(fields='lower(name_ascii), id', 
                                               table=city_table,
                                               where = 'lead_city in (1,0)  AND valid_to > CURRENT_TIMESTAMP and name_ascii is not null',
                                                one=False))
                         
        cities_variant_code = dict(self.dbcon.execute(fields='lower(name_variant), lower(country_code)',
                                                  table=city_table, 
                                                  where = 'name_variant is not null and lead_city in (1,0) and valid_to > CURRENT_TIMESTAMP and name_variant is not null',
                                                  one=False))
        cities_variant = dict(self.dbcon.execute(fields='lower(name_variant), id',
                                                  table=city_table, 
                                                  where = 'name_variant is not null and lead_city in (1,0) and valid_to > CURRENT_TIMESTAMP',
                                                  one=False))
        
        continents = dict(self.dbcon.execute(fields=continent_fields,
                                              table=continent_table,
                                               where = '''language = 'en' and valid_to > CURRENT_TIMESTAMP''',
                                               one=False))
                         
        regions = dict(self.dbcon.execute(fields=region_fields,
                                           table=region_table,
                                           where = '''language = 'en' and valid_to > CURRENT_TIMESTAMP''',
                                            one=False))
                         
        country_adj = dict(self.dbcon.execute(fields=country_adj_fields,
                                               table=country_adj_table,
                                               where = 'valid_to > CURRENT_TIMESTAMP and adjective is not null',
                                                one=False))
        country_adj_code = dict(self.dbcon.execute(fields='lower(adjective),lower(iso2)',
                                                    table=country_adj_table, 
                                                    where = 'valid_to > CURRENT_TIMESTAMP and adjective is not null',
                                                    one=False))
        
        
        cont_adj = dict(self.dbcon.execute(fields=cont_adj_fields,
                                            table=cont_adj_table,
                                            where = 'valid_to > CURRENT_TIMESTAMP and adjective is not null',
                                             one=False ))
        
        city_more_country = []
        citywithcountry = namedtuple('citywithcountry', 'id name country_code')
        qry = """
        with aux as 
            (select name, country_code, max(population) population from dn_city  where lead_city in (1,2) and valid_to > CURRENT_TIMESTAMP group by name,country_code having count(*) >1)
            select id, name, country_code from dn_city where lead_city in (1,2) and valid_to > CURRENT_TIMESTAMP
            except
            select dn_city.id, dn_city.name, dn_city.country_code  from dn_city, aux where dn_city.name = aux.name 
            and dn_city.country_code = aux.country_code
            and dn_city.population <> aux.population
            and dn_city.lead_city in (1,2) 
            and dn_city.valid_to > CURRENT_TIMESTAMP;
        """
        for id, name, country_code in self.dbcon.executeQuery(qry, False):
            city_more_country.append(citywithcountry(id, name, country_code))
        
        

    
        Index = namedtuple('Index', """cities cities_variant countries 
        cities_ascii continents regions country_adj cont_adj city_more_country 
        countries_code country_adj_code countries_id cities_code cities_variant_code cities_ascii_code""")
        self.index= Index(cities,cities_variant, countries, cities_ascii, 
                          continents, regions, country_adj, cont_adj, 
                          city_more_country, countries_code, country_adj_code,
                          countries_id,cities_code, cities_variant_code, cities_ascii_code)
    
if __name__ == '__main__':
    print(len(GeoTextCoreEn().index.city_more_country))
    #print('cities',places.cities)
    #print('countries',places.countries_short)
    #print('regions',places.regions_short)
    #print('continents', places.continents_short)
