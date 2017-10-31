import pandas as pd

import datetime


def date_time(df):
    '''
    The START_DATE and END_DATE fields are badly formatted,
    we need a columns YYYY-MM-DD HH:MM:SS format to apply datetime

    This function removes ".000Z" from the end and replaces T with " " in the
    START_DATE and END_DATE columns of df. Then adds stime and etime columns,
    which contain datetime objects to df and returns df
    '''
    df.END_DATE.fillna(df.START_DATE, inplace=True)  # fill missing values

    df['stime'] = pd.to_datetime([el[:-5].replace('T', ' ')
                                  for el in df.START_DATE.tolist()])

    df['etime'] = pd.to_datetime([el[:-5].replace('T', ' ')
                                  for el in df.END_DATE.tolist()])

    return df


def crime_main():
    '''
    This function reads in the 2015 and 2016 Washington DC crime data, drops
    unnecessary data, adds distance to nationals park column using the distance
    module (see distance.py), and converts time stamps into datetime objects
    by applying date_time() function.

    Returns crime2015 and crime2016 dataframes.
    '''

    cols = ['METHOD', 'OFFENSE', 'WARD', 'PSA', 'BLOCK_GROUP',
            'LATITUDE', 'LONGITUDE', 'START_DATE', 'END_DATE']

    crime2015 = pd.read_csv('Crime2015.csv', usecols=cols)

    crime2016 = pd.read_csv('Crime2016.csv', usecols=cols)

    '''
    Nationals Park is in Washington's 6th Ward.

    There is a significant distance to the Ward border to the 2nd Ward to the
    North East, the border of which is along I-695, limiting any foot traffic
    spillover in to the 2nd Ward

    The Potomac and Anacostia river limit any foot traffic from the
    stadium to the South-West and South, respectively and form the border
    between the 6th and 8th Wards. Source: Google Maps

    As such, we can safely drop any crime that did not occur in the 6th
    Ward before performing any further manipulation.
    '''

    crime2015, crime2016 = (crime2015[crime2015.WARD == 6]
                            .reset_index(drop=True),
                            crime2016[crime2016.WARD == 6]
                            .reset_index(drop=True))

    from distance import dist  # see distance.py

    point = (38.873181, -77.007546)  # approx. lat, lon of Nationals Stadium

    crime2015 = dist(crime2015, 'LATITUDE', 'LONGITUDE', point)

    crime2016 = dist(crime2016, 'LATITUDE', 'LONGITUDE', point)

    crime2015 = date_time(crime2015)

    crime2016 = date_time(crime2016)

    return crime2015, crime2016
