# crime-in-america

Code and analysis for "Felony Assaults With Guns Increasing In Hundreds of U.S. Communities" story published [here](newsy.com/stories/felony-gun-assaults-increasing-in-hundreds-of-communities/)

*Created by Amy Fan (<amy.a.fan@gmail.com>)*

*Reporter: Amy Fan (<amy.a.fan@gmail.com>)*

## Project goal

Looking at assaults, weapons, and firearms in the NIBRS data across agencies across the US. 

## Project notes

### Staff involved

Amy Fan, Data Reporter

Rosie Cima, Data Reporter

### Data sources

[Jacob Kaplan's Concatenated Files: National Incident-Based Reporting System (NIBRS) Data 1991-2021](https://jacobdkaplan.com/data.html)
* The data is released under a ODC Open Database License (ODbL)
* Jacob Kaplan's [NIBRS book online](nibrsbook.com/) served as a valuable reference guide as I navigated through the data. 

[FBI API](https://crime-data-explorer.fr.cloud.gov/pages/docApi) to get additional information on each agency (for instance, agency names)

## Technical

* Run the files in the etl folder in order to extract the data
* Analyses and intermediate datasets for data visualizations are in the analysis folder
* analysis/notebooks contains additional notes

## Data notes

* only agencies reporting 12 month of NIBRS data between 2019 - 2021 and with a population of more tha 50,000 were included in these analyses
* "personal weapons" were not counted as weapons
