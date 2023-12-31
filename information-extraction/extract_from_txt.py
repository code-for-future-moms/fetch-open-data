import argparse

parser = argparse.ArgumentParser(description='Process string.')
parser.add_argument('input_path', metavar='input file path')
parser.add_argument('output_path', metavar='output file path')
args = parser.parse_args()

with open(args.input_path) as fin:
    text = "".join(fin.readlines())
# print(text)
import mojimoji
# 数字を全角から半角に
text = mojimoji.zen_to_han(text, kana=False, ascii=False)
# 小数点を全角から半角に
import re
text = re.sub(r"(?<=\d)．(?=\d)", ".", text)

# 全角/半角コンマは除去
text = re.sub(r"(?<=\d)[，,](?=\d)", "", text)
regex = re.compile(r"(?<=医療機関名：).+(?=\n)")
matches = re.findall(regex, text)
name = None
for i in matches:
    name = i.strip()

# 医療機関名：の後に改行が挟まるクリニックも
if name is None:
    m = re.search(r'(?<=医療機関名：\n).+?(?=\n)', text, flags=re.DOTALL)
    if m:
        name = m.group(0).strip()

m = re.search(r'(?<=【凍結胚を用いた治療成績】).+?(?=来院患者情報)', text, flags=re.DOTALL)
stats = []
if m:
    stats = re.findall(r'[\d.]+', m.group(0))

import csv

clinic_address = None
registernum_address = {}
with open("/Users/msasaki/Downloads/20220502.csv", newline="", encoding="shift-jis") as fin:
    reader = csv.DictReader(fin, delimiter=",", quotechar='"')
    # print(reader.fieldnames)
    for row in reader:
        registernum_address[row['指定\n番号']] = row['所在地']

input_file_wo_path = args.input_path.split("/")[-1]
registernum = input_file_wo_path.split('_')[0]
if registernum in registernum_address.keys():
    # 住所の先頭に東京都をつける
    clinic_address = "東京都{}".format(registernum_address[registernum])

with open(args.output_path, 'a', encoding="utf-8", newline='') as fout:
    writer = csv.writer(fout, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    if name is not None and len(stats) == 4 and clinic_address is not None:
        et_count = int(stats[0])
        birth_count = int(stats[2])
        birth_rate = float(stats[3])
        try:
            birth_rate2 = birth_count/et_count * 100
            if abs(birth_rate - birth_rate2) < 1:
                writer.writerow(
                    [name, stats[0], stats[1], stats[2], stats[3], clinic_address, "VALID"]
                )
            else:
                writer.writerow(
                    [name, stats[0], stats[1], stats[2], stats[3], clinic_address, "INCONSISTENT{}:{}".format(args.input_path, ','.join(stats))]
                )
        except ZeroDivisionError:
            writer.writerow(
                [name, stats[0], stats[1], stats[2], stats[3], clinic_address, "INCONSISTENT{}:{}".format(args.input_path, ','.join(stats))]
            )
    elif name is None:
        writer.writerow(["", "", "", "", "", "", "NAME_NOT_IDENTIFIED:{}".format(args.input_path)])
    elif len(stats) != 4:
        writer.writerow([name, "", "", "", "", clinic_address, "NUMBERS_NOT_EXTRACTED{}:{}".format(args.input_path, ",".join(stats))])
    elif clinic_address is None:
        writer.writerow([name, stats[0], stats[1], stats[2], stats[3], "", "ADDRESS_NOT_EXTRACTED:{}".format(args.input_path)])