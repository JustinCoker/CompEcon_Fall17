import pandas as pd

raw_data = pd.read_excel(r'radio_merger_data.xlsx')  # read data

raw_data = raw_data.drop([11, 14])  # dropping record 11 & 14: duplicates

# split by year and reset index
actual_2007 = raw_data[raw_data.year == 2007].reset_index()

actual_2008 = raw_data[raw_data.year == 2008].reset_index()
