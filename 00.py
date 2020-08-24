import requests
from bs4 import BeautifulSoup 

import urllib.request

url = urllib.request.urlopen('https://www.oddsportal.com/soccer/england/premier-league-2019-2020/arsenal-watford-2JDks1o7/')

print(url.getcode())

html = url.read()

soup = BeautifulSoup(html)

print(soup.find_all(text='BETTING'))
