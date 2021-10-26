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
    # Remove first two column of blanks
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
    
    # Import GDP data, skip headers
    gdp = pd.read_csv("1-Intro/assets/world_bank.csv", skiprows=4)
    # Rename countries
    gdp['Country Name'] = gdp['Country Name'].replace("Korea, Rep.", "South Korea")
    gdp['Country Name'] = gdp['Country Name'].replace("Iran, Islamic Rep.", "Iran")
    gdp['Country Name'] = gdp['Country Name'].replace("Hong Kong SAR, China", "Hong Kong")
    # Take relevant columns
    gdp = gdp[['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    gdp.columns = ['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    
    # Import ScimEm data
    ScimEm = pd.read_excel("1-Intro/assets/scimagojr-3.xlsx")
    # Take the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
    ScimEm_15 = ScimEm[:15]

    # Merge datasets
    df = pd.merge(ScimEm_15, energy, how='inner', left_on='Country', right_on='Country')
    dataset = pd.merge(df, gdp, how='inner', left_on='Country', right_on='Country')
    
    # Set index as Country
    dataset.set_index('Country', inplace=True)

    return dataset

def answer_two():
    return 161-15

def answer_three():
    dataset = answer_one()
    gdp = dataset[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    gdp_mean = gdp.mean(axis=1, skipna=True)
    return gdp_mean

def answer_four():
    dataset = answer_one()

    # Country with 6th largest average GDP
    gdp_mean = answer_three()    
    gdp_mean.sort_values(ascending=False, inplace=True)
    # Country with 6th largest average GDP is 'United Kingdom'
    
    # Calculate GDP Change
    gdpChange= dataset['2015']['United Kingdom'] - dataset['2006']['United Kingdom']
    return gdpChange

def answer_five():
    dataset = answer_one()
    # What is the mean energy supply per capita?
    ESPC = dataset['Energy Supply per Capita']
    mean = ESPC.mean(axis=0, skipna=True)
    return mean

def answer_six():
    # What country has the maximum % Renewable and what is the percentage?
    renewable = answer_one()['% Renewable']
    max = renewable[renewable==renewable.max(axis=0)]
    return list(zip(max.index, max))[0]

def answer_seven():
    # Create a new column that is the ratio of Self-Citations to Total Citations
    citation = answer_one()['Self-citations']/answer_one()['Citations']
    
    # What is the maximum value for this new column, and what country has the highest ratio?
    max = citation[citation==citation.max(axis=0)]
    return list(zip(max.index, max))[0]

def answer_eight():
    # Create a column that estimates the population using Energy Supply and Energy Supply per capita
    population = answer_one()['Energy Supply']/answer_one()['Energy Supply per Capita']
    
    # What is the third most populous country according to this estimate?
    population.sort_values(axis=0, ascending=False, inplace=True)
    
    return "United States"

def answer_nine():
    # Create a column that estimates the number of citable documents per person
    dataset = answer_one()
    dataset['Citable Documents per Person'] = dataset['Citable documents']/(dataset['Energy Supply']/dataset['Energy Supply per Capita'])
    # What is the correlation between the number of citable documents per capita and the energy supply per capita?
    correlation = dataset['Citable Documents per Person'].corr(dataset['Energy Supply per Capita']) 
    return correlation

def answer_ten():
    # Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, 
    # and a 0 if the country's % Renewable value is below the median.
    dataset = answer_one()
    renewable = dataset['% Renewable']
    median = renewable.median(axis=0)
    dataset['HighRenew'] = [1 if x >= median else 0 for x in dataset['% Renewable']]
    return dataset['HighRenew']

def answer_eleven():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # Create a DataFrame that displays the sample size (the number of countries in each continent bin),
    # and the sum, mean, and std deviation for the estimated population of each country
    
    # Population Estimate
    dataset = answer_one()
    dataset['Population'] = dataset['Energy Supply']/dataset['Energy Supply per Capita']
    dataset.reset_index(inplace=True)
    
    # Continent 
    dataset['Continent'] = [ContinentDict[country] for country in dataset['Country']]
    
    # Set and group by Continent. Then, aggregate by Population
    df = dataset.set_index('Continent').groupby(level='Continent')['Population'].agg(['size', 'sum', 'mean', 'std'])
    return df

def answer_twelve():
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    # Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. 
    dataset = answer_one()
    dataset.reset_index(inplace=True)

    # Continent 
    dataset['Continent'] = [ContinentDict[country] for country in dataset['Country']]
    
    dataset['bins'] = pd.cut(dataset['% Renewable'], 5)

    # How many countries are in each of these groups?
    return dataset.groupby(['Continent', 'bins']).size()

def answer_thirteen():
    # Convert the Population Estimate series to a string with thousands separator (using commas).
    # Population Estimate
    dataset = answer_one()
    dataset['Pop'] = dataset['Energy Supply']/dataset['Energy Supply per Capita'].astype(float)
    series=[]
    for pop in dataset['Pop']:
        series.append('{:,}'.format(pop))
    dataset['Pop1'] = series
    return dataset['Pop1']

print(answer_thirteen())