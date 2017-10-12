'''
This script uses the actual match dataframes to create the dataframe of
counter factual matches using list comprehension
'''


# selects the buyer, target characteristics
B = ['year', 'buyer_id', 'corp_owner_buyer',
     'buyer_lat', 'buyer_long', 'num_stations_buyer']

T = ['target_id', 'price', 'target_lat', 'target_long',
     'hhi_target', 'population_target']

a = [actual_2007, actual_2008]  # list of dataframes used in counter factual

counter_fact = pd.DataFrame()  # initialize counter_fact df


# using list comprehension to create the counter factual

counter_fact = [el[B].iloc[i].values.tolist() +
                el[T].iloc[j].values.tolist()
                for el in a for i in range(len(el))
                for j in range(len(el)) if i != j]

# The counter-factual match dataframe
counter_fact = pd.DataFrame(counter_fact, columns=B + T)
