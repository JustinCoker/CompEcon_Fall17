B = ['year', 'buyer_id', 'corp_owner_buyer',
     'buyer_lat', 'buyer_long', 'num_stations_buyer']

T = ['target_id', 'price', 'target_lat', 'target_long',
     'hhi_target', 'population_target']

a = [actual_2007, actual_2008]


counter_fact = pd.DataFrame()
'''
for k in a:
    for i in range(len(k)):
        for j in range(len(k)):
            if i != j:
                counter_fact = counter_fact.append(
                    pd.concat([k[B].iloc[[i]].reset_index(drop=True),
                               k[T].iloc[[j]].reset_index(drop=True)], axis=1))
'''

# using list comprehension to create the counter factual

counter_fact = [el[B].iloc[i].values.tolist() +
                el[T].iloc[j].values.tolist()
                for el in a for i in range(len(el))
                for j in range(len(el)) if i != j]

counter_fact = pd.DataFrame(counter_fact, columns=B + T)
