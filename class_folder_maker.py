# Web Crawling
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
from tkinter import messagebox, filedialog

import re
import os
import time

url = "https://eclass.tukorea.ac.kr/ilos/main/member/login_form.acl"

# GUI
window = Tk()
window.title("Class Folder Maker")
window.rowconfigure(0, minsize=20)
window.columnconfigure(0, minsize=20)
window.resizable(False, False)

subWindow = None

# ID, PW 입력
loginFrame = LabelFrame(
    window,
    borderwidth=2,
    text="Login",
    pady=5,
    padx=5,
)
loginFrame.grid(
    row=0,
    column=0,
    columnspan=3,
)

label_id = Label(loginFrame, text="ID: ", width=3)
label_id.grid(row=0, column=0)
entry_id = Entry(loginFrame, width=15)
entry_id.grid(row=0, column=1)

entry_id.focus()

label_pw = Label(loginFrame, text="PW: ", width=3)
label_pw.grid(row=0, column=2)
entry_pw = Entry(loginFrame, width=15, show="*")
entry_pw.grid(row=0, column=3)

entry_pw.bind("<Return>", lambda event: login_and_make_folder(event))


# 폴더 위치 선택
def set_folder_path():
    global folderPath
    path = filedialog.askdirectory()
    folderPath.set(path)


folderPath = StringVar()
button_folderSet = Button(window, text="Select Folder", command=set_folder_path)
button_folderSet.grid(row=2, column=1, padx=2, pady=2, sticky="w")
folderPath = StringVar()
folderPath.set(os.getcwd())
entry_folderPath = Entry(window, textvariable=folderPath, width=40)
entry_folderPath.grid(row=2, column=0, padx=3, pady=3)


# 브라우저 숨기기
showBrowser = BooleanVar()
check_showBrowser = Checkbutton(
    window, text="Show Crawling Browser", variable=showBrowser
)
check_showBrowser.grid(row=3, column=0, padx=2, pady=2, sticky="w")


# driver 위치 설정
def set_driver_path():
    global driverPath
    path = filedialog.askopenfilename()
    driverPath = path


driverPath = os.path.join(os.getcwd(), "chromedriver.exe")
button_driverSet = Button(window, text="Select Driver", command=set_driver_path)
button_driverSet.grid(row=3, column=1, padx=2, pady=2, sticky="w")


def login_fail():
    messagebox.showerror("Login Fail", "아이디와 비밀번호를 다시 확인해주세요.")


def login(event=None):
    options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
    if not showBrowser.get():  # 사용자 설정에 따라 브라우저 숨기기
        options.add_argument("headless")
    driver = webdriver.Chrome(driverPath, options=options)  # driver 객체 생성
    driver.get(url)  # url 접속

    # 로그인
    try:
        id_input = driver.find_element(By.NAME, "usr_id")
        pw_input = driver.find_element(By.NAME, "usr_pwd")
        id_input.send_keys(entry_id.get())
        pw_input.send_keys(entry_pw.get())

        login_button = driver.find_element(By.ID, "login_btn")
        login_button.click()

        time.sleep(0.25)  # 페이지 로딩 대기

        # url이 변경되지 않은 경우 정상 로그인 X
        if url == driver.current_url:
            login_fail()
            return None

    # 예외 처리
    except (
        UnexpectedAlertPresentException,
        NoAlertPresentException,
        NoSuchElementException,
    ):
        login_fail()
        return None

    # 수강 과목 목록 가져오기
    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()
    main = BeautifulSoup(driver.page_source, "html.parser")
    subjectList = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")
    subjectList = [subject.text for subject in subjectList]

    # 브라우저 종료
    driver.quit()

    # 문자열로 반환
    return subjectList[0]


def find_subject(subjectStr):
    titleRegex = re.compile(r"[0-9]{4}-[1-2]{1}학기")
    subjectRegex = re.compile(r"\b(\S+(?:\s\S+)*)\([0-9]+\)")

    title = titleRegex.search(subjectStr)
    subjects = subjectRegex.findall(subjectStr)

    return title.group(), subjects


def make_folder(event, title, subjects, checkList):
    global subWindow
    for i, subject in enumerate(subjects):
        if checkList[i].get():
            os.makedirs(os.path.join(folderPath.get(), title, subject), exist_ok=True)

    subWindow.withdraw()


def login_and_make_folder(event=None):
    global subWindow

    subjectStr = login()
    if subjectStr is None:
        return
    title, subjects = find_subject(subjectStr)

    if subWindow is not None:
        subWindow.destroy()
    subWindow = Toplevel(window)
    subWindow.title("Select Subjects")
    subWindow.rowconfigure(0, minsize=50)
    subWindow.columnconfigure(0, minsize=20)

    label_subjects = Label(subWindow, text="Select Subjects", border=2, relief="groove")
    label_subjects.grid(row=0, column=0, columnspan=2)

    checkList = []

    for i, subject in enumerate(subjects):
        isCheck = BooleanVar()
        checkList.append(isCheck)
        isCheck.set(True)
        check_subject = Checkbutton(
            subWindow,
            text=subject,
            variable=isCheck,
        )
        check_subject.grid(row=i + 1, column=0, sticky="w")

    button_makeFolder = Button(
        subWindow,
        text="Make Folder",
        command=lambda: make_folder(None, title, subjects, checkList),
    )
    button_makeFolder.grid(row=i + 2, column=0, columnspan=2)

    subWindow.mainloop()


button_login = Button(loginFrame, text="Login", command=login_and_make_folder)
button_login.grid(row=0, column=4, padx=5)

window.bind("<Escape>", lambda event: window.destroy())
window.mainloop()
