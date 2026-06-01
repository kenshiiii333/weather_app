from flask import Flask, render_template, request
import requests

# 翻訳ライブラリ
from deep_translator import GoogleTranslator

app = Flask(__name__)

# OpenWeatherMap APIキー
API_KEY = "0f0ad71ace673342488d7f02af25c565"




@app.route("/", methods=["GET", "POST"])
def index():

    # 最初は東京
    target_city = "Tokyo"

    # 検索された時
    if request.method == "POST":

        target_city = request.form.get("city_name")

        target_city = target_city.strip()

        print("入力:", target_city)

    # 日本語 → 英語へ翻訳
        target_city = GoogleTranslator(
            source='ja',
            target='en'
        ).translate(target_city)

        print("翻訳後:", target_city)
    # API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={target_city}&appid={API_KEY}&units=metric&lang=ja"

    print(url)

    # API通信
    response = requests.get(url)

    # JSONをPython辞書へ変換
    data = response.json()

    print(data)

    # エラー時
    if response.status_code != 200:

        return render_template(
            "index.html",
            city="見つかりませんでした",
            weather="-",
            temp="-",
            humidity="-",
            icon_url="",
            main_weather=""
        )

    # 天気情報取得
    weather = data["weather"][0]["description"]

    # 気温
    temp = data["main"]["temp"]

    # 湿度
    humidity = data["main"]["humidity"]

    # 都市名
    city = data["name"]

    # 天気アイコン
    icon = data["weather"][0]["icon"]

    # アイコンURL
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    # 背景変更用
    main_weather = data["weather"][0]["main"]

    # HTMLへ渡す
    return render_template(
        "index.html",
        city=city,
        weather=weather,
        temp=temp,
        humidity=humidity,
        icon_url=icon_url,
        main_weather=main_weather
    )


# 実行
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
