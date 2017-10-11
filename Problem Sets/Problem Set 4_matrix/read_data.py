import pandas as pd

raw_data = pd.read_excel(r'radio_merger_data.xlsx')  # read data

# split by year and reset index
actual_2007 = raw_data[raw_data.year == 2007].reset_index()

actual_2008 = raw_data[raw_data.year == 2008].reset_index()

# transform population into thousands of people
actual_2007['population_target'] = actual_2007['population_target'] / 100000

actual_2008['population_target'] = actual_2008['population_target'] / 100000
