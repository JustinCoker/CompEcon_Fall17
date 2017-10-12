'''
This script imports the PS4 data, splits the actual matches into 2 dataframes
and transforms price and population into hundreds of thousdands of people and
dollars.

Note: assumes data is in the current working directory.

input: None

output: 2 DataFrames countaining actual match data.

'''


import pandas as pd

raw_data = pd.read_excel(r'radio_merger_data.xlsx')  # read data

# split by year and reset index
actual_2007 = raw_data[raw_data.year == 2007].reset_index()

actual_2008 = raw_data[raw_data.year == 2008].reset_index()

# transform population, price into 100 thousands of people, dollars
actual_2007[['price', 'population_target']] = actual_2007[
    ['price', 'population_target']] / 100000

actual_2008[['price', 'population_target']] = actual_2008[
    ['price', 'population_target']] / 100000
