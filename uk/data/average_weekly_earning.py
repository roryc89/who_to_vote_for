import pandas as pd
import numpy as np

# data downloaded from https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/adhocs/009216earningstimeseriesofmediangrossweeklyearningsfrom1968to2018
# and a couple of cells renamed to make them valid years.
# Specifically 2004inc => 2004 and 2006inc => 2006

FILE_NAME = "uk/data/AVERAGE_GROSS_WEEKLY_EARNINGS_1968-2018.xls"
SHEET_NAME = "GB Median Time-series"

weekly_mean_earnings = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME)

weekly_mean_earnings = weekly_mean_earnings.iloc[11:70, [1, 7, 17, 27]]
weekly_mean_earnings.columns = ["year", "male", "female", "both"]


def is_int(string):
    try:
        int(string)
        return True
    except:
        return False


def set_nas(cell):
    if is_int(cell):
        return int(cell)
    else:
        return np.nan


weekly_mean_earnings = (
    weekly_mean_earnings[weekly_mean_earnings.year.apply(is_int)]
    .set_index("year")
    .applymap(set_nas)
)

weekly_mean_earnings
