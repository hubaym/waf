from neo4jrestclient.client import GraphDatabase
from wrongsearchexception import WrongSearchException
import classes.constant.wafconnection as con
from searchcriteria import SearchCriteria
from spatialapi import SpatialApi

class NeoSearchQuery():
	def __init__(self):
		self.db = GraphDatabase(con.NEO_HOST, 
							username=con.NEO_USER, 
							password=con.NEO_PSW)
	
	
	def getDepartureGeometry(self, criteria):
		q="""
		match(c:criteria)-[:subsdept]-(dept:geo_city)
		where ID(c)={0} 
		return dept.lan, dept.lat
		""".format(criteria.criteriaid )
		result = self.db.query(q)
		return result
	def getArrivalGeometry(self, criteria):
		q="""
		match(c:criteria)-[:subsarr]-(dept:geo_city)
		where ID(c)={0} 
		return dept.lan, dept.lat
		""".format(criteria.criteriaid )
		result = self.db.query(q)
		return result
	def seachByCriteria(self, criteria):
		
		if criteria.departure is not None and criteria.arrival is not None:
			
			deptgeometry = self.getDepartureGeometry(criteria)
			arrgeometry = self.getArrivalGeometry(criteria)
			aroundDept = []
			aroundArr = []
			if deptgeometry or arrgeometry:
				spatial = SpatialApi()
				if deptgeometry:
					print(deptgeometry[0])
					aroundDept = spatial.findGeometriesWithinDistance("geomlayer", deptgeometry[0][0], deptgeometry[0][1], criteria.deptDistance)
				if arrgeometry:
					print(arrgeometry[0])
					aroundArr = spatial.findGeometriesWithinDistance("geomlayer", arrgeometry[0][0], arrgeometry[0][1], criteria.arrDistance)
		
			q="""   
			match (o:offer)-[:departure]-(n)<-[:contains*0..3]-(dept:geo)-[:subsdept]-(c:criteria)
			match (o:offer)-[:arrival]->(m)<-[:contains*0..3]-(arr:geo)-[:subsarr]-(c:criteria)
			where ID(c)={0} 
			return o,50 as point
			UNION
			match (o:offer)-[:departure]-(n)<-[:contains*0..3]-(dept:geo)-[:subsdept]-(c:criteria)
			match (o:offer)-[:arrival]-(m)<-[:contains*0..1]-(arr_country:geo_country)-[:contains]->(arr:geo_city)-[:subsarr]-(c:criteria)
			where ID(c)={0}  
			return o, 20 as point
			UNION
			match (o:offer)-[:departure]-(n)<-[:contains*0..3]-(dept:geo)
			match (o:offer)-[:arrival]->(m)<-[:contains*0..3]-(arr:geo)
			where dept.pgid in {1} and arr.pgid in {2}   
			return o,30 as point
			order by o.created_at desc
			""".format(criteria.criteriaid, aroundDept, aroundArr )
			print(q)
			result = self.db.query(q)
			return(result)
		
	def seachByCriteriaNode(self, criteria):
		
		if criteria.departure is not None and criteria.arrival is not None:
		
			q="""   
			match (o:offer)-[:departure]-(n)<-[:contains*0..3]-(dept)
			match (o:offer)-[:arrival]->(arr:geo_city)
			where dept.name='{0}' and arr.name='{1}'
			return o,50 as point
			UNION
			match (o:offer)-[:departure]-(n)<-[:contains*0..3]-(dept)
			match (o:offer)-[:arrival]-(m)<-[:contains*0..1]-(arr_country:geo_country)<-[:contains]->(arr:geo_city)
			where dept.name='{0}' and arr.name='{1}'
			return o, 20 as point
			order by o.created_at desc
			""".format(criteria.departure.lower(),criteria.arrival.lower()   )
			result = self.db.query(q)
			return(result)	
	
	def getPerfectMatch(self, departure, departureType, arrival, arrivalType):
		try:
			deptlabel = self.getlabel(departureType)
			arrlabel = self.getlabel(arrivalType )
		except WrongSearchException as e:
			raise e
		if deptlabel is None and arrlabel is None:
			raise WrongSearchException('At least one field should be filled')
		
		if deptlabel is not None and arrlabel is not None:
			
			q = """
			MATCH (o:offer)-[:departure]-(c_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE c_dept.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result = self.db.query(q)
			return(result)
		
		if deptlabel is None:
			
			q = """
			MATCH (o:offer)-[:arrival]-(c_arr:{0}) 
			WHERE c_arr.name = '{1}' 
			RETURN o""".format(arrlabel,arrival.lower()   )
			result = self.db.query(q)
			return self.getResult(result)
	
	def getMatchDeptCountry(self, departure, departureType, arrival, arrivalType):
		try:
			deptlabel = self.getlabel(departureType, 'CITY', 'COUNTRY')
			arrlabel = self.getlabel(arrivalType )
		except WrongSearchException as e:
			raise e
		
		if departureType =='CITY':
			q = """
			MATCH (o:offer)-[:departure]-(c_dept_cou:geo_city)-
			[:contains]-(count_dept:geo_country)-[:contains]-(c_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE c_dept.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result = self.db.query(q)
		if departureType =='COUNTRY':
			q = """
			MATCH (o:offer)-[:departure]-(c_dept_cou:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE c_dept_cou.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result = self.db.query(q)
		return self.getResult(result)
	
	def getMatchDeptNeighCountry(self, departure, departureType, arrival, arrivalType):
		try:
			deptlabel = self.getlabel(departureType, 'CITY', 'COUNTRY' )
			arrlabel = self.getlabel(arrivalType )
		except WrongSearchException as e:
			raise e
		
		if departureType =='CITY':
			q = """
			MATCH (o:offer)-[:departure]-(c_dept_cou:geo_city)-
			[:contains]-(count_dept_neigh:geo_country)-[:neighbour]-(count_dept:geo_country)-[:contains]-(c_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE c_dept.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result1 = self.db.query(q)
			q = """
			MATCH (o:offer)-[:departure]-(count_dept_neigh:geo_country)-[:neighbour]-(count_dept:geo_country)-[:contains]-(c_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE c_dept.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result2 = self.db.query(q)
		if departureType =='COUNTRY':
			q = """
			MATCH (o:offer)-[:departure]-(c_dept_cou:geo_city)-
			[:contains]-(count_dept_neigh:geo_country)-[:neighbour]-(count_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE count_dept.code = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result1 = self.db.query(q)
			q = """
			MATCH (o:offer)-[:departure]-(count_dept_neigh:geo_country)-[:neighbour]-(count_dept:{0})
			MATCH (o:offer)-[:arrival]-(c_arr:{1}) 
			WHERE count_dept.name = '{2}'and c_arr.name = '{3}' 
			RETURN o""".format(deptlabel,arrlabel,departure.lower(),arrival.lower()   )
			result2 = self.db.query(q)
		
		return self.getResult(result1, result2)
	
	def getlabel(self, type, *filter):
		
		if type is None:
			return None
		
		if len(filter) > 0:
			if type not in filter:
				raise WrongSearchException('wrong type for filter criteria')
			
		if type =='CITY':
			return('geo_city')
		if type =='COUNTRY':
			return('geo_country')
		if type =='REGION':
			return('geo_region')
		if type =='CONTINENT':
			return('geo_continent')
		raise WrongSearchException('wrong arrival or departure type')
	

	def getResult(self, *results):
		l = list()
		for result in results:
			for elem in result:
				l.append(elem)
		return l
	
if __name__ == "__main__":
	neoq = NeoSearchQuery()
		
	