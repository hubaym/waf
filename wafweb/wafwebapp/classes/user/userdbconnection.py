from dbconnection import DbConnection
from waflog import WafLog
import psycopg2
from _ast import Try

class UserDbConnection(DbConnection):
    
    def __init__(self):
        super().__init__()
        
        
    def getHashforUser(self, email):
        
        result = self.execute( fields ='hash', 
                     table='waf_user',
                      where= """
                      email_auth='{0}'
                    """.format(email), one = True)
        
        if result is None:
            raise Exception('No User found for this email')
        else:
            return result[0]
        
    def isUserExists(self, email):
        
        result = self.execute( fields='email_auth', table='waf_user',
                                where="""email_auth = '%s'"""% (email),
                                 one=True)
        if result is None or len(result)==0:
            return False
        else:
            return True
    def insertNewUser(self, user):
        
        
        if self.isUserExists(user.email_auth):
            raise Exception('User is already exists')
        
        if user.hash is not None:
            resp = self.executeInsert(table = 'waf_user',
                            fields='email_auth, email_subs, hash',
                            values= " '%s','%s', %s" % (user.email_auth, user.email_subs, psycopg2.Binary(user.hash)))
                              
        
        else:
            resp = self.executeInsert(table = 'waf_user',
                              fields='email_auth, email_subs',
                              values= """ '{0}','{1}'""".format(user.email_auth, user.email_subs))
            
        self.con.commit() 
        
        WafLog().neologger.info(resp)
        
        