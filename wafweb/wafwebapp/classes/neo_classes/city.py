 
class City:
    
    def __init__(self,id, name, country_code = ' ',
                 lat = ' ', lan = ' ', 
                 label='geo_city',
                 language="en",
                 name_foreign = ' '
                 ):
        self.pgid = id
        self.name = name
        self.lat = lat
        self.lan = lan
        self.country_code = country_code
        self.language = language
        self.label =label
        self.name_foreign = name_foreign
        
    
    