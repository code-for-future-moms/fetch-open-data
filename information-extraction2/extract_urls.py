from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_hrefs(url, ids):
    req = Request(url, headers={'User-Agent': 'Mozilla'})
    html_page = urlopen(req, timeout=2).read()
    soup = BeautifulSoup(html_page, 'lxml', from_encoding="utf-8")

    for a in soup.find_all('a', href=True):
        if a["href"].startswith("/clinic/search/modal.php?id="):
            raw_id = a["href"].replace("/clinic/search/modal.php?id=", "")
            ids.add(raw_id)
        elif a["href"].startswith(url + "&page="):
            get_hrefs(a["href"], ids)


for i in range(47):
    url = "https://funin-fuiku.cfa.go.jp/clinic/search/?area%5B%5D={}".format(i)
    ids = set()
    get_hrefs(url, ids)
    for id in ids:
        print("python extract.py https://funin-fuiku.cfa.go.jp/clinic/search/modal.php?id={}".format(id))

