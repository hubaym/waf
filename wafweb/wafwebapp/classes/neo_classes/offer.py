
class Offer:
    
    def __init__(self,mongoid,tweetid, dept,
                 arr, created_at,
                 text,
                 language="en",
                 source_lev_1=None,
                 source_lev_2=None,
                 links = None,
                 status = None
                 ):
        self.mongoid = mongoid
        self.tweetid = tweetid
        self.dept = dept
        self.arr = arr
        self.created_at = created_at
        self.text = text
        self.language = language
        self.source_lev_1=source_lev_1
        self.source_lev_2=source_lev_2
        self.links = links
        self.status = status
        
        
    
        
