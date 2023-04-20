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
window.rowconfigure(0, minsize=50)
window.columnconfigure(0, minsize=20)

subWindow = None

# ID, PW 입력
loginFrame = LabelFrame(
    window,
    borderwidth=2,
    text="Login",
    pady=5,
    padx=5,
)
loginFrame.grid(row=0, column=0, columnspan=2)

label_id = Label(loginFrame, text="ID: ", width=3)
label_id.grid(row=0, column=0)
entry_id = Entry(loginFrame, width=10)
entry_id.grid(row=0, column=1)

entry_id.focus()

label_pw = Label(loginFrame, text="PW: ", width=3)
label_pw.grid(row=0, column=2)
entry_pw = Entry(loginFrame, width=10, show="*")
entry_pw.grid(row=0, column=3)

entry_pw.bind("<Return>", lambda event: login_and_make_folder(event))


# 폴더 위치 선택
def set_folder_path():
    global folderPath
    path = filedialog.askdirectory()
    folderPath.set(path)


folderPath = StringVar()
button_folderSet = Button(window, text="Select Folder", command=set_folder_path)
button_folderSet.grid(row=2, column=1, padx=2, pady=2)
entry_folderPath = Entry(window, textvariable=folderPath, width=30)
entry_folderPath.grid(row=2, column=0, padx=10, pady=10)


# 브라우저 숨기기
showBrowser = BooleanVar()
check_showBrowser = Checkbutton(window, text="Show Browser", variable=showBrowser)
check_showBrowser.grid(row=3, column=0, sticky="w", padx=10)


def login_fail():
    messagebox.showerror("Login Fail", "아이디와 비밀번호를 다시 확인해주세요.")


def login(event=None):
    print("call login")
    options = webdriver.ChromeOptions()
    if not showBrowser.get():
        options.add_argument("headless")
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    driver.get(url)

    try:
        id_input = driver.find_element(By.NAME, "usr_id")
        pw_input = driver.find_element(By.NAME, "usr_pwd")
        id_input.send_keys(entry_id.get())
        pw_input.send_keys(entry_pw.get())

        login_button = driver.find_element(By.ID, "login_btn")
        login_button.click()

        time.sleep(0.5)

        if url == driver.current_url:
            login_fail()
            return None

    except UnexpectedAlertPresentException as error:
        alert = None
        try:
            alert = driver.switch_to.alert
            login_fail()
            return None
        except NoAlertPresentException:
            login_fail()
            return None
    except (NoAlertPresentException, NoSuchElementException) as error:
        login_fail()
        return None
    driver.find_element(
        By.CSS_SELECTOR, "#quick-menu-index > a:nth-child(1) > div"
    ).click()
    main = BeautifulSoup(driver.page_source, "html.parser")
    subjectList = main.select("#lecture_list > div:nth-child(2) > div:nth-child(1)")
    subjectList = [subject.text for subject in subjectList]

    driver.quit()

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
        return None
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

window.mainloop()
