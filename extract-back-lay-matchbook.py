import requests
from bs4 import BeautifulSoup
import re
from typing import Dict
import pandas as pd

soup = BeautifulSoup(open("html_page.html"), "html.parser")

odds_store: Dict = {}

betting_exchanges_table = soup.find_all("table", class_="table-main detail-odds sortable")[1]
for cell in betting_exchanges_table("td", class_=re.compile("(center|odds)")):
    if 'colspan' in cell.attrs:
        break
    if cell.string == None:
            if 'Back' in odds_store and odds_store['Back'] is None:
                odds_store['Back'] = cell.div.contents[0]
            elif 'Lay' in odds_store and odds_store['Lay'] is None:
                odds_store['Lay'] = cell.div.contents[0]
            else:
                print(cell.div.contents)
                print('*************', end='\n\n')
            continue
    if cell.string == 'Back' or cell.string == 'Lay':
        odds_store[cell.string] = None

odds_store_df = pd.DataFrame(data=odds_store, index=[soup.title.string])


