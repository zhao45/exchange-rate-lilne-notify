import urllib.request as request
from bs4 import BeautifulSoup as sp
import requests
import time
from datetime import datetime

# LineNotify 函數
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code

# 白銀價格監控和發送LINE通知
def check_silver_price():
    url = "https://www.exchange-rates.org/zh-hant/precious-metals/silver-price/taiwan"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    req = request.Request(url, headers=headers)
    with request.urlopen(req) as response:
        data = response.read().decode("utf-8")
    root = sp(data, "html.parser")
    silver_price = root.find_all("td")[1].text.strip()
    silver_change = root.find_all("td")[2].find("span", class_="rate-change rate-green").text.strip()
    silver_change_cleaned = silver_change.strip(' "')
    
    # 組合訊息並發送通知
    message = f"台灣白銀價格: {silver_price}，漲幅: {silver_change_cleaned}"
    token = 'HKzWCviZhNrCMvvylQgiM5uK3CpbL6aOd24onWWFFpX'  # 請替換成你的Token
    lineNotifyMessage(token, message)

# 確認是否為中午12點並發送通知
def run_daily_notify():
    while True:
        now = datetime.now()
        if now.hour == 1 and now.minute == 0:  # 判斷幾點
            check_silver_price()
            time.sleep(120)  # 等待2分鐘後再次檢查，以避免重複發送
        else:
            time.sleep(30)  # 每30秒檢查一次時間

run_daily_notify()
