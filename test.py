from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tkinter import *
from tkinter import filedialog
import os
import time
import re

# Tkinter 윈도우 생성
root = Tk()
root.title("eClass Login")

# ID 입력 Label, Entry 생성
id_label = Label(root, text="ID:")
id_label.grid(row=0, column=0)
id_entry = Entry(root)
id_entry.grid(row=0, column=1)
id_entry.focus()

# PW 입력 Label, Entry 생성
pw_label = Label(root, text="Password:")
pw_label.grid(row=1, column=0)
pw_entry = Entry(root, show="*")
pw_entry.grid(row=1, column=1)


# 폴더 선택 버튼 생성
def choose_folder():
    global folder_path
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


folder_path = StringVar()
folder_button = Button(root, text="Select Folder", command=choose_folder)
folder_button.grid(row=2, column=0)
folder_entry = Entry(root, textvariable=folder_path)
folder_entry.grid(row=2, column=1)


# 로그인 버튼 생성
def login():
    # 드라이버 경로 설정
    driver_path = "chromedriver.exe"
    # 크롬 드라이버 실행
    driver = webdriver.Chrome(driver_path)
    # eClass 로그인 페이지로 이동
    driver.get("https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl")
    # ID와 PW 입력
    id_input = driver.find_element(By.NAME, "usr_id")
    pw_input = driver.find_element(By.NAME, "usr_pwd")
    id_input.send_keys(id_entry.get())
    pw_input.send_keys(pw_entry.get())
    # 로그인 버튼 클릭
    login_button = driver.find_element(By.ID, "login_btn")
    login_button.click()
    # 페이지 로딩 대기
    time.sleep(5)
    # 과목명 리스트 생성
    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()
    main = BeautifulSoup(driver.page_source, "html.parser")
    subject = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")
    subjectList = [subject_.text for subject_ in subject]
    # 드라이버 종료
    driver.quit()

    titleRegex = re.compile(r"[0-9]{4}-[1-2]{1}학기")
    subjectRegex = re.compile(r"\b(\S+(?:\s\S+)*)\([0-9]+\)")

    title = titleRegex.search(subjectList[0])
    subjects = subjectRegex.findall(subjectList[0])

    # 폴더 생성
    base_folder = folder_path.get()
    for subject in subjects:
        subject_folder = os.path.join(base_folder, subject)
        os.makedirs(subject_folder, exist_ok=True)


login_button = Button(root, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2)

root.mainloop()
