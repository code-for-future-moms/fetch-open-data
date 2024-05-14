from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_hospital_id(url, ids):
    req = Request(url, headers={'User-Agent': 'Mozilla'})
    html_page = urlopen(req, timeout=2).read()
    soup = BeautifulSoup(html_page, 'lxml', from_encoding="utf-8")

    for a in soup.find_all('a', href=True):
        if a["href"].startswith("/clinic/search/modal.php?id="):
            raw_id = a["href"].replace("/clinic/search/modal.php?id=", "")
            ids.add(raw_id)

def get_page_url(url, urls_page):
    req = Request(url, headers={'User-Agent': 'Mozilla'})
    html_page = urlopen(req, timeout=2).read()
    soup = BeautifulSoup(html_page, 'lxml', from_encoding="utf-8")

    for a in soup.find_all('a', href=True):
        if a["href"].startswith(url + "&page="):
            urls_page.add(a["href"])

print('printf "name\taddress\tprefecture\tphone\tflag1\tflag2\tflag3\tflag4\tflag5\tflag6\tflat7\tflag8\tfrozen_egg\tfrozen_preg\tfrozen_birth\tfrozen_rate\tclinic_url\n"')
for i in range(47):
    url = "https://funin-fuiku.cfa.go.jp/clinic/search/?area%5B%5D={}".format(i)
    ids = set()
    urls_page = set()
    get_page_url(url, urls_page)
    # urls_pageはすべてのページを含んでいるわけではない 東京都の場合 最初のページから2, 3, 6ページ目までのリンクしか得られない
    last_page = -1
    for url_with_page in urls_page:
        page_num = int(url_with_page.split("&page=")[1])
        if page_num > last_page:
            last_page = page_num
    # 途中のページを埋める
    for i in range(1, last_page + 1):
        urls_page.add(url + "&page=" + str(i))
    for url_with_page in urls_page:
        get_hospital_id(url_with_page, ids)
    if not urls_page: # 1ページしかないなら
        get_hospital_id(url, ids)
    for id in ids:
        print("python ./information-extraction2/extract.py https://funin-fuiku.cfa.go.jp/clinic/search/modal.php?id={}".format(id))
