import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox

def vocab_window(root):
    from menu import main_menu

    #DB연결
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  #나보다 위 디렉토리에 있음

    import sqlite3
    from DB_module.wordbook import Wordbook

    # DB 연결
    conn = sqlite3.connect("toeic_vocab.db")

    # 사용자 정보 (예시로 admin 넣음)
    user_info = {
        "user_id": "admin",
        "username": "관리자",
        "is_admin": True
    }

    # Wordbook 인스턴스 생성
    wb = Wordbook(conn, user_info)

    # 단어 받기
    words = wb.show_word_list

    # DB 연결 종료
    #conn.close()


    # wb = Wordbook()  #클래스 가져오기
    # wb.show_word_list

    # for widget in root.winfo_children():  # 기존 UI 제거
    #     widget.destroy()
    # root.title("단어장")

    # def go_to_menu():
    #     main_menu(root)
    
    # label = ttk.Label(root, text="단어장 화면", font=("Arial", 18, "bold"), bootstyle="primary")
    # label.pack(pady=20)
    
    # exit_button = ttk.Button(root, text="닫기", bootstyle="danger", command=go_to_menu)
    # exit_button.pack(pady=20)
from tkinter import ttk, font
#ttest

#단어 데이터
# words = [
#     {"id": 1, "word": "apple", "meaning": "사과", "pos": "명사", "example": "I ate an apple.", "category": "과일", "wrong_count": 0},
#     {"id": 2, "word": "run", "meaning": "달리다", "pos": "동사", "example": "She runs fast.", "category": "동작", "wrong_count": 2},
#     {"id": 3, "word": "blue", "meaning": "파란", "pos": "형용사", "example": "The sky is blue.", "category": "색상", "wrong_count": 1},
#     {"id": 4, "word": "dog", "meaning": "개", "pos": "명사", "example": "Dogs are friendly.", "category": "동물", "wrong_count": 3},
# ]

#DB연결
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  #나보다 위 디렉토리에 있음

import sqlite3
from DB_module.wordbook import Wordbook

# DB 연결
conn = sqlite3.connect("toeic_vocab.db")

# 사용자 정보 (예시로 admin 넣음)
user_info = {
    "user_id": "admin",
    "username": "관리자",
    "is_admin": True
}

# Wordbook 인스턴스 생성
wb = Wordbook(conn, user_info)

wb.show_wordbook_menu()

# 단어 받기
words = wb.show_word_list()

print(words)

filtered_words = words.copy()

# 단어 테이블 업데이트
def update_word_table():
    for row in word_table.get_children():
        word_table.delete(row)
    for item in filtered_words:
        word_table.insert("", "end", values=(item["id"], item["word"], item["meaning"], item["wrong_count"]))

# 단어 클릭 시 상세 정보 표시
def on_row_click(event):
    selected = word_table.focus()
    if selected:
        data = word_table.item(selected, "values")
        word = next((w for w in filtered_words if str(w["id"]) == data[0]), None)
        if word:
            detail_text.set(f"품사: {word['pos']}\n예문: {word['example']}")

# 검색 기능
def search_word():
    keyword = search_var.get().lower()
    category = selected_category.get()
    global filtered_words
    filtered_words = [
        w for w in words
        if keyword in w['word'].lower()
        and (category == "전체" or w["category"] == category)
    ]
    update_word_table()
    detail_text.set("")

# 카테고리 변경 시
def on_category_change(cat):
    search_word()

# 뒤로가기 버튼
def go_back():
    print("뒤로가기 클릭됨")

#카테고리에 단어 추가
def confirm_category_change():
    selected = word_table.focus()
    if selected:
        data = word_table.item(selected, "values")
        word = next((w for w in filtered_words if str(w["id"]) == data[0]), None)
        if word:
            word["category"] = selected_word_category.get()
            print(f"{word['word']} → 카테고리 변경: {word['category']}")

#단어 선택시 카테고리 선택과 확인버튼
def on_row_click(event):
    selected = word_table.focus()
    if selected:
        data = word_table.item(selected, "values")
        word = next((w for w in filtered_words if str(w["id"]) == data[0]), None)
        if word:
            detail_text.set(f"품사: {word['pos']}\n예문: {word['example']}")
            selected_word_category.set(word["category"])

            # 카테고리는 무조건 "전체"로 고정 표시
            selected_word_category.set("전체")

            # 숨겨진 옵션 메뉴와 버튼을 보여줌
            # 버튼이 이미 보이면 중복 pack 방지
            if not option_row.winfo_ismapped():
                option_row.pack(anchor="w", padx=20, pady=20, side=tk.BOTTOM)

# GUI 시작
root = tk.Tk()
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

categories = ["전체", "과일", "동작", "색상", "동물"]
selected_category = tk.StringVar(value="전체")
category_menu = ttk.OptionMenu(top_bar, selected_category, selected_category.get(), *categories, command=on_category_change)
category_menu.pack(side=tk.LEFT)

back_button = ttk.Button(top_bar, text="← 뒤로가기", command=go_back, style="Big.TButton")
back_button.pack(side=tk.RIGHT)

# 검색창
search_frame = ttk.Frame(root)
search_frame.pack(fill=tk.X, padx=10)

search_var = tk.StringVar()
search_entry = ttk.Entry(search_frame, textvariable=search_var, font=big_font)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="검색", command=search_word, style="Big.TButton")
search_button.pack(side=tk.LEFT, padx=5)

# 단어 테이블
table_frame = ttk.Frame(root)
table_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

columns = ("id", "word", "meaning", "wrong_count")
word_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12, style="Custom.Treeview")  #단어 보여주는 목록 길이
word_table.heading("id", text="ID")
word_table.heading("word", text="단어")
word_table.heading("meaning", text="의미")
word_table.heading("wrong_count", text="틀린 수")
word_table.column("id", width=50, anchor="center")
word_table.column("word", width=150, anchor="center")
word_table.column("meaning", width=150, anchor="center")
word_table.column("wrong_count", width=80, anchor="center")
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
detail_label.pack(anchor="w", padx=10, pady=10)

# === 카테고리 OptionMenu + 확인 버튼 ===
option_row = ttk.Frame(detail_frame)
option_row.pack(anchor="w", padx=10, pady=(0,10))
option_row.pack_forget()  # 처음엔 안 보이게

selected_word_category = tk.StringVar(value="전체")
category_option = ttk.OptionMenu(option_row, selected_word_category, "전체", *categories)
category_option.pack(side=tk.LEFT)

confirm_button = ttk.Button(option_row, text="확인", command=confirm_category_change)
confirm_button.pack(side=tk.RIGHT)

# 초기 단어 표시
update_word_table()

root.mainloop()

