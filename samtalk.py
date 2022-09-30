
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
from datetime import datetime

# headless 추가하기
def main():
    month = int(input("Month: ")) # 여기만 변경
    day   = int(input("Day: "))
    
    day_code = get_day_info(month,day)
    
    wb = Workbook()
    ws = wb.active
    ws.append(["구분", "대상자명", "*대상자ID", "*출결일자", "*출결구분코드 (출석(01)/지각(02)/조퇴(03)/결석(04)/기타(99)", "출결 시/분", "귀가 시/분", "급식 (조식(01),중식(03),석식(05))", "사유 및 내용"])
   
    id = [
    "U201706002258007","U201903002258020","U201711002258010","U202004002258032","U202103002258037",
    "U201712002258012","U202103002258035","U201803002258014","U201712002258011","U201804002258019",
    "U202205002258041","U202103002258038","U201704002258006","U202004002258033","U201903002258021",
    "U202001002258031","U202103002258039","U202109002258040","U201803002258015","U202011002258034",
    "U202206002258042","U201804002258016","U201903002258023","U201803002258013","U202001002258027",
    "U202208002258043","U201804002258017"
    ]
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    driver.implicitly_wait(10)
    driver.get("https://www.samtalk.co.kr:8443/academy/login")

    driver.find_element(By.ID, "id").send_keys("myid") # 보안상의 이유로 지워둠
    driver.find_element(By.ID, "pwd").send_keys("mypwd")

    driver.find_element(By.CLASS_NAME, "btn_submit") .click()
    # mouse hover 추가
    driver.find_element(By.LINK_TEXT, "출석부(학급별)").click()

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tbodyList"))
        )
        
        for i in range(27):
            student = driver.find_element(By.CSS_SELECTOR, f"#tbodyList > tr:nth-child({i+1})")
            td_tags = student.find_elements(By.TAG_NAME, "td")
            
            name, attend_code, in_time, out_time, eat_code = get_info(day,td_tags)
            
            to_save = ["", name, id[i], day_code, attend_code, in_time, out_time, eat_code]
            ws.append(to_save)
            
    finally:
        driver.quit()
        wb.save(f"{month}_{day}_attend.xlsx")
    
    
def forming_time(time):
    time_ls = time.split(":")
    my_time = "".join(time_ls)
    return my_time

def get_day_info(month, day):
    current_time = datetime.now()
    
    year  = str(current_time.year)
    month = str(month)
    day   = str(day)
    
    if len(month) == 1:
        month = f"0{month}"
    if len(day)   == 1:
        day = f"0{day}"
    
    day_code = year + month + day
    return day_code

def get_info(day, tags):
    name  = tags[1].text.split("\n")[0]
    times = tags[day + 5].text.split("\n")
    in_time, out_time, attend_code, eat_code, is_weekend = decide_info(times)
    return name, in_time, out_time, attend_code, eat_code

def decide_info(times):
    in_time = forming_time(times[0])
    
    out_time    = ""
    eat_code    = ""
    attend_code = ""
    is_weekend  = False
    
    if in_time   == "결석": # 결석
        attend_code  = "04"
    elif in_time == "공결": # 공결
        attend_code  = "99"
    elif in_time == "":    # 주말 / 공휴일
        is_weekend  = True
    else:                  # 정상출석
        out_time    = forming_time(times[1])
        attend_code = "01"
        eat_code    = "05"
        
    return in_time, out_time, attend_code, eat_code, is_weekend

if __name__ == "__main__":
    main()
    

    







