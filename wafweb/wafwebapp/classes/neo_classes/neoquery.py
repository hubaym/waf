from neo4jrestclient import client
import classes.constant.wafconnection as con
from neo4jrestclient.client import GraphDatabase
from classes.constant.waflog import WafLog
import classes.utils.status as status

class NeoQuery():
	def __init__(self):
		self.db = GraphDatabase(con.NEO_HOST, 
							username=con.NEO_USER,
							password=con.NEO_PSW)
	
	def getGeoByID(self,id):
		q1 = '''pgid:{0}'''.format(id)
		q = '''
		MATCH (n:geo{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info(" {0} not found".format(id))
			return None
		return result[0][0]
		
	def getCountryByCode(self,country_code):
		q1 = '''code:"{0}"'''.format(country_code)
		q = '''
		MATCH (n:geo_country{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("country {0} not found".format(country_code))
			return None
		return result[0][0]
	
	def getNodeByNameAndType(self,name, type):
		q1 = '''name:"{0}"'''.format(name)
		q = '''
		MATCH (n:{0}{''' + q1+ '''}) 
		RETURN n'''.format(type)
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("name {0} not found".format(name))
			return None
		return result[0][0]
	
	
	def getUserById(self,userid):
		q1 = '''pgid:"{0}"'''.format(userid)
		q = '''
		MATCH (n:user{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("userid {0} not found".format(userid))
			return None
		return result[0][0]
	
	def getCountryByName( self, name):
		q1 = '''name:"{0}"'''.format(name)
		q = '''
		MATCH (n:geo_country{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("country {0} not found".format(name))
			return None
		return result[0][0]

	def getProvinceByName( self, name):
		q1 = '''name:"{0}"'''.format(name)
		q = '''
		MATCH (n:geo_province{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("country {0} not found".format(name))
			return None
		return result[0][0]

	
	def getCityByName(self, name):
		q1 = '''name:"{0}"'''.format(name)
		q = '''
		MATCH (n:geo_city{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("city {0} not found".format(name))
			return None
		return result[0][0]

	def getContinentByCode(self, continent):
		q1 = '''code:"{0}"'''.format(continent)
		q = '''
		MATCH (n:geo_continent{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("continent {0} not found".format(continent))
			return None
		return result[0][0]

	def getRegionByCode(self, region):
		q1 = '''code:"{0}"'''.format(region)
		q = '''
		MATCH (n:geo_region:{''' + q1+ '''}) 
		RETURN n'''
		result = self.db.query(q, returns=(client.Node))
		if len(result) == 0:
			WafLog().neologger.info("region {0} not found".format(region))
			return None
		return result[0][0]
	
	def isNeighbourExists(self, country_code_1, country_code_2):
		q1 = '''code:"{0}"'''.format(country_code_1)
		q2 = '''code:"{0}"'''.format(country_code_2)
		q = '''
		MATCH (n:geo_country{''' + q1+ '''}) -[r:neighbour]- 
		(m:geo_country{''' + q2+'''})
		RETURN r'''
		result = self.db.query(q, returns=(client.Relationship))
		if len(result) == 0:
			return False
		else:
			return True
		
	def deleteOffers(self):
		q = """
		MATCH (n:offer) detach delete n"""
		self.db.query(q)
		WafLog().neologger.info("db is deleted")
			
	def createIndexOnCountry(self):
		q ="""CREATE INDEX ON :geo_country(country_code) """
		self.db.query(q)
		WafLog().neologger.info("index is created on Countries")
		
	def createIndexOnCity(self):
		q ="""CREATE INDEX ON :geo_city(name) """
		self.db.query(q)
		WafLog().neologger.info("index is created on cities")
		
	def createIndexOnGeo(self):
		q ="""CREATE INDEX ON :geo(pgid) """
		self.db.query(q)
		WafLog().neologger.info("index is created on geo, pgid")
		
	def createIndexOnProvince(self):
		q ="""CREATE INDEX ON :geo_province(name) """
		self.db.query(q)
		WafLog().neologger.info("index is created on geo_province, name")	
		
		
	def deleteDB(self):
		q = """
		MATCH (n) detach delete n"""
		self.db.query(q)
		WafLog().neologger.info("db is deleted")
	
	def getAllCityID(self):
		q = """
		MATCH (n:geo_city) RETURN ID(n)"""
		result = self.db.query(q)
		return(result)
	
	def getOffersAndUsers(self):
		q = """
		MATCH (o:offer) -[]-
		WHERE o.status = 'IN_NEO_EMAIL_NOT_DONE'
		RETURN ID(n)"""
		result = self.db.query(q)
		return(result)
		
if __name__ == "__main__":
	neoq = NeoQuery()
	WafLog().neologger.info (neoq.getGeoByID(50024))