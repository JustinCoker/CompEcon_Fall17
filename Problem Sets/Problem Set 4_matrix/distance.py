'''


'''

from geopy.distance import vincenty

import numpy as np


def dist(df, latlon1, latlon2):
    '''
    This function calulates distance between 2 lattitude, longitude pairs
    where these pairs are found in dataframe columns

    Input:
        df: a dataframe, the columns of which contain lattitude, longitude
            coordinates

        latlon1: a tuple of column names which contains lattitude and longitude
                 respectively

        latlon2: a tuple of column names containing the lattitude longitude
                 respectively of the second location.
    '''

    l = latlon1 + latlon2  # creates lattitude, longitude pairs

    a, b = np.split(df[l].values, 2, axis=1)  # splits lat, long pairs

    if len(a) == len(b):
        # calculates distance
        distance = [vincenty(a[i], b[i]).miles for i in range(len(a))]

        return distance

    else:
        print('lat, long columns in DataFrame are not of equal lengths')


dfs = [actual_2007, actual_2008, counter_fact]

latlon1 = ['buyer_lat', 'buyer_long']

latlon2 = ['target_lat', 'target_long']

for el in dfs:
    # calls the distance function on dataframes
    el['distance'] = dist(el, latlon1, latlon2)
