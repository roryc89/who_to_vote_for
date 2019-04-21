from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

r = requests.get("http://inflation.iamkate.com/")

soup = BeautifulSoup(r.text, "html.parser")

print(soup.prettify())

rows = soup.find_all("tr")


def get_df_row(row):
    cells = row.find_all("td")

    return {
        "year": int(cells[0].text),
        "inflation": float(re.sub("%", "", cells[1].text or "0")),
        "multiplier": float(cells[2].text or 1),
    }


df = pd.DataFrame(list(map(get_df_row, rows[1:]))).set_index("year")

df.to_csv("uk/data/parsed/inflation.csv")
