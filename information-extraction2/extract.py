from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import argparse

parser = argparse.ArgumentParser(description='Parse given URL')
parser.add_argument('url', type=str, help='URL to be parsed')

args = parser.parse_args()

req = Request(args.url, headers={'User-Agent': 'Mozilla'})
html_page = urlopen(req, timeout=2).read() # timeout指定しないと時間がかかりすぎる

soup = BeautifulSoup(html_page, 'lxml', from_encoding="utf-8")

# 医療機関の基礎情報
block = soup.div.div.div
clinic_name = block.find(class_="name").text
address = block.find(class_="address").text
phone_number = block.find(class_="tel").text
pref = block.find(class_="area").text
clinic_url = block.find(class_="site").find("a")["href"] if block.find(class_="site") is not None else "" # Noneの可能性も
# どんな治療内容を提供しているかスクレイピング
treatments_ele = soup.find("h2", string="治療内容")
tbl = treatments_ele.parent.find('table')
table_body = tbl.find('tbody')
rows = table_body.find_all('tr')
treatments_flag = dict()
for row in rows:
    treatment_name = row.find("th").string.strip()
    src_fname = row.find("td").find("img")["src"].strip().split("/")[-1]
    if src_fname == "passable.svg":
        flag_offer = True
    elif src_fname == "unpassable.svg":
        flag_offer = False
    treatments_flag[treatment_name] = flag_offer
# 体外受精の治療成績をスクレイピング
stats_tbl = soup.find("h3", string="【凍結胚を用いた治療成績】").parent.find("table")
rows = stats_tbl.find("tbody").find_all("tr")
frozen_stats = dict()
for row in rows:
    count_name = row.find("th").string.strip()
    parsed_val = int(row.find("td").string)
    frozen_stats[count_name] = parsed_val
print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(clinic_name, address,pref, phone_number,
                                                                              treatments_flag["人工授精"], treatments_flag["採卵術"], treatments_flag["体外受精"], treatments_flag["顕微授精"],
                                                                              treatments_flag["新鮮胚移植"], treatments_flag["凍結・融解胚移植"], treatments_flag["精巣内精子採取術"], treatments_flag["顕微鏡下精巣内精子採取術"],
                                                                              frozen_stats["採卵総回数（回）"], frozen_stats["妊娠数（回）"],
                                                                              frozen_stats["生産分娩数（回）"], frozen_stats["移植あたり生産率（%）"], clinic_url))
