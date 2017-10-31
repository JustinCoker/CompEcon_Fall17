import pandas as pd

from datetime import timedelta

# mlb data is an "event" .evn file, which is not readily convertable into any
# useful file format like .csv


def read_evn(filename):

    '''
    This function takes a .evn file from retrosheet.org and reads the data
    into a dataframe, the columns of which are the date, start time, duration,
    attendance, and site of each game in a given season.

    Input:
        filename: a raw string, which is the name of the relevant .evn file
        in the current working directory.

    Output:
        a dataframe, rows are each game in a season, columns are date, start,
        duration, attendance, site of the games.
    '''

    in_file = open(filename, "rt")  # opens .evn file containing mlb data

    contents = in_file.read()  # assigns the text from .evn file as string

    data = contents.split("id,")
    # assigns data from each game to an element of the list, data

    data = [el.split("\n") for el in data]
    data = data[1:]  # .split creates an empty 0 element
    # assigns each "variable" to an element of a nested list.
    # data is now a list of key value pairs associated with each game.

    # I need data on the date, start time, attendance, and game duration.

    vars = [5, 7, 23, 24, 4]

    Date, start, duration, attendance, site = [[el[i].split(",")[2]
                                                for el in data] for i in vars]
    # Date is always the 5th element
    # Start_time 7th, duration 23rd, attendance 24th, site 4th.
    # each elements is: 'info,varname","Data"'

    cols = ['date', 'start', 'duration', 'att', 'site']

    gamedata = pd.DataFrame(list(zip(Date, start, duration, attendance, site)),
                            columns=cols)

    return gamedata


def gettime(df, datecol='date', timecol='start', durationcol='duration'):
    '''
    This functions returns the ending time given a dataframe containing date,
    start time, and duration as strings in separate columns

    Input:
        df: a Dateframe containing date, strat time, duration columns

        datecol, timecol, durationcol: the df column names that contain date,
                                       start time, duration respectively.

    Output:
        df: the original dataframe with columns for begin, end time dataframe
            as datetime objects
    '''

    # create begin column as a date time object
    # must use date and time in order to use timedelta properly
    df['begin'] = pd.to_datetime(df[datecol] + ' ' + df[timecol])

    # creates a list of date time object from the begin column
    time = df.begin.tolist()

    # creates time delta object for each element in durationcol
    dur = [timedelta(minutes=int(el)) for el in df[durationcol].tolist()]

    # adds the timedelta objects to the begin time objects, assigns this
    # to the data frame column "end"
    df['end'] = [time[i] + dur[i] for i in range(len(dur))]

    return df


def mlb_main():
    '''
    This function reads in the data through read_evn and begin and end columns
    containing datetimem objects through endtime().

    Returns mlb2015 and mlb2016 dataframes.
    '''
    mlb2016 = read_evn("2016WAS.EVN")

    mlb2015 = read_evn("2015WAS.EVN")

    mlb2016 = gettime(mlb2016)

    mlb2015 = gettime(mlb2015)

    return mlb2015, mlb2016
