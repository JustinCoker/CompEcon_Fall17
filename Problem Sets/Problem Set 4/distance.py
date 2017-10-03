from geopy.distance import vincenty

import numpy as np


def dist(df, latlon1, latlon2):

    l = latlon1 + latlon2

    a, b = np.split(df[l].values, 2, axis=1)

    if len(a) == len(b):

        distance = [vincenty(a[i], b[i]).miles for i in range(len(a))]

        return distance

    else:
        print('lat, long columns in DataFrame are not of equal lengths')


testdist = dist(actual_2008, ['buyer_lat', 'buyer_long'],
                             ['target_lat', 'target_long'])


dfs = [actual_2007, actual_2008, counter_fact]

latlon1 = ['buyer_lat', 'buyer_long']

latlon2 = ['target_lat', 'target_long']

for el in dfs:
    el['distance'] = dist(el, latlon1, latlon2)
