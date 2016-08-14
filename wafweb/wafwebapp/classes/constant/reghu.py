reg_is_HU_accent = r"([áéíóőúűÁÉÍÓŐÚŰ])" 
reg_is_DE_accent = r"([ÄäöÖüÜß])" 
#
#General city
reg_city_1_HU = r"([A-ZÓÜÖÚŐŰÁÉÍ]+[a-zóüöőúűéá]*)"
reg_city_2_HU = r"([A-ZÓÜÖÚŐŰÁÉÍ]+[a-zóüöőúűéá]*(?:[ '-][A-ZÓÜÖÚŐŰÁÉÍ]+[a-zóüöőúűéá]*)*)"
#
#Depart city
reg_depart_1_HU = r"([A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+)(?=(?i)ból|ről|ról|ből)"
reg_depart_2_HU = r"([A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[ |-][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+)(?=(?i)ból|ről|ról|ből)"
#
#Arrival city
reg_arrival_1_HU = r"([A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+)(?=(?i)ba|be|ra|re)"
reg_arrival_2_HU = r"([A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[ |-][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+)(?=(?i)ba|be|ra|re)"

# Everything before Depart
reg_before_depart_1_HU = r"(.+)[ ][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+(?=(?i)ból|ről|ról|ből)"
reg_before_depart_2_HU = r"(.+)[ ][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[ |-][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+(?=(?i)ból|ről|ról|ből)"
#
# Everything before Arrival
reg_before_arrival_1_HU = r"(.+)[ ][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+(?=(?i)ba|be|ra|re)"
reg_before_arrival_2_HU = r"(.+)[ ][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[ |-][A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+(?=(?i)ba|be|ra|re)"

# Everything after Depart
reg_after_depart_1_HU = r"[A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[(?i)ból|ről|ról|ből)][ ](.+)"

# Everything after Arrival
reg_after_arrival_1_HU = r"[A-ZÓÜÖÚŐŰÁÉÍa-zóüöőúűéá]+[(?i)ba|be|ra|re)][ ](.+)"