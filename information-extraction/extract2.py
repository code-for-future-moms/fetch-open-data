import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_path', metavar='file path')
args = parser.parse_args()

with open(args.input_path) as fin:
    text = "".join(fin.readlines())
# print(text)
import mojimoji

text = mojimoji.zen_to_han(text, kana=False, ascii=False)
import re
regex = re.compile(r"(?<=医療機関名：).+(?=\n)")
matches = re.findall(regex, text)
name = None
for i in matches:
    name = i.strip()

m = re.search(r'(?<=【凍結胚を用いた治療成績】).+(?=来院患者情報)', text, flags=re.DOTALL)
stats = re.findall(r'[\d.]+', m.group(0))

regex =  re.compile(r"(?<=医療機関のホームページについて\n)http.+?(?=\n)")
matches = re.findall(regex, text)
clinic_url = None
for i in matches:
    clinic_url = i.strip()
    break

if name is not None and len(stats) == 4 and clinic_url is not None: 
    print("{}\t{}\t{}\t{}\t{}\t{}".format(name, stats[0], stats[1], stats[2], stats[3], clinic_url))
elif name is None:
    print("NAME_NOT_IDENTIFIED\t\t\t\t\t{}".format(args.input_path))
elif len(stats) != 4:
    print("{}\t\t\t\t\tNUMBERS_NOT_EXTRACTED{}".format(name, args.input_path))
elif clinic_url is None:
    print("{}\t{}\t{}\t{}\t{}\tURL_NOTEXTRACTED{}".format(name, stats[0], stats[1], stats[2], stats[3], args.input_path))
exit(1)

import requests

regex_address =  re.compile(r"(?<=〒)\d\d\d-\d\d\d\d")
with requests.session() as s:
    response = s.get(clinic_url)
    response.encoding = response.apparent_encoding
    scraped_text = response.text
    # print(scraped_text)
    matches = re.findall(regex_address, scraped_text)
    print(matches)