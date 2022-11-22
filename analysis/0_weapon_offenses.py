"""
AF 11-2022

Counting offenses by weapons 

inputs: 
______

    processed//weapons_{year}.csv
    
    source//nibrs_1991_2021_batch_header_dta//nibrs_batch_header_{year}.dta


outputs: 
_______

   processed//0_weapons_offenses_with_population.csv


"""


import pandas as pd 
import numpy as np

source = "..//..//youth-crime//data//source//"
processed = "..//data//processed//"
manual = "..//..//youth-crime//data//manual//"

# weapons but grouping all firearms together
all_weapons = ['knife/cutting instrument (ice pick, screwdriver, ax, etc.)',
       'personal weapons (hands, feet, teeth, etc.)', 'other', 'none',
       'blunt object (club, hammer, etc.)', 'motor vehicle', 'unknown',
       'asphyxiation (by drowning, strangulation, suffocation, gas, etc.)',
       'drugs/narcotics/sleeping pills', 'explosives',
       'fire/incendiary device', 'poison (include gas)', 
       'firearm']

start_yr = 2019
end_yr = 2021

years = list(range(start_yr, end_yr + 1))
year_cols = pd.Series(years).apply(lambda x: str(x))

y = []

for year in years: 

    w_str = processed + "weapons_" + str(year) + ".csv"
    
    w = pd.read_csv(w_str)
    w['year'] = year
    
    y.append(w)
    
yrs = pd.concat(y, axis = 0)


final = yrs.groupby(['year', 'ori', 'agency_name', 'state_name', 'population', 'city_name', 'ucr_offense_code'])[all_weapons].sum()

final = final.melt(ignore_index = False).reset_index()

fin = pd.pivot_table(final, columns = 'year', 
                     index = ['ori', 'agency_name', 'state_name', 'population', 'city_name', 'ucr_offense_code', 'variable'], 
                     values = 'value', 
                     aggfunc= 'sum')

pop_cols = ['ori', 'population']
pop_list = []

for year in years: 
    
    bh_str = source + "nibrs_1991_2021_batch_header_dta//nibrs_batch_header_" + str(year) + ".dta"

    bh = pd.read_stata(bh_str, columns = pop_cols)
    bhs = bh[bh.ori.isin(yrs.ori.unique())].set_index('ori')
    
    pop_list.append(bhs)

pops = pd.concat(pop_list, axis=1)
pops.columns = year_cols + "_pop"

nonzero = fin[fin[2021]!=0]

last = pd.merge(nonzero.reset_index(), pops.reset_index(), on = 'ori')

outfile_str = processed + "0_weapons_offenses_with_population.csv"

last.sort_values('ucr_offense_code').to_csv(outfile_str)