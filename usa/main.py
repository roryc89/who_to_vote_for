import pandas as pd
import matplotlib.pyplot as plt
import dateutil
import numpy as np
import seaborn as sns
import six


def render_mpl_table(
    data,
    col_width=3.0,
    row_height=0.625,
    font_size=14,
    header_color="#40466e",
    row_colors=["#f1f1f2", "w"],
    edge_color="w",
    bbox=[0, 0, 1, 1],
    header_columns=0,
    ax=None,
    **kwargs
):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array(
            [col_width, row_height]
        )
        fig, ax = plt.subplots(figsize=size)
        ax.axis("off")

    mpl_table = ax.table(
        cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs
    )

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight="bold", color="w")
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax


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

national_debt_df = pd.read_csv(
    "usa/data/parsed/national_debt.csv", index_col="year"
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
    result_shift = 1
    median_income = incomes_df.loc[year + result_shift, :]

    violent_crime_rate = violent_crime_df.loc[
        year + result_shift
    ].violent_crime_rate

    national_debt = national_debt_df.loc[year + result_shift].national_debt

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
            "national_debt": national_debt,
            "party": president.party,
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
df["national_debt_diff"] = df.national_debt.diff()


cols = ["median_income", "violent_crime_rate", "national_debt"]

for col in cols:
    ax = df.plot.line("year", col)

    plt.xlabel("year")

    units = {
        "median_income": "$",
        "violent_crime_rate": "per 100,0000",
        "national_debt": "billion $",
    }

    plt.ylabel(col + " (" + units[col] + ")")

    plt.title("Red = Democrat, Green = Republican")

    ax.pcolorfast(
        ax.get_xlim(),
        ax.get_ylim(),
        df["president_rep"].values[np.newaxis],
        cmap="RdYlGn",
        alpha=0.3,
    )

    plt.legend()

    plt.show()


cols = [
    "president_rep",
    "more_reps_than_dems_in_house",
    "more_reps_than_dems_in_senate",
]

aggs = {
    "median_income_diff": "mean",
    "violent_crime_rate_diff": "mean",
    "national_debt_diff": "mean",
}


bars = df.groupby(["party"]).agg(aggs)

pres_cols = [
    ["median_income_diff", "annual change in income"],
    [
        "violent_crime_rate_diff",
        "annual change in violent crime rate (per 100,000 pop)",
    ],
    ["national_debt_diff", "national debt (billions of $)"],
]

for col in pres_cols:

    ax = bars.loc[:, col[0]].plot.bar()
    plt.ylabel(col[1])
    for p in ax.patches:
        anotation = str(p.get_height())[:6]
        ax.annotate(anotation, (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.show()


df.groupby(
    [
        "president_rep",
        "more_reps_than_dems_in_house",
        "more_reps_than_dems_in_senate",
    ]
).agg(aggs)


df[df.president_dem].median_income_diff.mean()
df[df.president_rep].median_income_diff.mean()

df[df.president_dem].violent_crime_rate_diff.mean()
df[df.president_rep].violent_crime_rate_diff.mean()

df[df.president_dem].national_debt_diff.mean()
df[df.president_rep].national_debt_diff.mean()

df[df.more_reps_than_dems_in_house].median_income_diff.mean()
df[~df.more_reps_than_dems_in_house].median_income_diff.mean()

df[df.more_reps_than_dems_in_senate].median_income_diff.mean()
df[~df.more_reps_than_dems_in_senate].median_income_diff.mean()

df.corr()
correlations = df.corr().loc[
    [
        "president_rep",
        "more_reps_than_dems_in_house",
        "more_reps_than_dems_in_senate",
    ],
    ["median_income_diff", "violent_crime_rate_diff", "national_debt_diff"],
]
correlations.columns = ["median income", "violent crime", "national debt"]
correlations["Controlled by republicans"] = [
    "White house",
    "House of representatives",
    "Senate",
]
correlations = correlations[correlations.columns[[3, 0, 1, 2]]]
correlations
render_mpl_table(correlations)

df.corr().median_income_diff.sort_values(ascending=False)

df.corr().violent_crime_rate.sort_values(ascending=True)


# PLOTS
