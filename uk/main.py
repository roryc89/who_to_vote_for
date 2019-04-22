import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.collections as collections

govs_raw = pd.read_csv("uk/data/parsed/govs.csv").sort_values(
    ["year", "month"], ascending=False
)
govs_raw
# As government policies may take time to take effect we are increasing their
# year by 1 on each
govs_raw.year = govs_raw.year + 1

govs_raw["total_months"] = govs_raw.year * 12 + govs_raw.month


earnings_raw = pd.read_csv("uk/data/parsed/median_earnings.csv").set_index(
    "year"
)

combined_data = []

for year in range(1969, 2018):
    govs_before_year = govs_raw[govs_raw.year <= year]
    earning_start_of_year = earnings_raw.loc[year]
    earning_end_of_year = earnings_raw.loc[year + 1]
    for month in range(1, 13):
        total_months = year * 12 + month
        party = (
            govs_before_year[govs_before_year.total_months <= total_months]
            .iloc[0]
            .party
        )

        def get_weighted_earning(col):
            return (
                (earning_start_of_year[col] * (12 - month))
                + (earning_end_of_year[col] * month)
            ) / 12

        combined_data += [
            {
                "year": year,
                "month": month,
                "year_and_month": year * 12 + month,
                "party": party,
                "male": get_weighted_earning("male"),
                "female": get_weighted_earning("female"),
                "both": get_weighted_earning("both"),
            }
        ]

earnings_df = pd.DataFrame(combined_data)

earnings_diff = earnings_df.loc[:, ["male", "female", "both"]].diff()


earnings_df["male_annual_diff"] = earnings_diff.male * 52 * 12
earnings_df["female_annual_diff"] = earnings_diff.female * 52 * 12
earnings_df["both_annual_diff"] = earnings_diff.both * 52 * 12

earnings_df["is_labour"] = (earnings_df.party == "Labour").astype("float")
earnings_df["is_conservative"] = earnings_df.party == "Conservative"

ax = earnings_df.plot.line("year", ["male"])

plt.xlabel("year")
plt.ylabel("change in earnings")

plt.title("Change in annual male median earnings, inflation adjusted")

ax.pcolorfast(
    ax.get_xlim(),
    ax.get_ylim(),
    earnings_df["is_labour"].values[np.newaxis],
    cmap="RdYlGn",
    alpha=0.3,
)

plt.legend()

plt.show()


earnings_df[earnings_df.party == "Labour"].male_annual_diff.mean()
earnings_df[earnings_df.party == "Conservative"].male_annual_diff.mean()


earnings_df[earnings_df.party == "Labour"].female_annual_diff.mean()
earnings_df[earnings_df.party == "Conservative"].female_annual_diff.mean()
