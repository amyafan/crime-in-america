"""
AF 11-2022

Cleaning the offense table so that it's easier to look at weapons 

inputs: 
______

    ..//data//source//nibrs_1991_2021_offense_segment_dta//nibrs_offense_segment_{year}.dta
    
        .dta files with information on how many months each agencies reported each year 
        
    ..//data//source//nibrs_1991_2021_batch_header_dta//nibrs_batch_header_2021.dta"
        

outputs: 
_______
    
    ..//data//processed//etl_0_weapons_{year}.parquet

        Cleaned data for that year and ORI 

"""

##############
# SETTING UP #
##############

import pandas as pd 
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

source = "..//data//source//"
yc_processed = "..//..//youth-crime//data//processed//"
processed = "..//data//processed//"

start_yr = 2019
end_yr = 2021

years = list(range(start_yr, end_yr + 1))
year_cols = pd.Series(years).apply(lambda x: str(x))


#######################
# IMPORTANT FUNCTIONS #
#######################

firearms = ['handgun', 'firearm (type not stated)', 'rifle', 'shotgun', 'other firearm']

def make_weapon_flag(offense_table, weapon):
    
    column = (offense_table.type_weapon_force_involved_1 == weapon)
    column[offense_table.type_weapon_force_involved_2 == weapon] = True
    column[offense_table.type_weapon_force_involved_3 == weapon] = True
    
    return column

def clean_offenses_weapons(year):
    
    offense_cols = ['ori', 'ucr_offense_code'
                , 'type_weapon_force_involved_1', 'automatic_weapon_indicator_1'
                , 'type_weapon_force_involved_2', 'automatic_weapon_indicator_2'
                , 'type_weapon_force_involved_3', 'automatic_weapon_indicator_3'
                , 'location_type'
                , 'unique_incident_id']
    
    offense_yr_str = yc_source + "nibrs_1991_2021_offense_segment_dta//nibrs_offense_segment_" + str(year) + ".dta"
    offense_yr = pd.read_stata(offense_yr_str, columns = offense_cols)    
    
    offense_yr_oris = offense_yr[offense_yr.ori.isin(our_oris)]
    
    all_weapons = offense_yr_oris.type_weapon_force_involved_1.unique()
    
    for weapon in all_weapons: 
        
        print(weapon)
        
        offense_yr_oris[weapon] = False
        offense_yr_oris.loc[offense_yr_oris.type_weapon_force_involved_1 == weapon, weapon] = True
        offense_yr_oris.loc[offense_yr_oris.type_weapon_force_involved_2 == weapon, weapon] = True        
        offense_yr_oris.loc[offense_yr_oris.type_weapon_force_involved_3 == weapon, weapon] = True
    
    offense_yr_oris['firearm'] = (offense_yr_oris[firearms].sum(axis=1) >= 1)
    
    print(offense_yr_oris.head())
    
    return offense_yr_oris

####################
# PICKING AGENCIES #
####################

ori_str = yc_processed + "etl_0_ori_months_reported.parquet"
ori = pd.read_parquet(ori_str, columns = list(year_cols))

# this is a bad way to loop but whatever 

for year in years: 
    
    ori = ori[ori[str(year)]==12]
    
our_oris = ori.index

ori_cols = ['ori', 'agency_name', 'agency_type_name', 'state_name', 'state_abbr', 'population', 'city_name', 'population_group']

ori_info_str = yc_processed + "etl_3_ORI_information.csv"
ori_info = pd.read_csv(ori_info_str)

ori_pop = ori_info[ori_info.population>50000]
oris = ori_pop[ori_pop.ori.isin(our_oris)]

print(len(oris))
                
#############################
# DOING THE ACTUAL CLEANING #
#############################
                
for year in range(start_yr, end_yr+1): 
    
    off_year = clean_offenses_weapons(year)
                
    final = pd.merge(oris, off_year, how = 'right', on = 'ori')
    
    outfile_str = processed + "weapons_" + str(year) + ".csv"
    final.to_csv(outfile_str)
    
    print(f"done with {year}")
    


