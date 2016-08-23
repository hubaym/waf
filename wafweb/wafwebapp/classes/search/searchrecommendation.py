import difflib
from dbconnection import DbConnection
from searchrecommendationcoreen import SearchRecommendationCoreEn


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class SearchRecommendation():
    
    def __init__(self):
        pass
    
    def getCloseMatches(self, name, language = 'en'):
        
        return difflib.get_close_matches(name,SearchRecommendationCoreEn().name)
        
        
        
if __name__ == '__main__':
    
    print(SearchRecommendation().getCloseMatches('Milan Bergamo', 'en'))
    
    