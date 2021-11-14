''' late_finishers=df(~df.index.isin(early_finishers.index))
early_finisher=df[pd.to_datetime(df['assignment1_submission']) < '2018']

import scipy as sp
from scipy.stats import ttest_ind
ttest_ind(early_finisher['a'], late_finisher['b'])
ttest_ind()
'''

import pandas as pd
import numpy as np
from pandas.core.tools.numeric import to_numeric
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
    nba_df.reset_index(inplace=True, drop=True)
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

def mlb_correlation(): 
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NFL', 'NBA', 'NHL'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['MLB'] = cities['MLB'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['MLB'].replace('—', np.NaN, inplace=True)
    cities['MLB'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)

    mlb_df=pd.read_csv("1-Intro/assets/mlb.csv")
    # Data Cleaning: mlb_df
    # Keep only year = 2018 data
    mlb_df = mlb_df[mlb_df['year']==2018]
    # Drop columns not needed
    mlb_df.drop(['W', 'L','GB', 'year', 'League'], axis='columns', inplace=True)
    mlb_df.reset_index(inplace=True, drop=True)
    # Create column for Metropolitan area
    mlb_df['Metropolitan area'] = mlb_df['team'].map({'Boston Red Sox':'Boston',
     'New York Yankees':'New York City',
     'Tampa Bay Rays':'Tampa Bay Area',
     'Toronto Blue Jays':'Toronto',
     'Baltimore Orioles':'Baltimore',
     'Cleveland Indians':'Cleveland',
     'Minnesota Twins':'Minneapolis–Saint Paul',
     'Detroit Tigers':'Detroit',
     'Chicago White Sox':'Chicago',
     'Kansas City Royals':'Kansas City',
     'Houston Astros':'Houston',
     'Oakland Athletics':'San Francisco Bay Area',
     'Seattle Mariners':'Seattle',
     'Los Angeles Angels':'Los Angeles',
     'Texas Rangers':'Dallas–Fort Worth',
     'Atlanta Braves':'Atlanta',
     'Washington Nationals':'Washington, D.C.',
     'Philadelphia Phillies':'Philadelphia',
     'New York Mets':'New York City',
     'Miami Marlins':'Miami–Fort Lauderdale',
     'Milwaukee Brewers':'Milwaukee',
     'Chicago Cubs':'Chicago',
     'St. Louis Cardinals':'St. Louis',
     'Pittsburgh Pirates':'Pittsburgh',
     'Cincinnati Reds':'Cincinnati',
     'Los Angeles Dodgers':'Los Angeles',
     'Colorado Rockies':'Denver',
     'Arizona Diamondbacks':'Phoenix',
     'San Francisco Giants':'San Francisco Bay Area',
     'San Diego Padres':'San Diego'})
    # Columns 'W/L%' as type int
    mlb_df['W-L%'] = pd.to_numeric(mlb_df['W-L%'])

    # Merge and Group
    df = mlb_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=True)
    
    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W-L%'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def nfl_correlation(): 
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NHL', 'NBA', 'MLB'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['NFL'] = cities['NFL'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['NFL'] = cities['NFL'].str.strip()
    cities['NFL'].replace('—', np.NaN, inplace=True)
    cities['NFL'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)

    nfl_df=pd.read_csv("1-Intro/assets/nfl.csv")
    # Data Cleaning: mlb_df
    # Keep only year = 2018 data
    nfl_df = nfl_df[nfl_df['year']==2018]
    # Drop subheaders
    nfl_df.drop(range(0, 40, 5), axis='rows', inplace=True)
    # Drop irrelevant columns
    nfl_df.drop(['DSRS', 'L', 'League', 'MoV', 'OSRS', 'PA', 'PD', 'PF', 'SRS', 'SoS', 'T', 'W', 'year'], axis='columns', inplace=True)
    # Remove '*' and '+' from team
    nfl_df['team'] = nfl_df['team'].str.replace('\*|\+', '', regex=True)
    # Create column for Metropolitan area
    nfl_df['Metropolitan area'] = nfl_df['team'].map({'New England Patriots':'Boston',
     'Miami Dolphins':'Miami–Fort Lauderdale',
     'Buffalo Bills':'Buffalo',
     'New York Jets':'New York City',
     'Baltimore Ravens':'Baltimore',
     'Pittsburgh Steelers':'Pittsburgh',
     'Cleveland Browns':'Cleveland',
     'Cincinnati Bengals':'Cincinnati',
     'Houston Texans':'Houston',
     'Indianapolis Colts':'Indianapolis',
     'Tennessee Titans':'Nashville',
     'Jacksonville Jaguars':'Jacksonville',
     'Kansas City Chiefs':'Kansas City',
     'Los Angeles Chargers':'Los Angeles',
     'Denver Broncos':'Denver',
     'Oakland Raiders':'San Francisco Bay Area',
     'Dallas Cowboys':'Dallas–Fort Worth',
     'Philadelphia Eagles':'Philadelphia',
     'Washington Redskins':'Washington, D.C.',
     'New York Giants':'New York City',
     'Chicago Bears':'Chicago',
     'Minnesota Vikings':'Minneapolis–Saint Paul',
     'Green Bay Packers':'Green Bay',
     'Detroit Lions':'Detroit',
     'New Orleans Saints':'New Orleans',
     'Carolina Panthers':'Charlotte',
     'Atlanta Falcons':'Atlanta',
     'Tampa Bay Buccaneers':'Tampa Bay Area',
     'Los Angeles Rams':'Los Angeles',
     'Seattle Seahawks':'Seattle',
     'San Francisco 49ers':'San Francisco Bay Area',
     'Arizona Cardinals':'Phoenix'}) 
    # Convert W-L% to numeric
    nfl_df['W-L%'] = to_numeric(nfl_df['W-L%'])
    nfl_df.reset_index(inplace=True, drop=True)
    
    # Merge and Group
    df = nfl_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=True)
 
    population_by_region = df['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = df['W-L%'] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

def nhl(): 
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
    df.drop(['W', 'L'], axis='columns', inplace=True)
    # Group by Metropolitan area
    df = df.groupby('Metropolitan area').mean().reset_index(drop=False)
    df.drop(['Population'], axis='columns', inplace=True)
    return df

def nba():
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
    nba_df.reset_index(inplace=True, drop=True)
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
    nba_df['W/L'] = pd.to_numeric(nba_df['W/L%'])
    nba_df.drop(['W/L%'], axis='columns', inplace=True)

    df = nba_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=False)
    df.drop(['Population'], axis='columns', inplace=True)
    return df

def mlb(): 
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NFL', 'NBA', 'NHL'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['MLB'] = cities['MLB'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['MLB'].replace('—', np.NaN, inplace=True)
    cities['MLB'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)

    mlb_df=pd.read_csv("1-Intro/assets/mlb.csv")
    # Data Cleaning: mlb_df
    # Keep only year = 2018 data
    mlb_df = mlb_df[mlb_df['year']==2018]
    # Drop columns not needed
    mlb_df.drop(['W', 'L','GB', 'year', 'League'], axis='columns', inplace=True)
    mlb_df.reset_index(inplace=True, drop=True)
    # Create column for Metropolitan area
    mlb_df['Metropolitan area'] = mlb_df['team'].map({'Boston Red Sox':'Boston',
     'New York Yankees':'New York City',
     'Tampa Bay Rays':'Tampa Bay Area',
     'Toronto Blue Jays':'Toronto',
     'Baltimore Orioles':'Baltimore',
     'Cleveland Indians':'Cleveland',
     'Minnesota Twins':'Minneapolis–Saint Paul',
     'Detroit Tigers':'Detroit',
     'Chicago White Sox':'Chicago',
     'Kansas City Royals':'Kansas City',
     'Houston Astros':'Houston',
     'Oakland Athletics':'San Francisco Bay Area',
     'Seattle Mariners':'Seattle',
     'Los Angeles Angels':'Los Angeles',
     'Texas Rangers':'Dallas–Fort Worth',
     'Atlanta Braves':'Atlanta',
     'Washington Nationals':'Washington, D.C.',
     'Philadelphia Phillies':'Philadelphia',
     'New York Mets':'New York City',
     'Miami Marlins':'Miami–Fort Lauderdale',
     'Milwaukee Brewers':'Milwaukee',
     'Chicago Cubs':'Chicago',
     'St. Louis Cardinals':'St. Louis',
     'Pittsburgh Pirates':'Pittsburgh',
     'Cincinnati Reds':'Cincinnati',
     'Los Angeles Dodgers':'Los Angeles',
     'Colorado Rockies':'Denver',
     'Arizona Diamondbacks':'Phoenix',
     'San Francisco Giants':'San Francisco Bay Area',
     'San Diego Padres':'San Diego'})
    # Columns 'W/L%' as type int
    mlb_df['W/L'] = pd.to_numeric(mlb_df['W-L%'])
    mlb_df.drop(['W-L%'], axis='columns', inplace=True)
    # Merge and Group
    df = mlb_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=False)
    df.drop(['Population'], axis='columns', inplace=True)
    return df

def nfl(): 
    cities=pd.read_html("1-Intro/assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    # Data Cleaning: cities
    # Drop columns not needed
    cities.drop(['NHL', 'NBA', 'MLB'], axis='columns', inplace=True)
    # Rename Population column and convert it to numeric
    cities.rename(columns={"Population (2016 est.)[8]": "Population"}, inplace=True)
    cities['Population'] = pd.to_numeric(cities['Population'])
    # Clean up NHL column to retain only team names
    cities['NFL'] = cities['NFL'].str.replace('(\[)(note [0-9]+)(\])', '', regex=True)
    cities['NFL'] = cities['NFL'].str.strip()
    cities['NFL'].replace('—', np.NaN, inplace=True)
    cities['NFL'].replace('', np.NaN, inplace=True)
    cities.dropna(inplace=True)
    cities.reset_index(inplace=True, drop=True)

    nfl_df=pd.read_csv("1-Intro/assets/nfl.csv")
    # Data Cleaning: mlb_df
    # Keep only year = 2018 data
    nfl_df = nfl_df[nfl_df['year']==2018]
    # Drop subheaders
    nfl_df.drop(range(0, 40, 5), axis='rows', inplace=True)
    # Drop irrelevant columns
    nfl_df.drop(['DSRS', 'L', 'League', 'MoV', 'OSRS', 'PA', 'PD', 'PF', 'SRS', 'SoS', 'T', 'W', 'year'], axis='columns', inplace=True)
    # Remove '*' and '+' from team
    nfl_df['team'] = nfl_df['team'].str.replace('\*|\+', '', regex=True)
    # Create column for Metropolitan area
    nfl_df['Metropolitan area'] = nfl_df['team'].map({'New England Patriots':'Boston',
     'Miami Dolphins':'Miami–Fort Lauderdale',
     'Buffalo Bills':'Buffalo',
     'New York Jets':'New York City',
     'Baltimore Ravens':'Baltimore',
     'Pittsburgh Steelers':'Pittsburgh',
     'Cleveland Browns':'Cleveland',
     'Cincinnati Bengals':'Cincinnati',
     'Houston Texans':'Houston',
     'Indianapolis Colts':'Indianapolis',
     'Tennessee Titans':'Nashville',
     'Jacksonville Jaguars':'Jacksonville',
     'Kansas City Chiefs':'Kansas City',
     'Los Angeles Chargers':'Los Angeles',
     'Denver Broncos':'Denver',
     'Oakland Raiders':'San Francisco Bay Area',
     'Dallas Cowboys':'Dallas–Fort Worth',
     'Philadelphia Eagles':'Philadelphia',
     'Washington Redskins':'Washington, D.C.',
     'New York Giants':'New York City',
     'Chicago Bears':'Chicago',
     'Minnesota Vikings':'Minneapolis–Saint Paul',
     'Green Bay Packers':'Green Bay',
     'Detroit Lions':'Detroit',
     'New Orleans Saints':'New Orleans',
     'Carolina Panthers':'Charlotte',
     'Atlanta Falcons':'Atlanta',
     'Tampa Bay Buccaneers':'Tampa Bay Area',
     'Los Angeles Rams':'Los Angeles',
     'Seattle Seahawks':'Seattle',
     'San Francisco 49ers':'San Francisco Bay Area',
     'Arizona Cardinals':'Phoenix'}) 
    # Convert W-L% to numeric
    nfl_df['W/L'] = to_numeric(nfl_df['W-L%'])
    nfl_df.drop(['W-L%'], axis='columns', inplace=True)
    nfl_df.reset_index(inplace=True, drop=True)
    
    # Merge and Group
    df = nfl_df.merge(cities, left_on='Metropolitan area', right_on='Metropolitan area', how='left')
    df = df.groupby('Metropolitan area').mean().reset_index(drop=False)
    df.drop(['Population'], axis='columns', inplace=True)

    return df

def sports_team_performance():
    
    nhl_df = nhl()
    nba_df = nba()
    mlb_df = mlb()
    nfl_df = nfl()
    
    # Merge Tables and Calculate p_values between W/L ratio
    nba_nfl = pd.merge(nba_df,nfl_df, on='Metropolitan area')
    pval_nba_nfl = stats.ttest_rel(nba_nfl['W/L_x'],nba_nfl['W/L_y'])[1]
    nba_nhl = pd.merge(nba_df,nhl_df, on='Metropolitan area')
    pval_nba_nhl = stats.ttest_rel(nba_nhl['W/L_x'],nba_nhl['W/L_y'])[1]
    mlb_nfl = pd.merge(mlb_df,nfl_df, on='Metropolitan area')
    pval_mlb_nfl = stats.ttest_rel(mlb_nfl['W/L_x'],mlb_nfl['W/L_y'])[1]
    mlb_nhl = pd.merge(mlb_df,nhl_df, on='Metropolitan area')
    pval_mlb_nhl = stats.ttest_rel(mlb_nhl['W/L_x'],mlb_nhl['W/L_y'])[1]
    mlb_nba = pd.merge(mlb_df,nba_df, on='Metropolitan area')
    pval_mlb_nba = stats.ttest_rel(mlb_nba['W/L_x'],mlb_nba['W/L_y'])[1]
    nhl_nfl = pd.merge(nhl_df,nfl_df, on='Metropolitan area')
    pval_nhl_nfl = stats.ttest_rel(nhl_nfl['W/L_x'],nhl_nfl['W/L_y'])[1]
    
    p_values_dict = {'NFL': {"NFL": np.nan, 'NBA': pval_nba_nfl, 'NHL': pval_nhl_nfl, 'MLB': pval_mlb_nfl},
     'NBA': {"NFL": pval_nba_nfl, 'NBA': np.nan, 'NHL': pval_nba_nhl, 'MLB': pval_mlb_nba},
     'NHL': {"NFL": pval_nhl_nfl, 'NBA': pval_nba_nhl, 'NHL': np.nan, 'MLB': pval_mlb_nhl},
     'MLB': {"NFL": pval_mlb_nfl, 'NBA': pval_mlb_nba, 'NHL': pval_mlb_nhl, 'MLB': np.nan}
    }
    p_values = pd.DataFrame(p_values_dict)
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values

sports_team_performance()