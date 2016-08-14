import re
from langdetect import detect
from geotext35 import GeoText
import regen as ren
import reghu as rhu



example1 = "Seoul, South Korea to either Los Angeles or San Francisco,"
example2 = "Geneva, Switzerland to Indonesia for only €362 roundtrip with @TurkishAirlines"
example3 = "Seattle to Shanghai, China for only $528 roundtrip with @AirCanada"
example4 = "Non-stop from Reykjavík to Mauritius for only £315 roundtrip."
example5 = "Error fare: Bangkok, Thaiföld Berlinből 48.000 Ft-tól  http://bit.ly/1qqQNSb #repjegy #Bangkok #Utazás"
examplelist = (example1,example2,example3,example4,example5)



city_default ="DEFAULT"


class ExtractData(object):
    
    def __process_hu(self):
        
        #depart city with previous than without
        self.__saveDepartureCity( self.text, "HU", rhu.reg_depart_2_HU, rhu.reg_depart_1_HU)
                
        #arrival city with previous than without
        self.__saveArrivalCity( self.text, "HU", rhu.reg_arrival_2_HU, rhu.reg_arrival_1_HU)
        
        
        if self.dep_city == city_default or self.arr_city == city_default:
            #departure city is matched, looking further for arrival city
            if self.dep_city != city_default and self.arr_city == city_default:
            
                if self.dep_city_word == 1:
                    new_text = re.findall(rhu.reg_before_depart_1_HU, self.text)
                if self.dep_city_word == 2:
                    new_text = re.findall(rhu.reg_before_depart_2_HU, self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveArrivalCity( new_text_elem, "HU", rhu.reg_city_2_HU, rhu.reg_city_1_HU):
                        new_text = re.findall(rhu.reg_after_depart_1_HU, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveArrivalCity( new_text_elem, "HU", rhu.reg_city_2_HU, rhu.reg_city_1_HU)
                            
                            
    def __process_en(self):
        
        #depart city with previous than without
        self.__saveDepartureCity( self.text, "EN", ren.reg_depart_2_EN, ren.reg_depart_1_EN)
                
        #arrival city with previous than without
        self.__saveArrivalCity( self.text, "EN", ren.reg_arrival_2_EN, ren.reg_arrival_1_EN)
        
        if self.dep_city == city_default or self.arr_city == city_default:
            #departure city is matched, looking further for arrival city
            if self.dep_city != city_default and self.arr_city == city_default:
            
                if self.dep_city_word == 1:
                    new_text = re.findall(ren.reg_before_depart_1_EN, self.text)
                if self.dep_city_word == 2:
                    new_text = re.findall(ren.reg_before_depart_2_EN, self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveArrivalCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        if self.dep_city_word == 1:
                            new_text = re.findall(ren.reg_after_depart_1_EN, self.text)
                        if self.dep_city_word == 2:
                            new_text = re.findall(ren.reg_after_depart_2_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveArrivalCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
                            
            elif self.dep_city == city_default and self.arr_city != city_default:
                
                if self.arr_city_word == 1:
                    new_text = re.findall(ren.reg_before_arrival_1_EN, self.text)
                if self.arr_city_word == 2:
                    new_text = re.findall(ren.reg_before_arrival_2_EN, self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveDepartureCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        if self.arr_city_word == 1:
                            new_text = re.findall(ren.reg_after_arrival_1_EN, self.text)
                        if self.arr_city_word == 2:
                            new_text = re.findall(ren.reg_after_arrival_2_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveDepartureCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
              
            elif self.dep_city == city_default and self.arr_city == city_default:
                
                self.__saveDepartureCity( self.text, "EN", ren.reg_depart_2_EN, ren.reg_depart_before_to_1_EN)
                              
                            
        #----if country is still empty-------------  
        if self.dep_country == city_default or self.arr_country == city_default:
            #depart country with previous than without
            self.__saveDepartureCountry( self.text, "EN", ren.reg_depart_2_EN, ren.reg_depart_1_EN)
                
            #arrival country with previous than without
            self.__saveArrivalCountry( self.text, "EN", ren.reg_arrival_2_EN, ren.reg_arrival_1_EN)
            #departure country is matched, looking further for arrival country
            if self.dep_country != city_default and self.arr_country == city_default:
            
                #self.dep_country_word = self.__checkWordCount(self.dep_country,regex)
                self.dep_country_word = 1
                if self.dep_country_word == 1:
                    new_text = re.findall(ren.reg_before_depart_1_EN, self.text)
                if self.dep_country_word == 2:
                    new_text = re.findall(ren.reg_before_depart_2_EN, self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveArrivalCountry( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        new_text = re.findall(ren.reg_after_depart_1_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveArrivalCountry( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
                            
            if self.dep_country == city_default and self.arr_country != city_default:
                
                #self.arr_country_word = self.__checkWordCount(ren.arr_country,regex)
                self.arr_country_word = 1
                if self.arr_country_word == 1:
                    new_text = re.findall(ren.reg_before_arrival_1_EN, self.text)
                if self.arr_country_word == 2:
                    new_text = re.findall(ren.reg_before_arrival_2_EN, self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveDepartureCountry( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        new_text = re.findall(ren.reg_after_arrival_1_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveDepartureCountry( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
         #-----one more try
        if self.dep_city == city_default or self.arr_city == city_default:
            #departure city is matched, looking further for arrival city
            if self.dep_country != city_default and self.dep_city == city_default:
            
                if self.dep_country_word == 1:
                    new_text = re.findall(ren.cityFromCountry1En(self.dep_country), self.text)
                if self.dep_country_word == 2:
                    new_text = re.findall(ren.cityFromCountry2En(self.dep_country), self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveDepartureCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        new_text = re.findall(ren.reg_after_depart_1_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveDepartureCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
                            
            if self.arr_city == city_default and self.arr_country != city_default:
                
                if self.arr_country_word == 1:
                    new_text = re.findall(ren.cityFromCountry1En(self.arr_country), self.text)
                if self.arr_country_word == 2:
                    new_text = re.findall(ren.cityFromCountry2En(self.arr_country), self.text)
                    
                if len(new_text) > 0:
                    new_text_elem = new_text[0]
                    
                    if not self.__saveArrivalCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN):
                        new_text = re.findall(ren.reg_after_arrival_1_EN, self.text)
                        if len(new_text) > 0:
                            new_text_elem = new_text[0]
                            self.__saveArrivalCity( new_text_elem, "EN", ren.reg_city_2_EN, ren.reg_city_1_EN)
                                                   
                        
    def __saveArrivalCity(self, text, country, regular2, regular1):
        geo_result = GeoText(text, country, regular2)
        if len(geo_result.cities) > 0:
            self.arr_city_word = 2
            self.arr_city = geo_result.cities[0]
            self.arr_country_short = geo_result.country_short[0]
            self.arr_country = geo_result.country_from_short[0]
            return True
        else:
            geo_result = GeoText(text, country, regular1)
            if len(geo_result.cities) > 0:
                self.arr_city_word = 1
                self.arr_city = geo_result.cities[0]
                self.arr_country_short = geo_result.country_short[0]
                self.arr_country = geo_result.country_from_short[0]
                return True
            else:
                return False
            
    def __saveArrivalCountry(self, text, country, regular2, regular1):
        if self.arr_country == city_default:
            geo_result = GeoText(text, country, regular2)
            if len(geo_result.countries) > 0:
                self.arr_country_word = 2
                self.arr_country_short = geo_result.country_short[0]
                self.arr_country = geo_result.countries[0]
                return True
            else:
                geo_result = GeoText(text, country, regular1)
                if len(geo_result.countries) > 0:
                    self.arr_country_word = 1
                    self.arr_country_short = geo_result.country_short[0]
                    self.arr_country = geo_result.countries[0]
                    return True
                else:
                    return False
        else:
            return True
            
    def __saveDepartureCity(self, text, country, regular2, regular1):
        geo_result = GeoText(text, country, regular2)
        if len(geo_result.cities) > 0:
            self.dep_city_word = 2
            self.dep_city = geo_result.cities[0]
            self.dep_country_short = geo_result.country_short[0]
            self.dep_country = geo_result.country_from_short[0]
            return True
        else:
            geo_result = GeoText(text, country, regular1)
            if len(geo_result.cities) > 0:
                self.dep_city_word = 1
                self.dep_city = geo_result.cities[0]
                self.dep_country_short = geo_result.country_short[0]
                self.dep_country = geo_result.country_from_short[0]
                return True
            else:
                return False
            
    def __saveDepartureCountry(self, text, country, regular2, regular1):
        if self.dep_country == city_default:
            geo_result = GeoText(text, country, regular2)
            if len(geo_result.countries) > 0:
                self.dep_country_word = 2
                self.dep_country_short = geo_result.country_short[0]
                self.dep_country = geo_result.countries[0]
                return True
            else:
                geo_result = GeoText(text, country, regular1)
                if len(geo_result.countries) > 0:
                    self.dep_country_word = 1
                    self.dep_country_short = geo_result.country_short[0]
                    self.arr_country = geo_result.countries[0]
                    return True
                else:
                    return False
        else:
                return False
        
    def __process(self):
        self.text = self.text.replace("*","")
        self.text = self.text.replace("(","")
        self.text = self.text.replace(")","")
        result = re.findall(self.text, rhu.reg_is_HU_accent)
        if len(result) > 0:
            self.__process_hu()
            self.language ="hu"
        else:
            self.language = detect(self.text)
            if self.language == "en":
                self.__process_en()
            elif self.language == "hu":
                    self.__process_hu()
            else:
                print('other language: '+ self.language )
            
    def __checknull(self,txt):
        empty = " - "
        if txt is not None and len(txt)>0 :
            return txt
        else:
            return empty
        
    def __checkWordCount(self,txt, regex):
        result = re.findall(regex, txt)
        return result
            
    def printInfos(self):
        print(self.text)
        print('  depCity:    ' + self.__checknull(self.dep_city) )
        print('  depCountry: ' + self.__checknull(self.dep_country))
        print('  depCountry: ' + self.__checknull(self.dep_country_short))
        print('  arrCity:    ' + self.__checknull(self.arr_city) )
        print('  arrCountry: ' + self.__checknull(self.arr_country) )
        print('  arrCountry: ' + self.__checknull(self.arr_country_short) )
        print('  language:   ' + self.__checknull(self.language) )
              
    
        
    def __init__(self, text):
        self.text = text
        self.dep_city = city_default
        self.dep_country = city_default
        self.dep_country_short = city_default
        self.arr_city = city_default
        self.arr_country = city_default
        self.arr_country_short = city_default
        self.language=city_default
        self.__process()


if __name__ == '__main__':
    for elem in examplelist:
        extract = ExtractData(elem)
        extract.printInfos()



