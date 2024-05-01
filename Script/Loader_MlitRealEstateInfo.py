import requests
import gzip
import json
import csv

base_url = "https://www.reinfolib.mlit.go.jp/ex-api/external/" #ベースURL
api_type = "XIT001" #APIの種類を記入。後の出力ファイル名にも反映させるため変数として格納しておく。

mlit_url = base_url + api_type #リクエスト用URL
mlit_params = {"year": "2021", "area": "12"} #パラメータの設定"response_format": "geojson", "z": "13", "x": "7280", "y": "3219", "from": "20223", "to": "20234"

mlit_key = input("Input your API key: ") #コマンドライン上でAPIキーの入力を求める
mlit_headers = {"Ocp-Apim-Subscription-Key": mlit_key, "Accept-Encoding": "gzip"} #APIキーをリクエストヘッダー用に格納する。gzipのレスポンスを許可する。

response = requests.get(mlit_url, headers=mlit_headers, params=mlit_params) #APIへリクエストを投げて、結果を変数に格納する

#APIからの応答に成功した場合の処理
if response.status_code == 200:
    #Content-Encodingヘッダーを確認してgzip形式であるかどうかを判断する
    if response.headers.get('Content-Encoding') == 'gzip':
        print("Response data is gzip encoded.")
        #gzip形式の場合は中身の解凍を試行する
        try:
            decoded_data = gzip.decompress(response.content) #gzipを解凍
            json_data = json.loads(decoded_data) #解凍したデータを格納
        except Exception as e:
            print("Error decoding gzip content:", e)
            json_data = response.json() #gzipの解凍にエラーが生じた場合は、レスポンス内容をそのままJSON形式で格納
    else:
        print("Response data is not gzip encoded.")
        json_data = response.json() #gzip形式でなければ、レスポンス内容をそのままJSON形式で格納
            
    #URLパラメータにおけるデータ形式の指定の仕方によって出力形式を分岐（GeoJSONかPBFか、response_formatの指定がないか）
    if "response_format" in mlit_params:
        response_format = mlit_params["response_format"].upper()
        if response_format == "GEOJSON":
            output_format = "GeoJSON" #パラメータで出力形式にGeoJSONが指定されていたらGeoJSONで出力する
        elif response_format == "PBF":
            print("Sorry, this program does not support PBF format. Output will be in GeoJSON format instead.")
            output_format = "GeoJSON" #パラメータで出力形式にPBFが指定されていたら、このプログラム上で対応できないので、代わりにGeoJSONで出力する
        else:
            print("Sorry, specified format is not supported in this program. Output will be in JSON format instead.")
            output_format = "JSON" #パラメータで不明な出力形式が指定されていたら、JSONで出力する
    else:
        output_format = input("Choose output format (JSON/CSV): ").upper() #response_formatの指定がないケースでは、出力形式をJSONかCSVで選択
    
    #選択した出力形式に応じて出力データの整形処理と保存を行う
    if output_format == "GeoJSON":
        with open("mlit_data_" + api_type + ".geojson", "w") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False) #JSON形式での文字列への変換。日本語の文字化け回避のためensure_ascii=Falseで対応。
        print("Data saved as GeoJSON successfully. Please see mlit_data_" + api_type + ".geojson")
    elif output_format == "CSV":
        headers = list(json_data["data"][0].keys()) #ヘッダー項目列の抽出
        with open("mlit_data_" + api_type + ".csv", "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers) #ヘッダー行を書き込む
            for item in json_data["data"]:
                csv_writer.writerow(item.values())
        print("Data saved as CSV successfully. Please see mlit_data_" + api_type + ".csv")
    else:
        with open("mlit_data_" + api_type + ".json", "w") as file:
            json.dump(json_data["data"], file, indent=4, ensure_ascii=False) #JSON形式での文字列への変換。日本語の文字化け回避のためensure_ascii=Falseで対応。
        print("Data saved as JSON successfully. Please see mlit_data_" + api_type + ".json")
#APIからの応答がエラーだった場合はその旨をコマンドラインに示す
else:
    print("Error:", response.status_code)
