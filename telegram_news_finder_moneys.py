import telegram
import schedule
import time
import sys
import io
from bs4 import BeautifulSoup
import requests
import pytz
import datetime
import os
import pandas as pd

import certifi
import urllib3
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

newsFilter2 = ['특징주']

recentSubject = ""
token = "5876483553:AAF77ZUF-F72eEWy8NaUx8ax6VBP5fTDIYU"
bot = telegram.Bot(token=token)
chat_id = "-1001557650956"
#chat_id = "5457358533"

def job():
    global recentSubject
    
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if now.hour >= 22 or now.hour <= 8:
        return

    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

    BASE_URL2 = "https://moneys.mt.co.kr/news/mwList.php?code=w0000&code2=w0100"

    try:
        with requests.Session() as s:
                res = s.get(BASE_URL2, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
                if res.status_code == requests.codes.ok:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    article = soup.select_one(
                        '#content > div > ul > li:nth-child(1) > a')
                    articleHref = article.attrs['href']    
                    

                    title = soup.select_one(
                        '#content > div > ul > li:nth-child(1) > a > div > strong')
                    titleText = title.text
                    article = soup.select_one(
                        '#content > div > ul > li:nth-child(1) > a > div > span > span.write')
                    articleText = article.text
                    attention_alarm = "-----------------------------------\n주목하세요. 이지운 기자님 특징주 기사입니다.\n-----------------------------------"
                    
                    if ("이지운 기자" in articleText) and (articleText != recentSubject) and ("특징주" in titleText):
                        bot.sendMessage(chat_id=chat_id,
                                        text=attention_alarm)
                        bot.sendMessage(chat_id=chat_id,
                                        text=articleText + articleHref)
                        recentSubject = articleText
                        print(articleText)
    except:
        print("에러가 났으나 다시 작동합니다.")
        os.system("C:/Python310/python.exe C:/Users/neote/study/telegram_news_finder_moneys.py")


# 0.5초 마다 실행
schedule.every(60).seconds.do(job)

bot.sendMessage(chat_id="5457358533", text="이지운 기자 기사 감시 시작")

# 파이썬 스케줄러
while True:
    schedule.run_pending()
    time.sleep(60)