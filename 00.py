import requests
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open("html_page.html"), "html.parser")

betting_exchanges_table = soup.find_all("table", class_="table-main detail-odds sortable")[1]

betting_exchanges_table.find_all("td") # 1, 2, 4, 5
back_odds = betting_exchanges_table("td")[2]
print(back_odds.div.contents)

#regex for center or odds in class

re.compile("(center|odds)")

betting_exchanges_table("td", class_=re.compile("(center|odds)"))

for cell in betting_exchanges_table("td", class_=re.compile("(center|odds)")):
    # print(cell)
    if 'colspan' in cell.attrs:
        break
    if cell.string == None:
        print(cell.div.contents)
        print('*************', end='\n\n')
        continue
    print(cell.string)

    print('*************', end='\n\n')


