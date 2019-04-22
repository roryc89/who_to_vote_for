from bs4 import BeautifulSoup
import pandas as pd
import re
import requests


page = requests.get(
    "https://www.multpl.com/us-median-real-income/table/by-year"
).text

soup = BeautifulSoup(page)

rows = soup.find_all("tr")

median_incomes = []

for row in rows:
    try:
        cells = row.find_all("td")
        year = int(cells[0].text.split(", ")[1])
        income = float(re.sub(",", "", cells[1].text))
        median_incomes += [{"year": year, "income": income}]
    except:
        pass


pd.DataFrame(median_incomes).to_csv("usa/data/parsed/median_incomes.csv")
