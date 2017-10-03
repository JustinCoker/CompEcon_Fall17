B = ['year', 'buyer_id', 'corp_owner_buyer',
     'buyer_lat', 'buyer_long', 'num_stations_buyer']

T = ['target_id', 'price', 'target_lat', 'target_long',
     'hhi_target', 'population_target']

counter_fact = pd.DataFrame()

a = [actual_2007, actual_2008]

for k in a:
    for i in range(len(k)):
        for j in range(len(k)):
            if i != j:
                counter_fact = counter_fact.append(
                    pd.concat([k[B].iloc[[i]].reset_index(drop=True),
                               k[T].iloc[[j]].reset_index(drop=True)], axis=1))
