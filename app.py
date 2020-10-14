
import oddsportal
from bs4 import BeautifulSoup
import pandas as pd

for starting_year in range(2011, 2020):
    print(">> starting year: " + str(starting_year))
    match_urls = oddsportal.return_soccer_url(starting_year, show_window=False)
    number_of_matches = len(match_urls)
    for i, match_url in enumerate(match_urls):
        print(f"> {starting_year}:{i:02}/{number_of_matches:02}\n> match url: " + match_url)
        html = oddsportal.fetch_odds_html(url=match_url,  # cs;2;1 will have the 0:0 odds enabled
                                          show_window=False,
                                          save=False)

        soup = BeautifulSoup(html, "html.parser")
        odds_store = oddsportal.get_odds_by_exchange(soup) if oddsportal.get_odds_by_exchange(soup) else \
            print("> match does not contain required info. Skipping.")

        if not odds_store:
            continue

        if 'reference_table' in locals():  # check if the variable exists in the local scope
            additional_observation = pd.DataFrame.from_dict(odds_store).T
            additional_observation['match_details'] = soup.title.string

            reference_table = pd.concat([reference_table, additional_observation])

        else:
            reference_table = pd.DataFrame.from_dict(odds_store).T
            reference_table['match_details'] = soup.title.string
            reference_table.index.name = 'Exchanges'

    reference_table.to_csv(f'./premier-league-{str(starting_year)}.csv')
