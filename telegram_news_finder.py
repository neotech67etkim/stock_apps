import telegram
import schedule
import time
import sys
import io
from bs4 import BeautifulSoup
import requests

import pytz
import datetime

import pandas as pd


newsFilter = ['판호','특징주','맥스트','챗GPT',\
    '특징주', '유라테크', '새빗켐', \
    'FPCB', '메타버스', '에스티큐브', '넬바스토바트', 'syk저해제', \
    '세비도플레닙', '오스코텍','네옴','빈 살만','사우디',\
    '푸틴', '모더나','JP 모건','에이비엘바이오','올릭스','큐라클','에이프릴바이오','티움바이오','강스템바이오텍',\
    '에이비온','메드팩토','휴이노','에스씨엠생명과학','아리바이오','비엘','마이크로바이옴',\
	'JP모건','엔켐','황반변성','레카네맙','대마','러시아',\
    '광산','리튬','중고차','리오프닝','드론','서린바이오','레드힐','소마젠','미국무역대표부','USTR',\
    '미국재대만협회','AIT','주미 대만 경제문화대표부','미국 정부 대표단','대만','미중','패권전쟁',\
    '중동','두바이','툴젠','마약류','대마','수소','리오프닝','청담글로벌','한국화장품','연우','마운자로',\
    '넥스턴바이오','비만 치료','MDS테크','나무가','diriyah','saudi','arab news','neom','red sea','qiddiya','roshn','가상발전소',\
    'VPP','태양광','풍력','곡물','오픈랜','ddr5','인텔','제온 스케일러블',\
    '지엔원에너지', 'STX', '경동인베스트', '영풍', '웰크론한텍', '혜인', '쎄노텍', '하이드로리튬', '어반리튬', '금양', '미래나노텍', '대모', '수산중공업',\
    '기가레인','와이어블','카카오엔터','웹툰','웹소설','미스터블루','대원미디어','큐브엔터','포르쉐','애머릿지','휴림로봇','동양피스톤','동아에스티','경동인베스트',\
    '신스틸','철강주','AI바이오','씨이랩','보로노이','실리콘투','마이크로소프트','거대 AI','AI 바이오','아비코전자','UWB','다보스','엔켐','삼성SDI','SK온',\
    'LG엔솔','AGV','알체라','스노우','AI 아바타','폐배터리','OTT','CCTV','스마트 홈 카메라','보안','라온시큐어','생체인증','디케이티','와이옥타','OCTA','하이난',\
    '제이에스티나','스마트홈','비대면 진료','비자 해제','비자해제','tesla','XR','AR','엔피','폼팩터','코세스']

recentSubject = []
token = "5876483553:AAF77ZUF-F72eEWy8NaUx8ax6VBP5fTDIYU"
bot = telegram.Bot(token=token)
chat_id = "-1001557650956"
#chat_id = "5457358533"


code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
code_df = code_df[['회사명', '종목코드']]
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
#print(code_df)

def job():
    global recentSubject
    
    now = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    if now.hour >= 22 or now.hour <= 7:
        return

    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

    BASE_URL = "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&listType=title&sid1=001"

    with requests.Session() as s:
        res = s.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, 'html.parser')
            for cnt in range(5):
                tmp_loc = f"#main_content > div.list_body.newsflash_body > ul:nth-child(1) > li:nth-child({cnt+1}) > a"
                article = soup.select_one(tmp_loc)
                articleText = article.text
                articleHref = article.attrs['href']
                for i in range(0, len(newsFilter)):
                    if (newsFilter[i] in articleText) and (articleText not in recentSubject) and ('김건희' not in articleText):
                        bot.sendMessage(chat_id=chat_id,
                                     text=articleText + articleHref)
                        recentSubject.append(articleText)
                        print(articleText)
    
    

# 0.5초 마다 실행
schedule.every(1).seconds.do(job)

newsin = '키워드 목록 : '

for i in newsFilter:
    newsin = newsin + i + ','
        
bot.sendMessage(chat_id=chat_id, text=newsin)

# 파이썬 스케줄러
while True:
    schedule.run_pending()
    time.sleep(1)