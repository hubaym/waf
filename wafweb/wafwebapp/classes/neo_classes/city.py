 
class City:
    
    def __init__(self,id, name, country_code = ' ',
                 lat = ' ', lan = ' ',                
                 province = ' ',
                 language="en",
                 name_foreign = ' '
                 ):
        self.pgid = id
        self.name = name
        self.lat = lat
        self.lan = lan
        self.country_code = country_code
        self.language = language
        self.name_foreign = name_foreign
        self.province = province
        
    
    