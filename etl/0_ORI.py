"""
AF 10-2022

Created a single dataset that includes information on how many months each ORIs reported each year 

inputs: 
______

    //data//source//nibrs_1991_2021_batch_header_dta//nibrs_batch_header_*.dta
    
        .dta files with information on how many months each agencies reported each year 
        

outputs: 
_______
    
    //data//processed//ori_months_reported.parquet

        dataset where each line is a unique ORI, and each column is a year that counts the # of months an ORI reported 

"""

##############
# SETTING UP #
##############

import pandas as pd 
import numpy as np

data_source = "..//data//source//"
data_export = "..//data//processed//"

bh_cols = ['ori', # ID
           'number_of_months_reported' # the actual value we want.
          ]


#################################
# READING IN ALL THE DATAFRAMES #
#################################

dflist =[]

for year in range(1991, 2022): 
    
    # location of the data
    bh_yr_str = data_source + "nibrs_1991_2021_batch_header_dta//nibrs_batch_header_" + str(year) + ".dta"
    
    # name of the dataset
    bh_yr = pd.read_stata(bh_yr_str, columns = bh_cols)
    
    # drop duplicates
    bh_yr.drop_duplicates(inplace = True)
    
    # set index
    bh_yr.set_index(['ori'], inplace = True)
    
    # rename columns 
    bh_yr.rename(columns = {'number_of_months_reported': str(year)}, inplace = True)
    
    # add this year's dataset to the list
    dflist.append(bh_yr)
    
    print(f"{year} is done!!!")
    
# concat all the years together    
ori_list = pd.concat(dflist, axis=1)

# clean up the data
final = ori_list.fillna(value=0).replace(["NN","NY"], 0).astype(int)

# figure out which year/ORI combinations are complete 
flags = final==12

# create a column for the number of full years 
final["full_years"] = flags.sum(axis =1)

# first year 
final['first'] = 9999

for year in range(1991, 2022): 
    
    final.loc[(final['first']>year) & (final[str(year)]==12), 'first'] = year
    
# number of consecutive years since 2021 (going backwards)
final['gaps'] = 2022 - (final['full_years'] + final['first']) 

final['gaps'] = final['gaps'].replace(-7977, -1)

#############
# EXPORTING #
#############

outfile_str = data_export + "etl_0_ori_months_reported.parquet"

final.to_parquet(outfile_str) 

print("ALL DONEEEEEE") 