import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import re
from selenium import webdriver
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from pandas import json_normalize

treasury_3year = {}
previous_dividend_yield = {}

# 국고채금리를 파싱하는 함수
def get_value_3year_treasury():
    url = "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=107301&idx_cd=1073&freq=Y&period=N"

    df2 = pd.read_html(url)[0]
    return df2.iloc[1]

def get_estimated_dividend_yield(code):
    dividend_yield = get_financial_statements(code)
    if len(dividend_yield) == 0:
        return 0
    dividend_yield = sorted(dividend_yield.items())[-1]
    return dividend_yield[1]

def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url, verify=False).text

    soup = BeautifulSoup(html, 'html5lib')
    dt_data = soup.select("td dl dt")

    dividend_yield = dt_data[-2].text
    dividend_yield = dividend_yield.split(' ')[1]
    dividend_yield = dividend_yield[:-1]

    return dividend_yield

def get_previous_dividend_yield(code):
    dividend_yield = get_financial_statements(code)

    now = datetime.datetime.now()
    cur_year = now.year

    global previous_dividend_yield

    for year in range(cur_year - 5, cur_year):
        if str(year) in dividend_yield:
            previous_dividend_yield[year] = dividend_yield[str(year)]

    return previous_dividend_yield

def get_financial_statements(code):
    # 인증값 추출
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    url = "https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    html = requests.get(url, verify=False).text

    search = re_enc.search(html)
    if search is None:
        return {}
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    # 스크래핑
    url = "https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(
        code, encparam, encid)
    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers, verify=False).text

    soup = BeautifulSoup(html, "html5lib")
    dividend = soup.select("table:nth-of-type(2) tr:nth-of-type(33) td span")
    years = soup.select("table:nth-of-type(2) th")

    dividend_dict = {}
    for i in range(len(dividend)):
        dividend_dict[years[i + 3].text.strip()[:4]] = dividend[i].text

    return dividend_dict

def get_current_3year_treasury():
    url = "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser') 
    td_data = soup.select("tr td") 
    return td_data[1].text

def get_3year_treasury():
    global treasury_3year
    df3 = get_value_3year_treasury()
    
    labels = df3.index.str.strip().tolist()  # Remove extra spaces
    values = df3.tolist()
    
    treasury_3year = dict(zip(labels, values))

    return treasury_3year
    
if __name__ == "__main__":
    
    print(get_3year_treasury())
    stock=input("stock number: ")
    print(get_dividend_yield(stock))
    print(get_estimated_dividend_yield(stock))
    print(get_previous_dividend_yield(stock))
