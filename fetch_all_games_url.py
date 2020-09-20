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

pprint.pprint(soup.find_all(href=re.compile('/soccer/england/premier-league')))