from webbot import Browser
from stringcase import snakecase
from typing import List, NewType, Dict
from bs4 import BeautifulSoup
import re
from datetime import date
import numpy as np

ResultSet = NewType('ResultSet', List)
NavigableString = NewType('NavigableString', str)


def login_oddsportal(url, show_window):
    """
    :param url: the url to pass in to webbot to return to after logging in
    :param show_window: open and navigate through the GUI
    :param save: save the html in the session to file
    :param chained_webbot:  (bool) whether this function is used in a continuing webbot session
    :return: html or driver (depending on whether chained_webbot is True/False)
    """

    driver = Browser(showWindow=show_window)
    driver.go_to(url)
    driver.click('Login', tag='button', classname='inline-btn-2')
    driver.click(tag='input', classname='int-text', id='login-username1')
    driver.type('offers15816')
    driver.click(tag='input', classname='int-text', id='login-password1')
    driver.type('8simpsons8')
    driver.click('Login', tag='button', classname="inline-btn-2", number=3)
    return driver


def return_soccer_url(starting_year: int, show_window: bool) -> List:
    """
    fetch all the urls from the results page, and filter the results to just the urls that pertain to football matches

    :return: (list)
    """
    if starting_year == date.today().year:
        odds_portal_url = 'https://www.oddsportal.com/soccer/england/premier-league/results/'
    else:
        odds_portal_url = f'https://www.oddsportal.com/soccer/england/premier-league-{str(starting_year)}-{str(starting_year+1)}/results/'

    driver = login_oddsportal(url=odds_portal_url,
                            show_window=show_window)

    driver.go_to(odds_portal_url)
    html = driver.get_page_source()
    # driver.close_current_tab()

    soup = BeautifulSoup(html, "html.parser")

    # fetch all the urls from the given page, then filter down to just the urls that pertain to football matches

    if starting_year == date.today().year:
        regex_pattern = '/soccer/england/premier-league/[a-z]'
    else:
        regex_pattern = f"/soccer/england/premier-league-{str(starting_year)}-{str(starting_year+1)}/[a-z]"

    raw_hrefs = soup.find_all(href=re.compile(regex_pattern))
    raw_url = [ref['href'] for ref in raw_hrefs]
    soccer_href_matches_url = [f'https://www.oddsportal.com/{s}#cs;2;1' for s in raw_url if
                               not any(xs in s for xs in ['results', 'standings', 'outrights'])]
    return soccer_href_matches_url


def fetch_odds_html(url, show_window, save):
    """
    returns the html of the given page on the 0:0 correct score odds

    :param url: the url to pass in to webbot to return to after logging in
    :param show_window: open and navigate through the GUI
    :param save: save the html in the session to local directory file
    :return: html of saved odds page
    """
    driver = login_oddsportal(url, show_window)
    driver.scrolly(800)
    driver.click('0:0')
    html = driver.get_page_source()
    page_title = snakecase(driver.get_title()).replace('/', '_')
    # driver.close_current_tab()
    if save:
        with open(f'{page_title}.html', "w") as file:
            file.write(html)

    return html


def split_exchanges_html(soup) -> Dict:


    if not soup.find_all("div", class_='exchangeDivider', text='BETTING EXCHANGES'):
        print('> Webpage has no betting exchanges section')
        return None

    betting_exchanges_table = soup.find_all("table", class_="table-main detail-odds sortable")[1]

    count_of_correct_score_tables_on_page = soup.find_all('div', class_='table-header-light even')
    if not count_of_correct_score_tables_on_page:
        print('> webpage has no correct score section')
        return None

    exchange_location = [x for x in [betting_exchanges_table.find_all(class_='name', href=re.compile(exchange))
                         for exchange in ['matchbook', 'betfair']] if x]

    exchange_dict = {result_set[0].string: result_set for result_set in exchange_location}
    return exchange_dict


# place the html for the matchbook row and the betfair row in separate elements in a list
def get_odds_by_exchange(soup) -> Dict[str, Dict[str, str]]:
    """
    Iterates through the split_exchanges_html dict and extracts the 'Back' and 'Lay' odds for every exchange present.

    :param soup: BeautifulSoup object that has parsed the oddsportal html
    :return: (dict) Booking Exchanges and their respective Back & Lay odds
    """
    exchange_dict = split_exchanges_html(soup)
    assert(exchange_dict), 'exchange_dict is empty'

    navigable_string = [k for k, _ in exchange_dict.items()][0]
    match_title = [parent.title.string for parent in navigable_string.parents if parent.title is not None][0]
    print(f'> match_title: {match_title}')

    betting_exchanges_table = soup.find_all("table", class_="table-main detail-odds sortable")[1]

    odd_class = betting_exchanges_table.find("tbody").find_all("tr", class_="odd")

    odds_store: Dict[str, Dict[str, str]] = {} # {'exchange_name': {'Back': [odds], 'Lay': [odds]}}
    for row in odd_class:
        exchange_name = row.find('a', class_='name').string
        odds_store[exchange_name] = {"Back": None}
        back_divs = row.find_all('div')
        back_odds = [div.contents[0] for div in back_divs if 'onmouseout' in div.attrs]
        odds_store[exchange_name]["Back"] = back_odds

        layrow = row.next_sibling
        lay_divs = layrow.find_all('div')
        lay_odds = [div.contents[0] for div in lay_divs if 'onmouseout' in div.attrs]
        odds_store[exchange_name]["Lay"] = lay_odds

    return odds_store



