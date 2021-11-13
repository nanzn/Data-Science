''' late_finishers=df(~df.index.isin(early_finishers.index))
early_finisher=df[pd.to_datetime(df['assignment1_submission']) < '2018']

import scipy as sp
from scipy.stats import ttest_ind
ttest_ind(early_finisher['a'], late_finisher['b'])
ttest_ind()
'''

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("1-Intro/assets/nhl.csv")
cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

def nhl_correlation(): 
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NFL', 'MLB', 'NBA'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['NHL'] = cities['NHL'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['NHL'].replace('—', np.NaN, inplace=True)
    cities['NHL'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)

    nhl_df=pd.read_csv("1-Intro/assets/nhl.csv")
    # Data Cleaning: nhl_df
    # Keep only year = 2018 data
    nhl_df = nhl_df[nhl_df['year']==2018]
    # Drop Division Labels
    nhl_df.drop([0,9,18,26], axis='rows', inplace=True)
    # Remove '*' from team
    nhl_df['team'] = nhl_df['team'].str.replace('*', '', regex=True)
    # Drop columns not needed
    nhl_df.drop(['GP', 'OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS', 'RPt%', 'ROW', 'year', 'League'], axis='columns', inplace=True)
    nhl_df.reset_index(inplace=True, drop=True)
    # Create column for Metropolitan area
    nhl_df['Metropolitan area'] = nhl_df['team'].map({'Tampa Bay Lightning':'Tampa Bay Area',
     'Boston Bruins':'Boston',
     'Toronto Maple Leafs':'Toronto',
     'Florida Panthers':'Miami–Fort Lauderdale',
     'Detroit Red Wings':'Detroit',
     'Montreal Canadiens':'Montreal',
     'Ottawa Senators':'Ottawa',
     'Buffalo Sabres':'Buffalo',
     'Washington Capitals':'Washington, D.C.',
     'Pittsburgh Penguins':'Pittsburgh',
     'Philadelphia Flyers':'Philadelphia',
     'Columbus Blue Jackets':'Columbus',
     'New Jersey Devils':'New York City',
     'Carolina Hurricanes':'Raleigh',
     'New York Islanders':'New York City',
     'New York Rangers':'New York City',
     'Nashville Predators':'Nashville',
     'Winnipeg Jets':'Winnipeg',
     'Minnesota Wild':'Minneapolis–Saint Paul',
     'Colorado Avalanche':'Denver',
     'St. Louis Blues':'St. Louis',
     'Dallas Stars':'Dallas–Fort Worth',
     'Chicago Blackhawks':'Chicago',
     'Vegas Golden Knights':'Las Vegas',
     'Anaheim Ducks':'Los Angeles',
     'San Jose Sharks':'San Francisco Bay Area',
     'Los Angeles Kings':'Los Angeles',
     'Calgary Flames':'Calgary',
     'Edmonton Oilers':'Edmonton',
     'Vancouver Canucks':'Vancouver',
     'Arizona Coyotes':'Phoenix'})
    # Columns 'W' and 'L' as type int
    nhl_df['W'] = pd.to_numeric(nhl_df['W'])
    nhl_df['L'] = pd.to_numeric(nhl_df['L'])

    # Merge cities + nhl_df
    df = nhl_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')

    # Calculate Win/Loss Ratio
    df['W/L'] = df['W']/(df['L']+df['W'])

    # Group by Metropolitan area
    df = df.groupby('Metropolitan area').mean().reset_index(drop=True)

    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def nba_correlation():
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NFL', 'MLB', 'NHL'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['NBA'] = cities['NBA'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['NBA'].replace('—', np.NaN, inplace=True)
    cities['NBA'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)
    
    nba_df=pd.read_csv("1-Intro/assets/nba.csv")
    # Data Cleaning: nba_df
    # Keep only year = 2018 data
    nba_df = nba_df[nba_df['year']==2018]
    # Remove '* ([0-9]+)' from team
    nba_df['team'] = nba_df['team'].str.replace('(\()([0-9]+)(\))', '', regex=True)
    nba_df['team'] = nba_df['team'].str.replace('*', '', regex=True)
    nba_df['team'] = nba_df['team'].str.strip()
    # Drop columns not needed
    nba_df.drop(['W', 'L','GB', 'PS/G', 'PA/G', 'SRS', 'year', 'League'], axis='columns', inplace=True)
    nhl_df.reset_index(inplace=True, drop=True)
    # Create column for Metropolitan area
    nba_df['Metropolitan area'] = nba_df['team'].map({'Toronto Raptors':'Toronto',
     'Boston Celtics':'Boston',
     'Philadelphia 76ers':'Philadelphia',
     'Cleveland Cavaliers':'Cleveland',
     'Indiana Pacers':'Indianapolis',
     'Miami Heat':'Miami–Fort Lauderdale',
     'Milwaukee Bucks':'Milwaukee',
     'Washington Wizards':'Washington, D.C.',
     'Detroit Pistons':'Detroit',
     'Charlotte Hornets':'Charlotte',
     'New York Knicks':'New York City',
     'Brooklyn Nets':'New York City',
     'Chicago Bulls':'Chicago',
     'Orlando Magic':'Orlando',
     'Atlanta Hawks':'Atlanta',
     'Houston Rockets':'Houston',
     'Golden State Warriors':'San Francisco Bay Area',
     'Portland Trail Blazers':'Portland',
     'Oklahoma City Thunder':'Oklahoma City',
     'Utah Jazz':'Salt Lake City',
     'New Orleans Pelicans':'New Orleans',
     'San Antonio Spurs':'San Antonio',
     'Minnesota Timberwolves':'Minneapolis–Saint Paul',
     'Denver Nuggets':'Denver',
     'Los Angeles Clippers':'Los Angeles',
     'Los Angeles Lakers':'Los Angeles',
     'Sacramento Kings':'Sacramento',
     'Dallas Mavericks':'Dallas–Fort Worth',
     'Memphis Grizzlies':'Memphis',
     'Phoenix Suns':'Phoenix'})
    # Columns 'W/L%' as type int
    nba_df['W/L%'] = pd.to_numeric(nba_df['W/L%'])

    df = nba_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=True)
    
    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W/L%'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

nba_correlation()