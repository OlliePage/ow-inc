# this script will fetch all the game urls given a league, year-year. Feeding this info into
# 'extract-back-lay-single-page' to generate a df, which is then concatted to one another to create a master df

from oddsportal import login_oddsportal
from bs4 import BeautifulSoup
import pprint
import re

html = login_oddsportal(url='https://www.oddsportal.com/soccer/england/premier-league/results/',
                        show_window=False,
                        save=True)

soup = BeautifulSoup(html, "html.parser")

# fetch all the urls from the given page, then filter down to just the urls that pertain to football matches
raw_hrefs = soup.find_all(href=re.compile('/soccer/england/premier-league/[a-z]'))
raw_url = [ref['href'] for ref in raw_hrefs]
soccer_href_matches_url = [f'https://www.oddsportal.com/{s}' for s in raw_url if not any(xs in s for xs in ['results', 'standings', 'outrights'])]

