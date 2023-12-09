from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

req = Request('https://funin-fuiku.cfa.go.jp/clinic/search/modal.php?id=470', headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()

soup = BeautifulSoup(html_page, 'lxml', from_encoding="utf-8")
block = soup.div.div.div
clinic_name = block.find(class_="name").text
address = block.find(class_="address").text
phone_number = block.find(class_="tel").text
pref = block.find(class_="area").text
print("{}\t{}\t{}\t{}".format(clinic_name, address, pref, phone_number))
