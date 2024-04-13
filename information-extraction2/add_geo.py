import argparse
import csv
import json
import time
import urllib.request

# 国土地理院API
# 参考: https://elsammit-beginnerblg.hatenablog.com/entry/2021/07/11/122916
url_base = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

parser = argparse.ArgumentParser(description='Parse given URL')
parser.add_argument('input', type=str, help='input file name')

args = parser.parse_args()

with open(args.input, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    header = next(reader)
    header.append("longitude")
    header.append("latitude")
    print("\t".join(header))
    for row in reader:
        full_url = url_base + urllib.parse.quote(row[1])
        req = urllib.request.Request(full_url)
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36")
        with urllib.request.urlopen(req) as response:
            tmp = response.read().decode('utf-8')
            data = json.loads(tmp)
            long = str(data[0]['geometry']['coordinates'][0])
            lat = str(data[0]['geometry']['coordinates'][1])
            row.append(long)
            row.append(lat)
            print("\t".join(row))
            time.sleep(10)