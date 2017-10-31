'''
Need to create columns in the crime dfs with an indicator for whether there
was a game on that day and a t- column that indicates the number of minutes
difference between the end time of the game and the stime of the crime
'''


def gametime(crimedf, mlbdf):

    '''
    This function returns a new dataframe with an added column containing:
    the time of the end of the game that was played on the day
    a given crime occured.
    '''

    gamedates = [el for el in mlbdf.end.tolist()]  # sends dates to a list
    # separates the list of dates for date matching
    date, time = zip(*[(el.date(), el.time()) for el in gamedates])
    gametime = []  # initialize gametime list
    crimes = crimedf.stime.tolist()  # sends crime datetimes to a list

    for i in range(len(crimes)):
        if crimes[i].date() in date:  # matches dates
            loc = date.index(crimes[i].date())  # locates the matched date
            gametime.append(gamedates[loc])  # appends time on matched dates

        else:
            gametime.append('nogame')  # appends "nogame" if no matching date

    crimedf['game_end'] = gametime  # creates gametime column in crime df

    return crimedf


def tminus(crimedf):
    '''
    This function creates a "t-minus" column in crimedf by calculating the
    difference between the time the crime occured and the time the game
    ended in minutes.
    '''

    '''must loop over the dataframe because df operations are not possible
       since crimedf.stime is a datetime series and crimedf.gametime is
       a standard df column. Alternative would be looping over the stime
       column and converting it back into a regular df column
       element by element'''

    tminus = []
    gt = crimedf.game_end.tolist()  # sends game endtime to list
    st = crimedf.stime.tolist()  # sends crime time to list

    for i in range(len(st)):
        if gt[i] != 'nogame':

            '''time difference object returns negative days, positive minutes
               if time1 occurs after time. must get the number of minutes
               measure by .days (1440) and add the number of seconds/60 to
               get the actual time difference in minutes'''

            mins = (st[i] - gt[i]).days * 1440 + (st[i] - gt[i]).seconds / 60
            # appends minutues. rounding since gametimes are precise to minutes
            tminus.append(round(mins))

        else:
            tminus.append('nogame')

    crimedf['t-minus'] = tminus  # adds t-minus to crimedf

    return crimedf


def combine_main():

    import mlbdata

    import crimedata

    mlb2015, mlb2016 = mlbdata.mlb_main()

    crime2015, crime2016 = crimedata.crime_main()

    crime2015 = gametime(crime2015, mlb2015)

    crime2016 = gametime(crime2016, mlb2016)

    crime2015 = tminus(crime2015)

    crime2016 = tminus(crime2016)

    return crime2015, crime2016
