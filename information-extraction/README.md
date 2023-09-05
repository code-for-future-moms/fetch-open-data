# information extraction
- PDFファイルの取得
```sh
wget -r -l 1 -nH -nd -np --ignore-case -A '*.pdf' https://www.fukushi.metro.tokyo.lg.jp/kodomo//kosodate/josei/funin/shiteiiryou-jouhoukoukai.html -P mydir
```
- 情報の抽出