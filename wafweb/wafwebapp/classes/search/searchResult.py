

class SearchResult():
    
    def __init__(self, created_at, text, language,source1, source2, point):
        self.created_at = created_at
        self.text = text
        self.language = language
        self.source1 = source1
        self.source2 = source2
        self.point = point + self.dateToPoint()
        
        
    def dateToPoint(self):
        
        return 1
    
    def pretty(self):
        return self.created_at +'----' + self.language + '-----'+ self.text[:120]
    
    def getDict(self):
        return self.__dict__
    
    def prettyPrint(self):
        print ('datum: ', self.created_at, 'language:', self.language, 'text: ', self.text[:40])
        
