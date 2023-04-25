from tkinter import *
from tkinter.ttk import *


class GUI:
    window = None

    # 크롤링 화면 보이기/안보이기 설정
    crawlingShow = None

    # 과목명 체크박스 리스트
    subjectList = []
    subjectList_var = []

    # 경로 선택
    rootPath = None
    txt_rootPath = None

    # 아이디, 비밀번호 입력 창
    entry_id = None
    entry_pw = None

    # 크롤링 버튼

    # 폴더 생성 버튼

    def __init__(self, webDriver):
        self.driver = webDriver

        if self.window == None:
            self.window = Tk()
            self.window.title("NewSemesterFolderCreator")

        # 크롤링 화면 보이기/안보이기 설정
        self.crawlingShow = IntVar()
        self.crawlingShow.set(0)

        btn_crawlingShow = Checkbutton(
            text="크롤링 화면 보이기", variable=self.crawlingShow, command=self.check_crawling
        )
        btn_crawlingShow.pack()

        # 경로 선택
        frame_pathSelect = Frame(self.window)
        frame_pathSelect.pack()

        btn_pathSelect = Button(
            frame_pathSelect, text="경로 선택", command=self.set_root_folder
        )
        btn_pathSelect.pack(side=RIGHT)

        self.txt_rootPath = Label(frame_pathSelect, text=self.rootPath)
        self.txt_rootPath.pack(side=LEFT)

        # 로그인
        frame_login = Frame(self.window)
        frame_login.pack()
        self.entry_id = Entry(frame_login)
        self.entry_id.pack(side=TOP)
        self.entry_pw = Entry(frame_login)
        self.entry_pw.pack(side=TOP)
        btn_login = Button(frame_login, text="로그인", command=self.login_info)
        btn_login.pack(side=TOP)

    def check_crawling(self):
        if self.crawlingShow.get():
            self.driver.add_argument("headless")
        else:
            self.driver.remove_argument("headless")

    def set_root_folder(self):
        self.rootPath = filedialog.askdirectory()
        os.chdir(self.rootPath)
        self.txt_rootPath.config(text=self.rootPath)

    def get_root_folder(self):
        return self.rootPath

    def login_info(self):
        return self.entry_id.get(), self.entry_pw.get()
