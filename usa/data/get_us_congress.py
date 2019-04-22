from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import dateutil

URL = (
    "https://en.wikipedia.org/wiki/Party_divisions_of_United_States_Congresses"
)

page = requests.get(URL).text

soup = BeautifulSoup(page)

rows = soup.select_one(
    "#mw-content-text > div > table:nth-child(7) > tbody"
).find_all("tr")

congress = []


def parse_count(txt):
    txt = re.sub("([\(\[]).*?([\)\]])", "", txt)
    try:
        return float(txt)
    except:
        try:
            return (float(txt.split("-")[0]) + float(txt.split("-")[1])) / 2
        except:
            try:
                return (
                    float(txt.split("–")[0]) + float(txt.split("–")[1])
                ) / 2
            except:
                print("hard txt", txt)
                return (
                    float(txt.split("/")[0]) + float(txt.split("/")[1])
                ) / 2


for row in rows:
    cells = row.find_all("td")
    try:
        print(cells[1].text.strip())
        print(cells[1].text.strip().split("–"))
        print(cells[1].text.strip().split("–")[0])

        congress += [
            {
                "start_year": int(cells[1].text.strip().split("–")[0]),
                "senate_democrats": parse_count(cells[3].text),
                "senate_republicans": parse_count(cells[4].text),
                "house_of_reps_democrats": parse_count(cells[8].text),
                "house_of_reps_republicans": parse_count(cells[9].text),
            }
        ]
    except Exception as e:
        print("e", e)
        print("cells", cells)

pd.DataFrame(congress).to_csv("usa/data/parsed/congress.csv")
