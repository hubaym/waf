
class WrongGeoNameException(Exception):
	
	def __init__(self,*args,**kwargs):
		self.__type = 'WrongGeoNameException'
		Exception.__init__(self,self.__type,__name__, *args,**kwargs)
		
		
		

if __name__ == "__main__":
	try:
		if 5 ==5:
			raise WrongGeoNameException('5 is equall woth 5', 'one more comment')
	except WrongGeoNameException as e:
		print (e)