# Web Crawling - 과목 정보 문자열로 획득
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Crawling을 통해 획득한 문자열을 정규식으로 통해 과목이름 별로 분리
import re

# 분리한 과목이름 리스트를 통해 과목별 폴더 생성
import os

test = False
if not test:
    driver = webdriver.Chrome("./chromedriver.exe")

    url = "https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"

    driver.get(url)

    driver.find_element(By.NAME, "usr_id").send_keys("2019182003")
    driver.find_element(By.NAME, "usr_pwd").send_keys("3183129")
    driver.find_element(By.ID, "login_btn").click()

    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()

    main = BeautifulSoup(driver.page_source, "html.parser")
    subjectList = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")

    subjectList = [subject.text for subject in subjectList]

    driver.quit()

# subjectStr = "\n\n\n2023-1학기 정규과목\n\n\n\n3D게임프로그래밍1(01)\n\n\n\n이용희\n수 [7~8] 15:30~17:20 금 [7~8] 15:30~17:20 (E동511호,E동424호)\xa0\n\n\n\n\nSTL(02)\n\n\n\n윤정현\n월 [2~3] 10:30~12:20 화 [5~6] 13:30~15:20 (E동323호)\xa0\n\n\n\n\n네트워크 기초(03)\n\n\n\n김재경\n월 [6]    14:30~15:20 화 [2~3] 10:30~12:20 (E동322호)\xa0\n\n\n\n\n스크립트언어(04)\n\n\n\n이대현\n월 [9~10] 17:25~19:05 금 [3~4] 11:30~13:20 (TIP209호)\xa0\n\n\n\n\n인간과현대사회(04)\n\n\n\n박한경\n목 [11~13] 19:05~21:40 (산융405호)\xa0\n\n\n\n\n한국문학산책(03)\n\n\n\n문선영\n목 [6~8] 14:30~17:20 (산융206호)\xa0\n\n\n\n\n현대사회와스포츠문화(02)\n\n\n\n김석기\n수 [11~12] 19:05~20:50 (C동111호)\xa0\n\n\n\n"

titleRegex = re.compile(r"[0-9]{4}-[1-2]{1}학기")
subjectRegex = re.compile(r"(\w+)(\([0-9]+\))")

title = titleRegex.search(subjectList[0])

subjects = subjectRegex.findall(subjectList[0])

os.mkdir(title.group())
for subject in subjects:
    os.mkdir(title.group() + "/" + subject[0])

# 해결해야될 문제 중간에 띄어쓰기가 있는
# '네트워크 기초' 같은 경우 뒤에 있는 '기초'만 과목명으로 인식
