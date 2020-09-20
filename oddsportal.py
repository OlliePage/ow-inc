from webbot import Browser
from stringcase import snakecase
from typing import List, NewType, Dict
from bs4 import BeautifulSoup
import re

ResultSet = NewType('ResultSet', List)
NavigableString = NewType('NavigableString', str)


def login_oddsportal(url, show_window=True, save=False, chained_webbot=False):
    """
    :param url: the url to pass in to webbot to return to after logging in
    :param show_window: open and navigate through the GUI
    :param save: save the html in the session to file under 'test.html'
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
    driver.go_to(url)
    if chained_webbot:
        return driver

    html = driver.get_page_source()
    page_title = snakecase(driver.get_title())

    driver.close_current_tab()
    if save:
        with open(f'{page_title}.html', "w") as file:
            file.write(html)
    return html


def return_soccer_url() -> List:
    """
    fetch all the urls from the results page, and filter the results to just the urls that pertain to football matches

    :return: (list)
    """
    html = login_oddsportal(url='https://www.oddsportal.com/soccer/england/premier-league/results/',
                            show_window=False,
                            save=True)

    soup = BeautifulSoup(html, "html.parser")

    # fetch all the urls from the given page, then filter down to just the urls that pertain to football matches
    raw_hrefs = soup.find_all(href=re.compile('/soccer/england/premier-league/[a-z]'))
    raw_url = [ref['href'] for ref in raw_hrefs]
    soccer_href_matches_url = [f'https://www.oddsportal.com/{s}' for s in raw_url if
                               not any(xs in s for xs in ['results', 'standings', 'outrights'])]
    return soccer_href_matches_url


def fetch_odds_html(url, show_window=True, save=False):
    """
    returns the html of the given page on the 0:0 correct score odds

    :param url: the url to pass in to webbot to return to after logging in
    :param show_window: open and navigate through the GUI
    :param save: save the html in the session to file under 'test.html'
    :return: html of saved odds page
    """
    driver = login_oddsportal(url, show_window, save, chained_webbot=True)
    driver.scrolly(800)
    driver.click('0:0')
    html = driver.get_page_source()
    page_title = snakecase(driver.get_title())
    page_title = page_title.replace('/', '_')
    driver.close_current_tab()
    if save:
        with open(f'{page_title}.html', "w") as file:
            file.write(html)

    return html


def split_exchanges_html(soup) -> Dict:
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


def get_odds_by_exchange(soup) -> Dict[str, Dict[str, str]]:
    """
    Iterates through the split_exchanges_html dict and extracts the 'Back' and 'Lay' odds for every exchange present
    and returns it in a dictionary

    :param soup: BeautifulSoup object that has parsed the oddsportal html
    :return: (dict) Booking Exchanges and their respective Back & Lay odds
    """
    exchange_dict = split_exchanges_html(soup)
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



