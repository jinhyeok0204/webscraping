import requests
import re
from bs4 import BeautifulSoup


# 5개의 페이지까지

idx = 1  # 제품 인덱스
for i in range(1, 6):
    page = i
    url = f'https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page}&rocketAll=false&searchIndexingToken=1=6&backgroundColor='
    headers = {"Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    p = re.compile("^search-product")
    items = soup.find_all("li", attrs={"class": p})

    print(f"[현재 페이지는 {page}p 입니다 ]")
    print("-" * 100)

    for item in items:

        # 광고 붙어있는 제품 제외
        is_ad = item.find("span", attrs={"class": "ad-badge-text"})
        if is_ad:
            print("[광고 제품은 제외]")
            print("-" * 100)
            continue

        name = item.find("div", attrs={"class": "name"}).text.strip()

        # 애플 제품 제외
        if "Apple" in name:
            print("[Apple 제품을 제외]")
            print("-" * 100)
            continue

        price = item.find("strong", attrs={"class": "price-value"}).text + "원"
        star = item.find("em", attrs={"class": "rating"})
        rating_total_count = item.find("span", attrs={"class": "rating-total-count"})

        # 리뷰 없는 제품 제외
        if star:
            star = star.text
            rating_total_count = rating_total_count.text
        else:
            print("[리뷰가 없는 제품 제외]")
            print("-" * 100)
            continue

        link = "https://www.coupang.com" + item.find("a", attrs={"class":"search-product-link"})["href"]
        # 리뷰 400개 이상, 평점 4.9 이상의 제품만 조회
        if float(star) >= 4.9 and int(rating_total_count[1:-1]) >= 400:
            print(f"제품명 : {name}")
            print(f"가격 : {price}")
            print(f"평점 : {star} {rating_total_count}")
            print(f"바로가기 : {link} ")
            print("-"*100)
            idx += 1


