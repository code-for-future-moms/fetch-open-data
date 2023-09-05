from pdfminer.high_level import extract_text
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_path', metavar='file path')
args = parser.parse_args()

text = extract_text(args.input_path)
print(text)
import re
m = re.search(r'(?<=【凍結胚を用いた治療成績】).+(?=来院患者情報)', text, flags=re.DOTALL)
stats = re.findall(r'[\d.]+', m.group(0))
print(stats)

regex =  re.compile(r"(?<=\n\n)http.+?(?= \n\n医療機関のホームページについて)")
matches = re.findall(regex, text)
clinic_url = None
for i in matches:
    clinic_url = i
    break
print(clinic_url)

import requests

regex_address =  re.compile(r"(?<=〒)\d\d\d-\d\d\d\d")
with requests.session() as s:
    response = s.get(clinic_url)
    response.encoding = response.apparent_encoding
    scraped_text = response.text
    print(scraped_text)
    matches = re.findall(regex_address, scraped_text)
    print(matches)
