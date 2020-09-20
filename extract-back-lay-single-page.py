import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, NewType
import pandas as pd
from oddsportal import fetch_odds

ResultSet = NewType('ResultSet', List)
NavigableString = NewType('NavigableString', str)

html = fetch_odds(url='https://www.oddsportal.com/soccer/england/premier-league-2019-2020/arsenal-watford-2JDks1o7/#cs;2;1',
                  show_window=False,
                  save=True)

soup = BeautifulSoup(html, "html.parser")


def split_exchanges_html() -> Dict:
    betting_exchanges_table = soup.find_all("table", class_="table-main detail-odds sortable")[1]
    exchange_location: List[List] = [betting_exchanges_table.find_all(class_='name', href=re.compile(exchange)) for
                                     exchange in ['matchbook', 'betfair']]
    exchange_dict: Dict[NavigableString, List[ResultSet]] = {}
    for i, v in enumerate(exchange_location):
        try:
            exchange_brand = v[0].string  # this evaluates to 'matchbook' or 'betfair'
            exchange_dict[exchange_brand] = v
        except IndexError:
            print('no more exchanges present in list')
            continue
    return exchange_dict

# place the html for the matchbook row and the betfair row in separate elements in a list


def get_odds_by_exchange() -> Dict[str, Dict[str, str]]:
    exchange_dict = split_exchanges_html()
    odds_store: Dict[str, Dict[str, str]] = {}
    for k, v in exchange_dict.items():
        odds_store[str(k)] = {}
        parent_row = k.parent.parent.parent.parent.parent

        for cell in parent_row.find_all("td", class_=re.compile("(center|right odds)")):
            if 'colspan' in cell.attrs:
                break
            if not cell.string:
                if 'Back' in odds_store[str(k)] and odds_store[str(k)]['Back'] is None:
                    odds_store[str(k)]['Back'] = cell.div.contents[0]
                elif 'Lay' in odds_store[str(k)] and odds_store[str(k)]['Lay'] is None:
                    odds_store[str(k)]['Lay'] = cell.div.contents[0]
                else:
                    print('> Unhandled output:')
                    print(cell.div.contents)
                    print('*************', end='\n\n')
                continue
            if cell.string == 'Back' or cell.string == 'Lay':
                odds_store[str(k)][cell.string] = None

    return odds_store


odds_store = get_odds_by_exchange()

reference_table = pd.DataFrame.from_dict(odds_store).T
reference_table.index.name = 'Exchanges'
reference_table['match_details'] = soup.title



