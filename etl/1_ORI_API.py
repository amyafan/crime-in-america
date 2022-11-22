"""
AF 10-2022

Getting the ORI information from the API 

inputs: 
______

    https://api.usa.gov/crime/fbi/sapi/api/agencies?api_key=<api_key>
    
    ~//data//source//nibrs_1991_2021_batch_header_dta//nibrs_batch_header_2021.dta"
    
    
outputs:
_______

    ~//data//processed//etl_3_ORI_information.csv
    
"""

##############
# SETTING UP #
##############

import pandas as pd
import requests

source = "..//data//source//"
processed = "..//data//processed//"

api_key = str(pd.read_csv("api_key.csv").columns[0])


# the URL we want 
URL = "https://api.usa.gov/crime/fbi/sapi/api/agencies?api_key=" + api_key


#######################
# MAKING THE API CALL #
#######################

a = requests.get(URL)

json = a.json()

records = pd.DataFrame([y for x in json.values() for y in x.values()])


######################
# MERGING IN BH INFO #
######################

bh_21_str = source + "nibrs_1991_2021_batch_header_dta//nibrs_batch_header_2021.dta"
bh_cols = ['ori', 'population', 'city_name','population_group']

bh = pd.read_stata(bh_21_str, columns = bh_cols)

final = pd.merge(records, bh, how = 'outer', on = 'ori')

########################
# WRITING OUT THE FILE #
########################

outfile_str = processed + "etl_3_ORI_information.csv"
final.to_csv(outfile_str)

print("we done!") 
