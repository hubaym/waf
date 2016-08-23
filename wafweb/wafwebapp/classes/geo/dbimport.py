from dbconnection import DbConnection
import settings

class DbImport(DbConnection):
    
    def __init__(self):
        super().__init__()
        
    def importProvince(self, language):
        
        if language =='en':
            csvpath = settings.BASE_DIR + '/DB/Datasources/ds_province.csv'
            table = 'temp_province'
            
        qry = """
        TRUNCATE TABLE temp_province;
        """
        self.executeQuery(qry, None)
        self.con.commit() 
         
        qry = """
            update
                dn_province
            set 
                valid_to = CURRENT_TIMESTAMP
            where 
                valid_to = (select max(valid_to) from dn_province);  
        """
        self.executeQuery(qry, None)
        self.con.commit() 
            
        f = open(csvpath, 'r',encoding='utf8')
        if f is not None:
            f.readline()
            self.cur.copy_from(f, table, sep=';', null='')
            sql = "COPY  {0} FROM stdin DELIMITER \';\' CSV ;".format(table)
            self.cur.copy_expert(sql, f)
            self.con.commit()
            f.close()
        
        qry = """
        
        INSERT INTO dn_province
        select t.*, DATE '3000-01-01' from temp_province t;
        """
        self.executeQuery(qry, None)
        self.con.commit()
    def importCountry(self, language):
        
        if language =='en':
            csvpath = settings.BASE_DIR + '/DB/Datasources/ds_country_en.csv'
            table = 'temp_country_en'
            
        qry = """
        TRUNCATE TABLE temp_country_en;
        """
        self.executeQuery(qry, None)
        self.con.commit() 
         
        qry = """
            update
                dn_country_en
            set 
                valid_to = CURRENT_TIMESTAMP
            where 
                valid_to = (select max(valid_to) from dn_country_en);  
        """
        self.executeQuery(qry, None)
        self.con.commit() 
            
        f = open(csvpath, 'r',encoding='utf8')
        if f is not None:
            f.readline()
            self.cur.copy_from(f, table, sep=';', null='')
            sql = "COPY  {0} FROM stdin DELIMITER \';\' CSV ;".format(table)
            self.cur.copy_expert(sql, f)
            self.con.commit()
            f.close()
        
        qry = """
        
        INSERT INTO dn_country_en
        select t.*, DATE '3000-01-01' from temp_country_en t;
        """
        self.executeQuery(qry, None)
        self.con.commit()
     
    def importContinent(self, language):
        
        if language =='en':
            csvpath = settings.BASE_DIR + '/DB/Datasources/ds_continent.csv'
            table = 'temp_continent'
        
        qry = """
        TRUNCATE TABLE temp_continent;
        """
        self.executeQuery(qry, None)
        self.con.commit() 
        
        qry = """
            update
                dn_continent
            set 
                valid_to = CURRENT_TIMESTAMP
            where 
                valid_to = (select max(valid_to) from dn_continent);  
        """
        self.executeQuery(qry, None)
        self.con.commit()       
            
        f = open(csvpath, 'r',encoding='utf8')
        if f is not None:
            f.readline()
            self.cur.copy_from(f, table, sep=';', null='')
            sql = "COPY  {0} FROM stdin DELIMITER \';\' CSV ;".format(table)
            self.cur.copy_expert(sql, f)
            self.con.commit()
            f.close()
        
        qry = """
        
        INSERT INTO dn_continent
        select t.*, DATE '3000-01-01' from temp_continent t;
        """
        self.executeQuery(qry, None)
        self.con.commit()
           
    def importRegion(self, language):
        
        if language =='en':
            csvpath = settings.BASE_DIR + '/DB/Datasources/ds_region.csv'
            table = 'temp_region'
        
        qry = """
        TRUNCATE TABLE temp_region;
        """
        self.executeQuery(qry, None)
        self.con.commit()   
        
        qry = """
            update
                dn_region
            set 
                valid_to = CURRENT_TIMESTAMP
            where 
                valid_to = (select max(valid_to) from dn_region);  
        """
        self.executeQuery(qry, None)
        self.con.commit()     
            
        f = open(csvpath, 'r',encoding='utf8')
        if f is not None:
            f.readline()
            self.cur.copy_from(f, table, sep=';', null='')
            sql = "COPY  {0} FROM stdin DELIMITER \';\' CSV ;".format(table)
            self.cur.copy_expert(sql, f)
            self.con.commit()
            f.close()
        
        qry = """
        
        INSERT INTO dn_region
        select t.*, DATE '3000-01-01' from temp_region t;
        """
        self.executeQuery(qry, None)
        self.con.commit()
        
    def importCity(self, language):
        
        if language =='en':
            csvpath = settings.BASE_DIR + '/DB/Datasources/ds_city.csv'
            table = 'temp_city'
        
        qry = """
        TRUNCATE TABLE temp_city;
        """
        self.executeQuery(qry, None)
        self.con.commit()  
        
        qry = """
            UPDATE
               dn_city
            set 
                valid_to = CURRENT_TIMESTAMP
            where 
                valid_to = (select max(valid_to) from dn_city);  
        """
        self.executeQuery(qry, None)
        self.con.commit()      
            
        f = open(csvpath, 'r',encoding='utf8')
        if f is not None:
            f.readline()
            self.cur.copy_from(f, table, sep=';', null='')
            sql = """COPY  {0} FROM stdin DELIMITER \';\' CSV ;""".format(table)
            self.cur.copy_expert(sql, f)
            self.con.commit()
            f.close()
            
   
        qry = """
        
               update temp_city set lead_city = 0;
                """
        self.executeQuery(qry, None)
        self.con.commit()

        qry = """
        
               update temp_city dn set lead_city = (
                select
                case when count(*) = 1 then 1
                when count(*) = 0 then 2 END
                from
                    (
                select name, max(population) as population from temp_city 
                    group by name having count(*)>1
                ) as aux
                where dn.name = aux.name and aux.population = dn.population
                )
                where dn.name in (
                select name from temp_city 
                    group by name having count(*)>1
                )
                ;
                """
        self.executeQuery(qry, None)
        self.con.commit()
        
        qry = """
        
        INSERT INTO dn_city (id, name, name_ascii, latitude, langitude, population, country, country_code
        ,country_code_3,province,name_hu,name_variant, lead_city, valid_to)
        select t.*, DATE '3000-01-01' from temp_city t;
        """
        self.executeQuery(qry, None)
        self.con.commit()

        
            
if __name__ == '__main__':
    # you want to initialize the class
    database   = DbImport()
    #database.importContinent('en')    
    database.importRegion('en')    
    database.importProvince('en') 
    #database.importCountry('en')    
    #database.importCity('en')
    
    database.close()
    print('done')