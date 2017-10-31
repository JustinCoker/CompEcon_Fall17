# distance module


def dist(df, latcol, loncol, point):

    '''
    This function calculates the distance between a fixed point passed to
    the function and pairs of lattitude, longitude ponts contained in a
    dataframe.

    Input:
        df, a dataframe containing lattidue, longitude coordinates.

        latcol, loncol: the names of the dataframe columns containing
        lattitude, longitude points, respectively.

        point: a fixed lattitude, longitude point.

    Output:
        df: A dataframe which is the result of joining df with a 'dist'
        column, which contains the distance between the latcol, loncol value
        and the fixed point.
    '''

    from geopy.distance import vincenty

    df_points = df[[latcol, loncol]].values.tolist()

    dist = [vincenty(el, point).meters for el in df_points]

    df['dist'] = dist

    return df
