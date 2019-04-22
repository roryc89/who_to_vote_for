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


weekly_mean_earnings = weekly_mean_earnings.drop_duplicates(
    subset="year", keep="first"
)


weekly_mean_earnings = (
    weekly_mean_earnings[weekly_mean_earnings.year.apply(is_int)]
    .set_index("year")
    .applymap(set_nas)
)

inflation = pd.read_csv("uk/data/parsed/inflation.csv")
weekly_mean_earnings = pd.merge(weekly_mean_earnings, inflation, on="year")

weekly_mean_earnings.male = (
    weekly_mean_earnings.male * weekly_mean_earnings.multiplier
)

weekly_mean_earnings.female = (
    weekly_mean_earnings.female * weekly_mean_earnings.multiplier
)

weekly_mean_earnings.both = (
    weekly_mean_earnings.both * weekly_mean_earnings.multiplier
)
weekly_mean_earnings = weekly_mean_earnings.drop(
    columns=["multiplier", "inflation"]
)
weekly_mean_earnings
weekly_mean_earnings.to_csv("uk/data/parsed/median_earnings.csv")
