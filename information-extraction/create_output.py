import os
import subprocess

directory = "./text"
medium_file = "hospital-auto.tsv" # not final. requires manual review
subprocess.run(["rm", medium_file])

import csv

with open(medium_file, 'w', encoding="utf-8", newline='') as fout:
    writer = csv.writer(fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["name", "et_count", "preg_count", "birth_count", "birth_ratio", "url", "log"])
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    subprocess.run(["python", "extract_from_txt.py", f, medium_file])