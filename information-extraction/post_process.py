import argparse

parser = argparse.ArgumentParser(description='Process files to include sub-address.')
parser.add_argument('input_path', metavar='input file path')
parser.add_argument('output_path', metavar='output file path')
args = parser.parse_args()

import csv
import re

fout = open(args.output_path, 'w', encoding="utf-8", newline='')
writer = csv.writer(fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
writer.writerow(
    [
        "name",
        "et_count",
        "preg_count",
        "birth_count",
        "birth_ratio",
        "address",
        "sub_address",
        "pref"
    ]
)

with open(args.input_path, newline="", encoding="utf-8") as fin:
    reader = csv.DictReader(fin, delimiter="\t", quotechar='"')
    for row in reader:
        address = row["address"]
        address_wo_pref = address.replace("東京都", "")

        regex = re.compile(r"^.+?[市区町村](?=.+)")
        matches = re.findall(regex, address_wo_pref)
        city = None
        for i in matches:
            city = i.strip()
        writer.writerow([row["name"], row["et_count"], row["preg_count"], row["birth_count"], row["birth_ratio"], row["address"], city, "東京都"])


fout.close()
