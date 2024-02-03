import csv
import math

national_ave = 26.6 # 凍結胚の移植あたり出生率(%)

with open('../data/cfa-20231213v2.tsv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    header = next(reader)
    header.append("icon")
    print("\t".join(header))
    for row in reader:
        num_transfers = int(row[12])
        num_births = int(row[14])
        if num_transfers == 0 and num_births == 0:
            icon = "N/A"
        else:
            frac_births = float(num_births)/num_transfers
            reliability_range = 1.96 * math.sqrt((num_transfers - num_births) * frac_births * frac_births + num_births * (1 - frac_births) * (1 - frac_births))/num_transfers
            frac_births_per = frac_births * 100
            reliability_range_per = reliability_range * 100
            if frac_births_per - reliability_range_per > national_ave:
                icon = "better"
            elif frac_births_per + reliability_range_per < national_ave:
                icon = "worse"
            else:
                icon = "consistent"
        row.append(icon)
        print("\t".join(row))