from searchmanager import SearchManager
from searchcriteria import SearchCriteria

class SearchModel:
    
    def __init__(self, depart, arrival):
      
        manager = SearchManager()
        manager.search(SearchCriteria(depart, arrival))
        self.result = manager.getDictList()
    
    def returnResult(self):
        return self.result 