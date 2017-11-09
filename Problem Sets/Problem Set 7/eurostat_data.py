def main():

    import pandas as pd
    from pyjstat import pyjstat

    eurostat = "http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/"
    rdURL1 = ("rd_e_gerdreg?precision=2&sectperf=TOTAL&sinceTimePeriod=1986&unit="
          "EUR_HAB&filterNonGeo=1&shortLabel=1&geoLevel=nuts2&grouped"
          "Indicators=1&unitLabel=code")

    url = eurostat + rdURL1

    dataset = pyjstat.Dataset.read(url)

    df = dataset.write('dataframe')

    # get region codes from the pyjstat dataset dict(s)
    region_code = list(dataset["dimension"]["geo"]["category"]["label"].items())

    # create a list to be added to df (each region appears for 28 years/rows)
    region = [el for el in region_code for i in range(29)]

    df['region'] = region

    # keep only region, year, values
    df = df[['region', 'time', 'value']]

    # reshape the data in panel format
    panel = df.pivot(index='region', columns='time', values='value')

    # Moves 'region' back to a column and resets the index from 0
    panel = panel.reset_index()

    # split (code, Name) tuple into 2 columns
    panel[["NUTS_ID", "Name"]] = panel.region.apply(pd.Series)

    return panel
