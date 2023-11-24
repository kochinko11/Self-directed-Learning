from bs4 import BeautifulSoup
import requests

def get_current_3year_treasury():
    url = "https://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser') 
    td_data = soup.select("tr td") 
    return td_data[1].text

if __name__ == "__main__":
    print(get_current_3year_treasury())