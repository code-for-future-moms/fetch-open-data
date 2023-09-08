# information extraction

## 最終的に得られたデータ
- [hospital-data-address-R40620.tsv](https://github.com/code-for-future-moms/fetch-open-data/blob/main/data/hospital-data-address-R40620.tsv)

## 前準備
- 必要なライブラリのインストール
```commandline
brew install poppler
pip install mojimoji
```

## 作業手順
- PDFファイルの取得と`mydir`への配置
```sh
wget -r -l 1 -nH -nd -np --ignore-case -A '*.pdf' https://www.fukushi.metro.tokyo.lg.jp/kodomo//kosodate/josei/funin/shiteiiryou-jouhoukoukai.html -P mydir
```
- 都内の医療機関の住所を得るためのデータソース
  - https://www.fukushi.metro.tokyo.lg.jp/kodomo//kosodate/josei/funin/si_list.html からcsvをダウンロード
  - このファイル中の"指定番号"はPDFファイルの先頭の番号と対応しているのでこれを用いて住所の情報を得る
- 情報の抽出
  1. Poppler実行
  1. テキストファイルから正規表現を用いて各種統計値を抽出・ファイルに出力
  1. 正規表現では取りきれないので人力でレビュー・修正
```commandline
python run_poppler.py
python create_output.py
```