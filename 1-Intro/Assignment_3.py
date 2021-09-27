import pandas as pd
import numpy as np

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')

def answer_one():
    # Import Energy data without footer
    energy = pd.read_excel("1-Intro/assets/Energy Indicators.xls", index_col=None, header=None,skipfooter=38)
    # Remove header
    energy = energy[18:]
    # Remove first column of blanks
    energy.drop([0,1], axis=1, inplace=True)
    # Set column headers
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    # Set '...' as NaN
    energy.replace('...', np.NaN, inplace=True)
    # Convert 'Energy Supply' to gigajoules
    energy['Energy Supply'] = energy['Energy Supply']*1000000
    # Rename countries
    # Remove numbers from 'Country'
    energy['Country']=energy['Country'].str.replace('\d+', '')
    # Remove values after parenthesis
    energy['Country']=energy['Country'].str.replace('\s\(.+\)$', '')
    # Set index as 'Country'
    energy.set_index('Country', inplace=True)
    # Rename special 'Country' names
    energy.rename(index={"Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"}, inplace=True)
    
    # Import GDP data
    gdp = pd.read_csv("1-Intro/assets/world_bank.csv", index_col=None, header=None)
    # Remove header
    gdp = gdp[4:]
    # Set first row and column name
    gdp_header = gdp.iloc[0]
    #gdp_header = gdp_header.to_string()
    #gdp_header = gdp_header.str.replace('\.0','A')
    print(gdp_header)
    gdp.columns = gdp_header
    gdp = gdp[1:]
    #print(gdp.head())

answer_one()