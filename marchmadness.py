''' 
Jake Wallack
Predicting NCAA Tourney Results
'''

import pandas as pd
import csv
from kenpompy.utils import login

# Returns an authenticated browser that can then be used to scrape pages that require authorization.
browser = login("jwall5678@outlook.com", "5253Jake1601#1!")

import kenpompy.summary as kp
import kenpompy.misc

# Returns a pandas dataframe containing the efficiency and tempo stats for the current season (https://kenpom.com/summary.php).

years = ["2016", "2017", "2018", "2019"]

data_dict = {}


for year in years:
    gen_stats = kenpompy.misc.get_pomeroy_ratings(browser, season = year)
    eff_stats = kp.get_efficiency(browser, season = year)
    four_factors = kp.get_fourfactors(browser, season = year)
    roster_stats = kp.get_height(browser, season = year)
    misc_stats = kp.get_teamstats(browser, season = year)
    stats = [gen_stats, eff_stats, four_factors, roster_stats, misc_stats]
    data_dict[year] = stats
    

gen = 0    
eff = 1
fac = 2
ros = 3
misc = 4


mm_data = pd.read_csv("Big_Dance_CSV.csv")
mm_16 = mm_data.loc[mm_data["Year"] == 2016]
mm_17 = mm_data.loc[mm_data["Year"] == 2017]
mm_18 = mm_data.loc[mm_data["Year"] == 2018]
mm_19 = mm_data.loc[mm_data["Year"] == 2019]




