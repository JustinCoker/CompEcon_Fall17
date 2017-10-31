import combine

import numpy as np

import pandas as pd

from matplotlib import pyplot as plt

crime2015, crime2016 = combine.combine_main()


def bindata(df):
    '''
    This function bins the crime dataframes using 4 minute bins
    '''

    # group the data by time until the end of a game
    # save only count and time, drop if no game
    grouped = (df.groupby('t-minus', as_index=False)
               .count()[['OFFENSE', 't-minus']][:-1])

# drop crimes more than 70 minutes from the end of a game
    grouped = grouped[(grouped['t-minus'] >= -70) &
                      (grouped['t-minus'] <= 70)].reset_index(drop=True)

    bins = np.linspace(-70, 70, 35)  # creates 4 minute bins

    grouped['bin'] = pd.cut(grouped['t-minus'], bins, include_lowest=True)

    # the output of pd.cut() does not play well with others, transforming to
    # list in order to remove NaNs and plot binned data.

    y = grouped.groupby('bin', as_index=False).mean().OFFENSE.tolist()

    # midpoint of the 4 minute bins as x axis
    xaxis = [x.mid for x in
             grouped.groupby('bin', as_index=False).mean().bin.tolist()]

    # removing NaNs (which are really zeros that pd.cut().mean() can't handle)
    yaxis = [0 if np.isnan(y) else y for y in y]

    return xaxis, yaxis


def bestfit(x, y, d):
    '''
    This function uses np.polyfit to return the y values for a line of best fit
    given x, y values as lists and the degree of polynomial, d.
    '''

    if d == 1:
        m, b = np.polyfit(x, y, d)
        y = [m * x + b for x in x]

    if d == 2:
        a, m, b = np.polyfit(x, y, d)
        y = [a * x ** 2 + m * x + b for x in x]

    if d == 3:
        b, a, m, b = np.polyfit(x, y, d)
        y = [b * x ** 3 + a * x ** 2 + m * x + b for x in x]
    return y


def RDplot(df, degree):
    '''
    This function plots an RD diagnostic graph for the crime dataframes given
    the dataframe and the desired degree polynomial for the fit line.
    '''
    x, y = bindata(df)
    plt.scatter(x, y)
    plt.plot((0, 0), (0, 5), color='r')
    plt.plot(x[:17], bestfit(x[:17], y[:17], degree), color='g')
    plt.plot(x[17:], bestfit(x[17:], y[17:], degree), color='g')
    plt.axis((-60, 60, 0, 5))
    plt.xlabel("Time until Game Ends")
    plt.ylabel("Number of Crimes")
    plt.show()


RDplot(crime2015, 1)

RDplot(crime2015, 2)

RDplot(crime2016, 1)

RDplot(crime2016, 2)

x, y = bindata(crime2015)
cut = [1 if i>0 else 0 for i in x]
binned2015 = pd.DataFrame({'TimeBin': x,
                           'CrimeCount': y,
                           'Crowd': cut
                           })

binned2015['TimeSq'] = binned2015['TimeBin'] ** 2

x, y = bindata(crime2016)
binned2016 = pd.DataFrame({'TimeBin': x,
                           'CrimeCount': y,
                           'Crowd': cut
                           })

binned2016['TimeSq'] = binned2016['TimeBin'] ** 2

binned2015.to_csv('bin_crime2015')

binned2016.to_csv('bin_crime2016')
