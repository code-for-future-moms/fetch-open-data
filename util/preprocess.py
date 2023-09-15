from collections import defaultdict
city_count = defaultdict(int)

with open("tokyo-code.tsv") as fin:
    lines = fin.readlines()

with open("../data/hospital-data-address2-R40620.tsv") as fin:
    for l in fin.readlines():
        city = l.strip().split("\t")[6]
        if not city.startswith("sub_"):
            city_count[city] += 1

for l in lines[1:]:
    flds = l.strip().split("\t")
    if flds[2] in city_count.keys():
        print('      <li><input type="checkbox" name="ar" value="{1}" id="{0}" class="checkbox-item"><label for="{0}">{1} ({2})</label></li>'.format(flds[0][:-1], flds[2], city_count[flds[2]]))