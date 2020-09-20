from webbot import Browser
from stringcase import snakecase


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


def fetch_odds(url, show_window=True, save=False):
    """
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



