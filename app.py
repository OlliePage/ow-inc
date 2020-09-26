#todo need to handle multiple pages of results (8 pages)

import oddsportal
from bs4 import BeautifulSoup
import pandas as pd

for starting_year in range(2015, 2020):
    print(">> starting year:" + str(starting_year))
    match_urls = oddsportal.return_soccer_url(starting_year, show_window=False)

    for match_url in match_urls:
        print("> match url: " + match_url)
        html = oddsportal.fetch_odds_html(url=match_url,   # cs;2;1 will have the 0:0 odds enabled
                                          show_window=False,
                                          save=True)

        soup = BeautifulSoup(html, "html.parser")
        odds_store = oddsportal.get_odds_by_exchange(soup)
        if not odds_store:
            print("> webpage doesn't contain required info. Skipping.")
            continue

        if 'reference_table' in locals():   # check if the variable exists in the local scope
            additional_observation = pd.DataFrame.from_dict(odds_store).T
            additional_observation['match_details'] = soup.title.string

            reference_table = pd.concat([reference_table, additional_observation])

        else:
            reference_table = pd.DataFrame.from_dict(odds_store).T
            reference_table['match_details'] = soup.title.string
            reference_table.index.name = 'Exchanges'