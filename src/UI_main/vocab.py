import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, font
from tkinter import PhotoImage
import pyttsx3

def vocab_window(root, user_number):
    from menu import main_menu
    from category_manage import category_manage
    from assist_module import category_id_search, word_id_search

    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()
    root.title("단어장")

    #뒤로가기
    def go_to_menu():
        main_menu(root, user_number)

    #DB연결
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.word_db import WordDB

    word_db = WordDB() #데베 클래스 생성
    words = word_db.get_all_words()

    # 카테고리 연결
    from database.category_db import CategoryDB
    category_db = CategoryDB()

    filtered_words = words.copy()

    # 단어 테이블 업데이트
    def update_word_table():
        for row in word_table.get_children():
            word_table.delete(row)
        for item in filtered_words: 
            word_table.insert("", "end", values=(item["word_id"], item["english"], item["meaning"], item["part_of_speech"]))

    # 검색 기능
    def search_word():
        keyword = search_var.get().lower() #입력된 값
        category = selected_category.get() #선택된 카테고리

        nonlocal filtered_words
        filtered_words = []

        if (category == "전체"):
            for w in words:
                if keyword in w["english"].lower():
                    filtered_words.append(w)
        else:
            #카테고리 번호 찾기
            category_id = category_id_search(user_number, category)
            if category_id == -1:
                print("오류 발생")
                return

            #카테고리 아이디로 카테고리 속한 단어들 검색
            search_category_list = category_db.get_words_in_category(category_id)
            
            for w in words:
                #입력한 값이 테이블에 있다면, 카테고리가 전체거나 일치하면 검색에 포함
                if keyword in w['english'].lower() and any(w['english'] == s['english'] for s in search_category_list):
                    filtered_words.append(w)

        update_word_table()
        detail_text.set("")

    # 카테고리 변경 시
    def on_category_change(value):
        search_word()

    #카테고리에 단어 추가
    def confirm_category_change():
        selected = word_table.focus()
        if selected:
            data = word_table.item(selected, "values")

            #선택된 카테고리 이름으로 카테고리 번호 조회
            category_data = selected_word_category.get() #선택된 카테고리
            #선택된 카테고리가 없으면 아무것도 하지 않음
            if (category_data == "전체"):
                return 

            #카테고리 번호 찾기
            category_number = category_id_search(user_number, category_data)
            if category_number == -1:
                print("오류 발생")
                return

            #카테고리 아이디, 워드 아이디
            success = category_db.add_word_to_category(category_number, data[0]) #카테고리 업데이트
            if success:
                messagebox.showinfo("성공", "카테고리가 업데이트 되었습니다.")
            else:
                messagebox.showwarning("경고", "실패")

    #단어 클릭 시 하단에 정보 출력
    def on_row_click(event):
        selected = word_table.focus()
        if selected:
            data = word_table.item(selected, "values")

            #단어 이름으로 단어 튜플을 통째로 찾음
            for w in filtered_words:
                if w["english"] == data[1]:
                    word = w
                    break

            if word:
                detail_text.set(f"품사: {word['part_of_speech']}\n예문: {word['example_sentence']}\n오답 횟수: {word['wrong_count']}")

                # 카테고리는 무조건 "전체"로 고정 표시
                selected_word_category.set("전체")

                # 숨겨진 옵션 메뉴와 버튼을 보여줌
                # 버튼이 이미 보이면 중복 pack 방지
                if not option_row.winfo_ismapped():
                    option_row.pack(anchor="w", padx=20, pady=20, side=tk.BOTTOM)
    
    #음성 듣기
    def listen_word():
        selected = word_table.focus()
        data = word_table.item(selected, "values")
        #data의 1번이 word

        engine = pyttsx3.init()
        engine.setProperty('rate', 200)
        engine.say(data[1])
        engine.runAndWait()

        #print(data[1])

    def go_to_category_manage():
        category_manage(root, user_number)

    # GUI 시작
    root.title("단어장")
    root.geometry("500x600")

    # ===== 폰트 설정 =====
    big_font = font.Font(family="맑은 고딕", size=13)
    tree_font = font.Font(family="맑은 고딕", size=13)

    # ===== 스타일 설정 =====
    style = ttk.Style()
    style.configure("Custom.Treeview", font=tree_font, rowheight=32)
    style.configure("Big.TButton", font=big_font)

    # 상단바 (카테고리 + 뒤로가기)
    top_bar = ttk.Frame(root)
    top_bar.pack(fill=tk.X, pady=5, padx=10)

    #카테고리 생성 부분
    category_list = category_db.get_user_categories(user_number)
    category_only_name = ["임시"] #카테고리 이름만을 포함하는 리스트 생성
    for category in category_list:
        category_only_name.append(category["name"])
    #전체를 맨 앞으로 보냄
    category_only_name.remove("전체")
    category_only_name.insert(0, "전체")
    categories = category_only_name
    
    selected_category = tk.StringVar(value="전체")
    category_menu = ttk.OptionMenu(top_bar, selected_category, selected_category.get(), *categories, command=on_category_change)
    category_menu.pack(side=tk.LEFT)

    back_button = ttk.Button(top_bar, text="← 뒤로가기", command=go_to_menu, style="Big.TButton")
    back_button.pack(side=tk.RIGHT)

    # 검색창 프레임
    search_frame = ttk.Frame(root)
    search_frame.pack(fill=tk.X, padx=10)

    # 첫 번째 줄: 검색 입력창 + 검색 버튼
    search_row1 = ttk.Frame(search_frame)
    search_row1.pack(fill=tk.X)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_row1, textvariable=search_var, font=big_font)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    search_button = ttk.Button(search_row1, text="검색", command=search_word, style="Big.TButton")
    search_button.pack(side=tk.LEFT, padx=5)

    # 두 번째 줄: 오른쪽 정렬된 카테고리 버튼
    search_row2 = ttk.Frame(search_frame)
    search_row2.pack(fill=tk.X)

    category_button = ttk.Button(search_row2, text="카테고리 관리", command=go_to_category_manage, style="Big.TButton")
    category_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # 단어 테이블
    table_frame = ttk.Frame(root)
    table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    columns = ("id", "english", "meaning", "part_of_speech")
    word_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Custom.Treeview")  #단어 보여주는 목록 길이
    word_table.heading("id", text="ID")
    word_table.heading("english", text="단어")
    word_table.heading("meaning", text="의미")
    word_table.heading("part_of_speech", text="품사")
    word_table.column("id", width=50, anchor="center")
    word_table.column("english", width=150, anchor="center")
    word_table.column("meaning", width=150, anchor="center")
    word_table.column("part_of_speech", width=80, anchor="center")
    word_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    word_table.bind("<<TreeviewSelect>>", on_row_click)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=word_table.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    word_table.configure(yscrollcommand=scrollbar.set)

    # 상세 정보
    detail_frame = ttk.LabelFrame(root, text="단어 정보", labelanchor="n")
    detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    detail_text = tk.StringVar()
    detail_label = ttk.Label(detail_frame, textvariable=detail_text, justify=tk.LEFT, font=big_font)
    detail_label.pack(anchor="w", padx=10, pady=10, fill="x")

    # === 카테고리 OptionMenu + 확인 버튼 ===
    option_row = ttk.Frame(detail_frame)
    option_row.pack(fill="x", padx=10, pady=(0,10))
    option_row.pack_forget()  # 처음엔 안 보이게

    option_row.grid_columnconfigure(2, weight=1)  # 중간 여백

    selected_word_category = tk.StringVar(value="전체")
    category_option = ttk.OptionMenu(option_row, selected_word_category, "전체", *categories)
    category_option.grid(row=0, column=0, sticky="w", padx=(0, 10))  # ← 간격 추가

    confirm_button = ttk.Button(option_row, text="확인", command=confirm_category_change)
    confirm_button.grid(row=0, column=1, sticky="w")

    # 소리 듣기 버튼 (tk.Button 사용)
    check_img = PhotoImage(file="C:\\github\\sw-egineering\\src\\UI_main\\asset\\z.sound.png")
    sound_button = tk.Button(
        option_row,
        image=check_img,
        command=listen_word,
        borderwidth=0,
        highlightthickness=0,
        relief="flat",
        background=root["background"]  # 배경색 맞추기 (선택)
    )
    sound_button.image = check_img  # GC 방지
    sound_button.grid(row=0, column=3, sticky="w", padx=270)

    # 초기 단어 표시
    update_word_table()