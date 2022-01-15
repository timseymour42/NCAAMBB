''' 
Jake Wallack
Predicting NCAA Tourney Results
'''

import pandas as pd
import csv
from kenpompy.utils import login
import kenpompy.summary as kp
import kenpompy.misc
import string


# Returns an authenticated browser that can then be used to scrape pages that require authorization.
browser = login("jwall5678@outlook.com", "NCAAProject1")

# we will be using the '15-16 through 18'-19' for our initial research
years = ["2016", "2017", "2018", "2019"]
data_dict = {}

def get_gen_missing(browser, season=None):
    '''
    Collects the general statistic for a given year and removes seeding from team names
    '''
    url = 'https://kenpom.com/index.php'
    if season and int(season) < 2002:
        raise ValueError("season cannot be less than 2002")
    url += '?y={}'.format(season)
    browser.open(url)
    page = browser.get_current_page()
    table = page.find_all('table')[0]
    ratings_df = pd.read_html(str(table))
    # Dataframe tidying.
    ratings_df = ratings_df[0]
    ratings_df.columns = ratings_df.columns.map(lambda x: x[1])
    ratings_df.dropna(inplace = True)
    ratings_df['Team'] = ratings_df['Team'].apply(strip_seed)
    ratings_df = ratings_df[ratings_df.Team != 'Team']
    return ratings_df

def strip_seed(name):
    '''
    Taking the seed out of team names
    '''
    if name[-1] in string.digits:
        return name.rstrip(string.digits)[:-1]
    else: 
        return name
    

# for loop to read in various kenpom statistics (tables) and put them together in a list for each year
for year in years:
    gen_stats = get_gen_missing(browser, season=year)
    eff_stats = kp.get_efficiency(browser, season = year)
    four_factors = kp.get_fourfactors(browser, season = year)
    roster_stats = kp.get_height(browser, season = year)
    misc_stats = kp.get_teamstats(browser, season = year)
    stats = [gen_stats, eff_stats, four_factors, roster_stats, misc_stats]
    data_dict[year] = stats
    
# indices s for stat tables
gen = 0    
eff = 1
fac = 2
ros = 3
misc = 4

# reading in march tournament data
mm_data = pd.read_csv("Big_Dance_CSV.csv")
mm_16 = mm_data.loc[mm_data["Year"] == 2016]
mm_17 = mm_data.loc[mm_data["Year"] == 2017]
mm_18 = mm_data.loc[mm_data["Year"] == 2018]
mm_19 = mm_data.loc[mm_data["Year"] == 2019]


final_df = pd.DataFrame()
for year in data_dict.keys():
    # contains the general dataset for the year
    temp_df = data_dict[year][0]
    # becomes false when the general stats df is iterated past
    first_df = True
    for df in data_dict[year]:
        if (first_df):
            first_df = False
        else:
            temp_df = temp_df.merge(df, left_on = 'Team', right_on = 'Team', how = 'inner')
    temp_df['Year'] = year
    final_df = final_df.append(temp_df)


teams = []
for team in gen_stats['Team'].values.tolist():
    if (team in temp_df['Team'].values.tolist()):
        teams.append(team)
df[~df['A'].isin([3, 6])]

four_factors.loc[~four_factors['Team'].isin(teams)]







        






