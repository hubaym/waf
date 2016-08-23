#----English---------
#General city 1-2 word:
reg_city_1_EN = r"([A-Z]+[a-z]*)"
reg_city_2_EN = r"([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)"
#
#Departure city word:
reg_depart_1_EN = r"[Ff]rom[ ][the ]*([A-Z]+[a-z]*)"
reg_depart_2_EN = r"[Ff]rom[ ][the ]*([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)"

reg_depart_before_to_1_EN = r"([A-Z]*[a-z]*)[, ]*([A-Z]+[a-z]*)[ ][Tt]o"
reg_depart_before_to_2_EN = r"([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)[, ]*([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)[ ][Tt]o"



#Arrival city word
reg_arrival_1_EN = r"[Tt]o[ ][the ]*([A-Z]+[a-z]*)"
reg_arrival_2_EN = r"[Tt]o[ ][the ]*([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)"
#
# Everything before Depart
reg_before_depart_1_EN = r"(.+)[ ][Ff]rom[ ][the ]*[A-Z]+[a-z]*"
reg_before_depart_2_EN = r"(.+)[ ][Ff]rom[ ][the ]*[A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*"
# Everything before Arrival
reg_before_arrival_1_EN = r"(.+)[ ][Tt]o[ ][the ]*[A-Z]+[a-z]*"
reg_before_arrival_2_EN = r"(.+)[ ][Tt]o[ ][the ]*[A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*"
#
# Everything after Depart
reg_after_depart_1_EN = r"[Ff]rom[ ][the ]*[A-Z]+[a-z]*[ ](.+)"
reg_after_depart_2_EN = r"[Ff]rom[ ][the ]*[A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*[ ,](.+)"

# Everything after Arrival
reg_after_arrival_1_EN = r"[Tt]o[ ][the ]*[A-Z]+[a-z]*[ ](.+)"
reg_after_arrival_2_EN = r"[Tt]o[ ][the ]*[A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*[ ,](.+)"


#country to city 
reg_cityfromcountry_1_EN= r"([A-Z]+[a-z]*)(?:[, ]+"
reg_cityfromcountry_2_EN= r"([A-Z]+[a-z]*(?:[ '-][A-Z]+[a-z]*)*)(?:[, ]+"

def cityFromCountry1En(country):
    return reg_cityfromcountry_1_EN + country + ")"
def cityFromCountry2En(country):
    return reg_cityfromcountry_2_EN + country + ")"

