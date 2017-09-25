#"/media/j/TOSHIBA/OneDrive - University of South Carolina - Moore School of Business/CompEcon_Fall17/Problem Sets/Problem Set 3"
#%%
import pandas as pd

data = pd.read_stata('PS3_data.dta')

print(set(data.relhh.values))
#Our data only contains heads of household

print(set(data.hsex.values))
#Our data contains both male and female heads of household.

data = data[data.hsex == 1]
print(set(data.hsex.values))
#We now have only males

print(set(data.age.values))
data = data[data.age <= 60]
data = data[data.age >= 25]
print(set(data.age.values))

#We now have only males between 25 and 60

#%%

data = data[data.hannhrs >0]
#dropping obs with 0 hours worked

#dropping individuals with nan hours or annual income
data = data.dropna(how='any', subset=['hannhrs', 'hlabinc'])

data['hwage'] = data.hlabinc/data.hannhrs
#creating hourly wage

data = data[data.hwage > 7.0]
#We now have only male heads of household between 25 and 60 with wage>7 and hours>0
#%%
import numpy as np

data = data.dropna(how='any', subset=['hrace', 'hyrsed'])
#dropping obs with missing race

print(set(data.hrace.values))
#race only takes values 1,2,3

#createing race dummies
data['black'] = np.where(data['hrace']==2, 1, 0)

data['hispanic'] = np.where(data['hrace']==5, 1, 0)

data['other'] = np.where(((data['hrace'] !=1 ) & (data['hrace'] != 2) & (data['hrace'] !=5)), 1, 0)