import csv
import json
import urllib.request

# 国土地理院API
# 参考: https://elsammit-beginnerblg.hatenablog.com/entry/2021/07/11/122916
url_base = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
with open('../data/cfa-20231213.tsv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    header = next(reader)
    header.append("longitude")
    header.append("latitude")
    print("\t".join(header))
    for row in reader:
        full_url = url_base + urllib.parse.quote(row[1])
        with urllib.request.urlopen(full_url) as response:
            tmp = response.read().decode('utf-8')
            data = json.loads(tmp)
            long = str(data[0]['geometry']['coordinates'][0])
            lat = str(data[0]['geometry']['coordinates'][1])
            row.append(long)
            row.append(lat)
            print("\t".join(row))
