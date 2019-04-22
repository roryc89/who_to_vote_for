from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import dateutil

URL = "https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States"

page = requests.get(URL).text

soup = BeautifulSoup(page)

rows = soup.select_one("table.wikitable tbody").find_all("tr")

presidents = []

for row in rows:
    try:
        cells = row.find_all("td")
        start_date = dateutil.parser.parse(cells[1].select_one(".date").text)
        party = cells[6].find("a").text
        presidents += [{"start_date": start_date, "party": party}]
    except Exception as e:
        print("e", e)
        pass

pd.DataFrame(presidents).to_csv("usa/data/parsed/presidents.csv")
