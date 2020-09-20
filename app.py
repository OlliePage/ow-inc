import oddsportal
from bs4 import BeautifulSoup
import pandas as pd

match_urls = oddsportal.return_soccer_url()

for match_url in match_urls:
    html = oddsportal.fetch_odds_html(url=match_url+'#cs;2;1',   # cs;2;1 will have the 0:0 odds enabled
                                                  show_window=False,
                                                  save=True)

    soup = BeautifulSoup(html, "html.parser")
    odds_store = oddsportal.get_odds_by_exchange(soup)

    if 'reference_table' in locals():   # check if the variable exists in the local scope
        additional_observation = pd.DataFrame.from_dict(odds_store).T
        additional_observation['match_details'] = soup.title

        reference_table = pd.concat([reference_table, additional_observation])

    else:
        reference_table = pd.DataFrame.from_dict(odds_store).T
        reference_table['match_details'] = soup.title
        reference_table.index.name = 'Exchanges'