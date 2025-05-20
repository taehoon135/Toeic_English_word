import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinter import Tk, Frame
from tkinter import messagebox

def quiz_menu(root, user_number):
    from quiz_interpret import quiz_interpret
    from quiz_four_choice import quiz_four_choice
    from quiz_word import quiz_word1
    from quiz_sentence import quiz_sentence
    from quiz_rain import AcidRainGame
    from menu import main_menu
    from ranking import ranking
    from assist_module import category_id_search

    #DB연결
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.category_db import CategoryDB

    #카테고리값 임시로 생성
    category_db = CategoryDB()
    
    category_db.create_category(user_number, "전체") #기본적으로 포함되어 있어야 하나 어떻게 되있을지는 모름
    category_db.create_category(user_number, "category1")
    category_db.create_category(user_number, "category2")
    category_db.create_category(user_number, "i'm category")

    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()

    root.title("퀴즈 메뉴")
    root.geometry("400x600")

    # 스타일 설정
    style = ttk.Style()
    style.configure("Placeholder.TEntry", foreground="gray")
    style.configure("Normal.TEntry", foreground="black")

    def go_to_menu():
        main_menu(root, user_number)
    
    def go_to_ranking():
        ranking(root, user_number)

    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", pady=10, padx=10)

    # 랭킹 버튼 (왼쪽 상단)
    rank_button = ttk.Button(button_frame, text="랭킹", bootstyle="secondary", command=go_to_ranking)
    rank_button.pack(side="left")

    # 홈 버튼 (오른쪽 상단)
    home_button = ttk.Button(button_frame, text="🏠 홈", bootstyle="secondary", command=go_to_menu)
    home_button.pack(side="right")

    # 옵션 선택 (OptionMenu)
    category_list = category_db.get_user_categories(user_number)
    category_only_name = ["임시"] #카테고리 이름만을 포함하는 리스트 생성
    for category in category_list:
        category_only_name.append(category["name"])
    #전체를 맨 앞으로 보냄
    category_only_name.remove("전체")
    category_only_name.insert(0, "전체")

    options = category_only_name
    option_var = tk.StringVar(value="전체")

    #가젯 생성
    option_menu = ttk.OptionMenu(root, option_var, option_var.get(),*options)
    option_menu.pack(pady=10)

    # 모드 선택 (OptionMenu)
    mode_var = tk.StringVar(value="Select Mode")
    modes = ["해석 맞추기", "해석 맞추기", "단어 맞추기", "사지선다형 단어 맞추기", "문장 채우기 게임", "산성비 게임"]

    #이미지 불러오기
    image1 = Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.exampleForGame1.jpg")  # 불러올 이미지 경로 (임의로 자기 경로에 맞게 설정해야 함)
    image1_5 = Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.exampleForGame1_5.jpg")
    image2 = Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.exampleForGame2.jpg")
    image3 = Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.exampleForGame3.jpg")
    image4 = Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.exampleForGame4.jpg")
    image1 = image1.resize((350, 300))
    image1_5 = image1_5.resize((350, 300))
    image2 = image2.resize((350, 300)) 
    image3 = image3.resize((350, 300)) 
    image4 = image4.resize((350, 300)) 
    photo1 = ImageTk.PhotoImage(image1)  #tk에서 사용할 수 있게 변환
    photo1_5 = ImageTk.PhotoImage(image1_5)
    photo2 = ImageTk.PhotoImage(image2)
    photo3 = ImageTk.PhotoImage(image3)
    photo4 = ImageTk.PhotoImage(image4)
    mode_explain = [photo1, photo1_5, photo2, photo3, photo4]

    # 모드 변경 시 그 모드에 대한 예시를 이미지로 출력
    def handle_mode_change(selected_mode):
        #인덱스 검색
        index = modes.index(selected_mode) - 1 #mode1이 중복되므로 하나 줄여야 함
        if (index < 0):
            index += 1
        
        label_display1.config(image= mode_explain[index])

    # OptionMenu 생성 시 command 추가
    mode_menu = ttk.OptionMenu(root, mode_var, *modes, command=handle_mode_change)
    mode_menu.pack(pady=10)

    # === ✅ 라벨을 위한 프레임 생성 ===
    style.configure("Custom.TFrame")  # 스타일 생성
    frame_display = ttk.Frame(root, style="Custom.TFrame")  # 스타일 적용
    frame_display.pack(pady=20)

    # 카테고리에 대한 라벨 생성 (초기값)
    label_display1 = ttk.Label(
        frame_display, 
        image=mode_explain[0],  # 모드에 따른 게임 예시. 초기 설정
        font=("나눔고딕", 16, "bold"),  # 글꼴 설정
        foreground="#3F7D58",
        bootstyle="info",  # 버튼 스타일
        wraplength=250,  # 텍스트가 자동으로 줄바꿈되도록 설정
        justify="center",  # 텍스트 중앙 정렬
        anchor="center",  # 텍스트 중앙 정렬
        borderwidth=2,  # 테두리 두께
        relief="raised" #테두리 스타일
    )
    label_display1.pack(pady=20, fill="both", expand=True)

    # 모드에 따라 다른 함수 실행
    def mode_1_function(selected_category):
        quiz_interpret(root, user_number, selected_category)

    def mode_1_5_function(selected_category):
        quiz_word1(root, user_number, selected_category)

    def mode_2_function(selected_category):
        quiz_four_choice(root, user_number, selected_category) #선택된 카테고리로 str값임

    def mode_3_function(selected_category):
        #API값이 존재하는지 확인
        from database.user_db import UserDB
        user_db = UserDB()
        if (user_db.get_api_key(user_number) != None):
            quiz_sentence(root, user_number, selected_category)
        else:
            from tkinter import messagebox
            messagebox.showwarning("경고", "API를 등록해주세요.")

    def mode_4_function(selected_category):
        game = AcidRainGame(root, user_number, selected_category)

    # Start 버튼 클릭 시 실행될 함수
    def start_button_clicked():
        selected_mode = mode_var.get()
        selected_category = option_var.get()

        #카테고리가 전체인 경우 아래 코드를 무시함
        if (selected_category != "전체"):
            #카테고리 내의 단어가 4개 미만인 경우를 경우를 고려
            category_id = category_id_search(user_number, selected_category)  #카테고리 이름으로 번호 찾기
            words_in_category = category_db.get_words_in_category(category_id)
            if (len(words_in_category) <= 4):
                messagebox.showwarning("경고", "카테고리 내에 단어를 추가해주세요.")
                return

        if selected_mode == "해석 맞추기":
            mode_1_function(selected_category)
        elif selected_mode == "단어 맞추기":
            mode_1_5_function(selected_category)
        elif selected_mode == "사지선다형 단어 맞추기":
            mode_2_function(selected_category)
        elif selected_mode == "문장 채우기 게임":
            mode_3_function(selected_category)
        elif selected_mode == "산성비 게임":
            mode_4_function(selected_category)
        else:
            print("오류 발생")

    # 시작 버튼 (맨 아래 배치)
    start_button = ttk.Button(root, text="시작", bootstyle="success", command=start_button_clicked)
    start_button.pack(pady=20, padx=150, fill="x")
