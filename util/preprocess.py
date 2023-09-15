with open("tokyo-code.tsv") as fin:
    lines = fin.readlines()

exists_city = list()
with open("../data/hospital-data-address2-R40620.tsv") as fin:
    for l in fin.readlines():
        city = l.strip().split("\t")[6]
        if not city.startswith("sub_"):
            exists_city.append(city)

for l in lines[1:]:
    flds = l.strip().split("\t")
    if flds[2] in exists_city:
        print('      <li><input type="checkbox" name="ar" value="{1}" id="{0}" class="checkbox-item"><label for="{0}">{1}</label></li>'.format(flds[0][:-1], flds[2]))