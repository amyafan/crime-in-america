"""
AF 11-2022

plotting 

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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


source = "..//..//youth-crime//data//source//"
processed = "..//data//processed//"
manual = "..//..//youth-crime//data//manual//"

all_weapons = ['firearm', 'knife/cutting instrument (ice pick, screwdriver, ax, etc.)',
       'personal weapons (hands, feet, teeth, etc.)', 'other',
       'blunt object (club, hammer, etc.)', 'motor vehicle', 'unknown',
       'asphyxiation (by drowning, strangulation, suffocation, gas, etc.)',
       'drugs/narcotics/sleeping pills', 'explosives',
       'fire/incendiary device', 'poison (include gas)']
start_yr = 2019
end_yr = 2021

years = list(range(start_yr, end_yr + 1))
year_cols = pd.Series(years).apply(lambda x: str(x))

s = []

for year in years: 

    w_str = processed + "etl_0_weapons_" + str(year) + ".csv"
    
    w = pd.read_csv(w_str)
    w = w[w.population>50000]
    w['year'] = year
    
    s.append(w)

s_yrs = pd.concat(s, axis = 0)

################
# ALL ASSAULTS #
################

ori_str = processed + "1_assaults_weapons.pdf"
    
with PdfPages(ori_str) as pdf:

    assault_codes = ['aggravated assault', 'simple assault', 'intimidation']
    assaults = s_yrs[s_yrs.ucr_offense_code.isin(assault_codes)]

    a_counts = assaults.groupby(['year', 'ori'])['unique_incident_id'].count().reset_index()
    a_pivot = pd.pivot_table(a_counts, index = 'ori', values = 'unique_incident_id', columns ='year')

    a_outfile = processed + "1_all_assaults.csv" 
    a_pivot.to_csv(a_outfile) 
    
    # plot the aggregate changes 
    a_agg_c = np.log(a_pivot[years].sum()/a_pivot[years].sum()[2019])
    
    plt.figure(figsize = (6,6))
    plt.plot(years, np.log(a_pivot.divide(a_pivot[2019], axis=0)).T, color = "k", alpha = 0.02)
    plt.plot([2019, 2020], [a_agg_c[2019], a_agg_c[2020]], color = "red", linewidth=4)
    plt.plot([2020, 2021], [a_agg_c[2020], a_agg_c[2021]], color = "red", linewidth=4)
    
    plt.title("Percent change in total number of assaults")
    plt.ylim((-1, 1))
    plt.ylabel("log(percent change in # of assaults")
    plt.xlabel("Year")

    pdf.savefig(bbox_inches = "tight")  # saves the current figure into a pdf page
    plt.close()
    
    print("all assaults done") 

    #########################
    # ASSAULTS WITH WEAPONS #
    #########################

    assaults['w'] = (assaults[all_weapons].sum(axis=1) >= 1)

    aw = assaults[assaults.w]
    aw = assaults[assaults.ucr_offense_code=="aggravated assault"]

    aw_counts = aw.groupby(['year','ori'])['unique_incident_id'].count().reset_index()

    aw_pivot = pd.pivot_table(aw_counts, index = 'ori', values = 'unique_incident_id', columns ='year')

    aw_outfile = processed + "1_weapon_agg_assaults.csv" 
    aw_pivot.to_csv(aw_outfile) 
    
    aw_agg_c = np.log(aw_pivot[years].sum()/aw_pivot[years].sum()[2019])

    
    plt.figure(figsize = (6,6))
    plt.plot(years, np.log(aw_pivot.divide(aw_pivot[2019], axis=0)).T, color = "k", alpha = 0.02)
    plt.plot([2019, 2020], [aw_agg_c[2019], aw_agg_c[2020]], color = "red", linewidth=4)
    plt.plot([2020, 2021], [aw_agg_c[2020], aw_agg_c[2021]], color = "red", linewidth=4)
    
    plt.title("Percent change in total number aggravated assaults with a weapon")
    plt.ylim((-1, 1))
    plt.ylabel("log(percent change in # of assaults")
    plt.xlabel("Year")

    pdf.savefig(bbox_inches = "tight")  # saves the current figure into a pdf page
    plt.close()
    
    print("AA with weapons done")
    
    ##################################
    # ASSAULTS WITH SPECIFIC WEAPONS #
    ##################################
    
    for weapon in all_weapons: 
        
        weap_counts = aw.groupby(['year','ori'])[weapon].sum().reset_index()
        
        weap_pivot = pd.pivot_table(weap_counts, index = 'ori', values = weapon, columns ='year')

        weap_outfile = processed + "1_" + ''.join(e for e in weapon if e.isalnum()) + "_agg_assaults.csv" 
        weap_pivot.to_csv(weap_outfile) 
        
        weap_agg_c = np.log(weap_pivot[years].sum()/weap_pivot[years].sum()[2019])

        plt.figure(figsize = (6,6))
        plt.plot(years, np.log(weap_pivot.divide(weap_pivot[2019], axis=0)).T, color = "k", alpha = 0.02)
        
        plt.plot([2019, 2020], [weap_agg_c[2019], weap_agg_c[2020]], color = "red", linewidth=4)
        plt.plot([2020, 2021], [weap_agg_c[2020], weap_agg_c[2021]], color = "red", linewidth=4)
        
        plt.title(f"Percent change in aggravated assaults with {weapon}")
        plt.ylim((-1, 1))
        plt.ylabel("log(percent change in # of assaults")
        plt.xlabel("Year")

        pdf.savefig(bbox_inches = "tight")  # saves the current figure into a pdf page
        plt.close()
        
        print(f"Done with {weapon}")

        
 