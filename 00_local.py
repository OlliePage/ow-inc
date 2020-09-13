import requests
from bs4 import BeautifulSoup

with open('scratch.html') as file:
    soup = BeautifulSoup(file)

html_doc = soup.prettify()

print(html_doc)

for string in soup.strings:
    print(repr(string))

target_odds = soup.find(text='31/2')

print([parent.name for parent in target_odds.parents])

