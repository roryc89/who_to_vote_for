from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

# found at https://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_the_United_Kingdom#Since_1721"
# it was far easier to copy these than parse the html

govs = [
    {"month": 10, "year": 1959, "party": "Conservative"},
    {"month": 10, "year": 1964, "party": "Labour"},
    {"month": 3, "year": 1966, "party": "Labour"},
    {"month": 6, "year": 1970, "party": "Conservative"},
    {"month": 2, "year": 1974, "party": "Labour"},
    {"month": 10, "year": 1974, "party": "Labour"},
    {"month": 5, "year": 1979, "party": "Conservative"},
    {"month": 6, "year": 1983, "party": "Conservative"},
    {"month": 6, "year": 1987, "party": "Conservative"},
    {"month": 4, "year": 1992, "party": "Conservative"},
    {"month": 5, "year": 1997, "party": "Labour"},
    {"month": 6, "year": 2001, "party": "Labour"},
    {"month": 5, "year": 2005, "party": "Labour"},
    {"month": 5, "year": 2010, "party": "Conservative"},
    {"month": 5, "year": 2015, "party": "Conservative"},
    {"month": 6, "year": 2017, "party": "Conservative"},
]

pd.DataFrame(govs).to_csv("uk/data/parsed/govs.csv")
