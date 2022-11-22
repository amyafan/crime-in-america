"""
AF 11-2022

Cleaning the offense table so that it's easier to look at weapons for the local stations

inputs: 
______

    ..//data//source//nibrs_1991_2021_offense_segment_dta//nibrs_offense_segment_{year}.dta
    
        .dta files with information on how many months each agencies reported each year 
        
    ..//data//manual//local_stations.csv
        
        information on the local stations
        

outputs: 
_______
    
    ..//data//processed//etl_3_local_weapons_{year}.parquet

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
manual = "..//data//manual//"
yc_source = "..//..//youth-crime//data//source//"
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

local_str = manual + "local_stations.csv"
local = pd.read_csv(local_str) 

our_oris = local.ori

                
#############################
# DOING THE ACTUAL CLEANING #
#############################
                
for year in range(start_yr, end_yr+1): 
    
    off_year = clean_offenses_weapons(year)
                
    final = pd.merge(local, off_year, how = 'right', on = 'ori')
    
    outfile_str = processed + "etl_3_local_weapons_" + str(year) + ".csv"
    final.to_csv(outfile_str)
    
    print(f"done with {year}")
    


