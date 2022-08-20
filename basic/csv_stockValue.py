import csv
import requests
from bs4 import BeautifulSoup


filename = "stockValue1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t")
writer.writerow(title)

for page in range(1, 5):
    url = f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page={page}'
    res = requests.get(url)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, "lxml")
    
    # type_2 table -> tbody -> tr
    
    data_rows = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    
    for row in data_rows:
        cols = row.find_all("td")
        # 의미 없는 column 제거
        if len(cols) <= 1:
            continue 
        data = [col.text.strip() for col in cols]
        writer.writerow(data)