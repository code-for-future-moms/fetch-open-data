import argparse
import csv
import json
import time
import urllib.request

import xml.etree.ElementTree as ET

# シンプルジオコーディング実験を利用
# 参考: https://geocode.csis.u-tokyo.ac.jp/home/simple-geocoding/
url_base = "https://geocode.csis.u-tokyo.ac.jp/cgi-bin/simple_geocode.cgi?charset=UTF8&addr="

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
            root = ET.fromstring(tmp)
            # 複数候補が返ってくることがあるから一つ目だけ採用
            first_candidate = root.find('candidate')
            long = first_candidate.find("longitude").text
            lat = first_candidate.find("latitude").text
            row.append(long)
            row.append(lat)
            print("\t".join(row))
            time.sleep(0.3)