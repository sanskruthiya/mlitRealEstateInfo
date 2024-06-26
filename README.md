# 不動産情報ライブラリAPIデータ取得スクリプト

国土交通省が提供している不動産情報ライブラリAPIからデータ取得するPythonスクリプトです。
「Script」内のLoader_MlitRealEstateInfo.pyがスクリプト本体になります。
このAPIを利用するには、事前にAPIキーの取得申請を行う必要があります。詳細は下記の公式リンクからご確認ください。

- 不動産情報ライブラリ：[リンク](https://www.reinfolib.mlit.go.jp/)
- 不動産情報ライブラリAPIマニュアル：[リンク](https://www.reinfolib.mlit.go.jp/help/apiManual/)

### 補足説明

- 最初の api_type = "XIT001" と mlit_params = {"year": "2021", "area": "12"} の部分はそれぞれ対象データの種類とそれに応じたパラメータなので、ここを取得したいデータに応じて書き換えることで、このAPIが提供する様々なデータにアクセスできます
- 注意点として、例えばパラメータのyearにデータがない直近年などを入れるとエラーが返されたりします。パラメータの適正な範囲と、各データ種類における必須パラメータについては、公式マニュアルの記載に従ってください
- 出力結果はGeoJSONで得られるものやJSONで取得するものがあります。JSON形式のレスポンスに関してはCSVのほうが使いやすいケースもあると思うので、 選択式でCSV形式の出力にも対応しました。ただし、PBFはバイナリファイルなので非対応としています。パラメータでPBFを出力形式に指定してもGeoJSONで出力します
