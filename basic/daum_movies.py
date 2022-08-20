import requests
from bs4 import BeautifulSoup


for year in range(2021, 2016, -1):    
    
    url =f'https://search.daum.net/search?w=tot&q={year}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'

    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    images = soup.find_all("img", attrs={"class": "thumb_img"})

    for i, image in enumerate(images):
    # 상위 5개의 이미지만 저장
        if i > 4: 
            break
        image_url = image["src"]

        if image_url.startswith("//"):
            image_url = "https:"+ image_url

        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open(f"{year}_movie{i+1}.jpg", "wb") as f:
            f.write(image_res.content)