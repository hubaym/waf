import psycopg2
import sys
import classes.constant.wafconnection as wcon
from classes.constant.waflog import WafLog


class DbConnection:
    
    
    def __init__(self):
        self.initconnection()
        
    def initconnection(self):
        try:
         
            self.con = psycopg2.connect(database=wcon.POSTG_DBNAME, 
                                        user=wcon.POSTG_USER, 
                                        password=wcon.POSTG_PSW, 
                                        host=wcon.POSTG_HOST, 
                                        port=wcon.POSTG_PORT)
            self.cur = self.con.cursor()
        
            
    
        except psycopg2.DatabaseError as e:
            print ('Error %s' % e)    
            sys.exit(1)
        
    def execute(self, fields='*', table='dual', where=None, one=True):
        self.query = self.querybuilder(fields, table, where)
        WafLog().neologger.info(self.query)
        return self.executeQuery( self.query, one)
    
    def executeInsert(self, fields, table, values):
        self.query = self.querybuilderinsert(fields, table, values)
        WafLog().neologger.info(self.query)
        return self.executeQuery( self.query, None)

    def executeQuery(self, querystr, one):

        try:
            self.cur.execute(querystr)
        
            if one is not None:
                if one:
                    res = self.cur.fetchone()
                    return res
                else:
                    res = self.cur.fetchall()
                    return res
            
            
        
    
        except psycopg2.DatabaseError as e:
            print ('Error %s' % e)    
            sys.exit(1)
        
                
    def querybuilder(self, fields='*', table='dual', where=None, one=True):
    
        query = 'SELECT '
        query += fields
        if table is not None:
            query += ' from ' + table
        else:
            query += ' '
        
        if where is not None:
            query += ' where ' + where
            
        query +=';'
        
        return (query)
    
    def querybuilderinsert(self, fields='*', table='dual', values = None):
    
        query = 'INSERT INTO '
        query += table
        query += """
         ( {0}  )       
        
        """.format(fields)
        query += """
         VALUES( {0}  )       
        
        """.format(values)
        query +=';'
        
        return (query)
    
    def close(self):
        if self.con:
            self.con.close()
        
                
                
if __name__ == "__main__":
    dbcon = DbConnection()
    result= dbcon.execute(fields=" 'test' ", table=None, one=True)
    dbcon.close()
    print(result)
