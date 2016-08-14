
class WrongSearchException(Exception):
	

	def __init__(self,*args,**kwargs):
		self.__type = 'WrongSearchException'
		Exception.__init__(self,self.__type,__name__, *args,**kwargs)

if __name__ == "__main__":
	try:
		if 5 ==5:
			raise WrongSearchException('5 is equall woth 5', 'one more comment')
	except WrongSearchException as e:
		print (e)