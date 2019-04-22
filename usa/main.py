import pandas as pd
import matplotlib.pyplot as plt
import dateutil
import seaborn as sns


# COLLATE DATA

congress_df = pd.read_csv(
    "usa/data/parsed/congress.csv", index_col="start_year"
).drop(columns=["Unnamed: 0"])

presidents_df = (
    pd.read_csv("usa/data/parsed/presidents.csv")
    .sort_values(["start_date"], ascending=False)
    .drop(columns=["Unnamed: 0"])
)

incomes_df = pd.read_csv(
    "usa/data/parsed/median_incomes.csv", index_col="year"
).drop(columns=["Unnamed: 0"])

violent_crime_df = pd.read_csv(
    "usa/data/parsed/violent_crime_rate.csv", index_col="year"
).drop(columns=["Unnamed: 0"])

presidents_df["start_year"] = presidents_df.start_date.apply(
    lambda d: dateutil.parser.parse(d).year
)

data = []

for year in range(1967, 2016):
    congress_key = year if year % 2 == 1 else year - 1
    congress = congress_df.loc[congress_key, :]
    president = presidents_df[presidents_df.start_year <= year].iloc[0]

    # we increase the year by to offset changes due to previous administration
    median_income = incomes_df.loc[year + 1, :]
    violent_crime_rate = violent_crime_df.loc[year + 1].violent_crime_rate

    senate_rep_over_dem = (
        congress.senate_republicans / congress.senate_democrats
    )
    house_rep_over_dem = (
        congress.house_of_reps_republicans / congress.house_of_reps_democrats
    )

    president_senate_and_house_all_same = (
        (senate_rep_over_dem > 1)
        == (house_rep_over_dem > 1)
        == (president.party == "Republican")
    )

    data += [
        {
            "year": year,
            "median_income": median_income.income,
            "violent_crime_rate": violent_crime_rate,
            "president_dem": president.party == "Democratic",
            "president_rep": president.party == "Republican",
            "senate_rep_over_dem": senate_rep_over_dem,
            "house_rep_over_dem": house_rep_over_dem,
            "president_senate_and_house_all_same": float(
                president_senate_and_house_all_same
            ),
            "president_senate_same": float(
                (senate_rep_over_dem > 1) == (president.party == "Republican")
            ),
            "president_house_same": float(
                (house_rep_over_dem > 1) == (president.party == "Republican")
            ),
            "senate_house_same": float(
                (house_rep_over_dem > 1) == (senate_rep_over_dem > 1)
            ),
            "more_reps_than_dems_in_house": congress.house_of_reps_republicans
            > congress.house_of_reps_democrats,
            "more_reps_than_dems_in_senate": congress.senate_republicans
            > congress.senate_democrats,
        }
    ]

df = pd.DataFrame(data).set_index("year", drop=False)

df["median_income_diff"] = df.median_income.diff()
df["violent_crime_rate_diff"] = df.violent_crime_rate.diff()


sns.lineplot(x="year", y="median_income", data=df)

df[df.president_dem].median_income_diff.mean()
df[df.president_rep].median_income_diff.mean()

df[df.more_reps_than_dems_in_house].median_income_diff.mean()
df[~df.more_reps_than_dems_in_house].median_income_diff.mean()

df[df.more_reps_than_dems_in_senate].median_income_diff.mean()
df[~df.more_reps_than_dems_in_senate].median_income_diff.mean()

df.corr().median_income_diff.sort_values(ascending=False)
df.corr().violent_crime_rate.sort_values(ascending=True)


# PLOTS
