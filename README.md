# fetch-open-data
PDFからの情報抽出やGitHub Actionsなどを試すrepo

## 東京都の公開しているPDFからの情報抽出
- [information-extraction](https://github.com/code-for-future-moms/fetch-open-data/tree/main/information-extraction) 参照

## ~~PDFからの情報抽出のテスト~~
- __pdfminer.sixではなくPopplerを利用することにしたため以下の内容は古く参考にしなくてよい__
- サンプルPDFの入手
  - [東京都特定不妊治療費助成事業指定医療機関の情報公開（2020年1月から12月分）](https://www.fukushi.metro.tokyo.lg.jp/kodomo//kosodate/josei/funin/shiteiiryou-jouhoukoukai.html) から好きな医療機関のPDFをダウンロード
  - 以下の例では`1_R4_hamada.pdf`をダウンロードしたと仮定して説明
- pdfminer.sixのインストール
```
pip install pdfminer.six
```
- 情報抽出のテスト
```python
from pdfminer.high_level import extract_text
text = extract_text('1_R4_hamada.pdf')
import re
m = re.search(r'(?<=【凍結胚を用いた治療成績】).+(?=来院患者情報)', text, flags=re.DOTALL)
# `m.group(0)`にPDFではテーブルになっている凍結胚を用いた治療の成績データが含まれる
# ' \n\n融解胚子宮内移植 \n\n131 \n移植総回数（回） \n22 \n妊娠数（回） \n13 \n生産分娩数（回） \n移植あたり生産率（%）  9.9 \n\n'
# `m2 = re.findall(r'[\d.]+', m.group(0))`で可視化する実際の数値を得る
# ['131', '22', '13', '9.9']
```