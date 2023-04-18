# Web Crawling - 과목 정보 문자열로 획득
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoAlertPresentException,
    UnexpectedAlertPresentException,
    NoSuchElementException,
)

# GUI
from tkinter import *
from tkinter.ttk import *

# Crawling을 통해 획득한 문자열을 정규식으로 통해 과목이름 별로 분리
import re

# 분리한 과목이름 리스트를 통해 과목별 폴더 생성
import os

# GUI
window = Tk()
window.title("NewSemesterFolderCreator")

# 크롬 브라우저를 띄우지 않고 크롤링
options = webdriver.ChromeOptions()
options.add_argument("headless")

test = False

if not test:
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

    url = "https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"

    driver.get(url)

    while True:
        userID = str(input("ID: "))
        userPW = str(input("PW: "))
        try:
            driver.find_element(By.NAME, "usr_id").send_keys(userID)
            driver.find_element(By.NAME, "usr_pwd").send_keys(userPW)
            driver.find_element(By.ID, "login_btn").click()
            if url != driver.current_url:
                break
        except UnexpectedAlertPresentException as error:
            alert = None
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                pass
            # alert.accept()
            print("아이디와 비밀번호를 다시 확인해주세요.")
        except (NoAlertPresentException, NoSuchElementException) as error:
            print("아이디와 비밀번호를 다시 확인해주세요.")

    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()

    main = BeautifulSoup(driver.page_source, "html.parser")
    subjectList = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")

    subjectList = [subject.text for subject in subjectList]

    driver.quit()

if test:
    subjectList = [
        "\n\n\n2023-1학기 정규과목\n\n\n\n3D게임프로그래밍1(01)\n\n\n\n이용희\n수 [7~8] 15:30~17:20 금 [7~8] 15:30~17:20 (E동511호,E동424호)\xa0\n\n\n\n\nSTL(02)\n\n\n\n윤정현\n월 [2~3] 10:30~12:20 화 [5~6] 13:30~15:20 (E동323호)\xa0\n\n\n\n\n네트워크 기초(03)\n\n\n\n김재경\n월 [6]    14:30~15:20 화 [2~3] 10:30~12:20 (E동322호)\xa0\n\n\n\n\n스크립트언어(04)\n\n\n\n이대현\n월 [9~10] 17:25~19:05 금 [3~4] 11:30~13:20 (TIP209호)\xa0\n\n\n\n\n인간과현대사회(04)\n\n\n\n박한경\n목 [11~13] 19:05~21:40 (산융405호)\xa0\n\n\n\n\n한국문학산책(03)\n\n\n\n문선영\n목 [6~8] 14:30~17:20 (산융206호)\xa0\n\n\n\n\n현대사회와스포츠문화(02)\n\n\n\n김석기\n수 [11~12] 19:05~20:50 (C동111호)\xa0\n\n\n\n"
    ]

titleRegex = re.compile(r"[0-9]{4}-[1-2]{1}학기")
subjectRegex = re.compile(r"\b(\S+(?:\s\S+)*)\([0-9]+\)")

title = titleRegex.search(subjectList[0])

subjects = subjectRegex.findall(subjectList[0])

print(subjects)

os.mkdir(title.group())
for subject in subjects:
    os.mkdir(title.group() + "/" + subject)


def generate_gui():
    window = Tk()
    window.title("NewSemesterFolderCreator")

    # 가져온 과목 체크박스 리스트
    ui_subjectAndReadFrame = Frame(window)
    ui_subjectAndReadFrame.pack()


def ui_generate_subjectLists(frame, subjectList=None):
    if subjectList == None:
        return

    subjectCheckBoxes = []
    for subject in subjectList:
        subjectCheckBoxes.append(Checkbutton(frame, text=subject))


def web_generate_webdriver():
    # 크롬 브라우저를 띄우지 않고 크롤링
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    url = "https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"
    driver.get(url)
    return driver


def web_login_eClass():
    while True:
        userID = str(input("ID: "))
        userPW = str(input("PW: "))
        try:
            driver.find_element(By.NAME, "usr_id").send_keys(userID)
            driver.find_element(By.NAME, "usr_pwd").send_keys(userPW)
            driver.find_element(By.ID, "login_btn").click()
            if url != driver.current_url:
                break
        except UnexpectedAlertPresentException as error:
            alert = None
            try:
                alert = driver.switch_to.alert
            except NoAlertPresentException:
                pass
            # alert.accept()
            print("아이디와 비밀번호를 다시 확인해주세요.")
        except (NoAlertPresentException, NoSuchElementException) as error:
            print("아이디와 비밀번호를 다시 확인해주세요.")

        # 오류가 발생하면 빠져나가서 경고 메시지 출력하도록 변경


def web_get_subject_list():
    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()
    main = BeautifulSoup(driver.page_source, "html.parser")
    subjectList = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")
    subjectList = [subject.text for subject in subjectList]
    return subjectList[0]


def find_semester_and_subjects(subjectStr):
    titleRegex = re.compile(r"[0-9]{4}-[1-2]{1}학기")
    subjectRegex = re.compile(r"\b(\S+(?:\s\S+)*)\([0-9]+\)")

    title = titleRegex.search(subjectStr)
    subjects = subjectRegex.findall(subjectStr)

    return title.group(), subjects


def set_root_folder():
    # tk로 폴더 선택
    # 해당 폴더로 이동
    pass


def make_folder(semester, subjects):
    os.mkdir(semester)
    for subject in subjects:
        os.mkdir(semester + "/" + subject)
