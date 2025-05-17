import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_result(root, user_number, word_list, word_list_answer):
    # 메인 메뉴 함수 import
    from menu import main_menu

    # 기존 창의 모든 위젯 제거 (화면 초기화)
    for widget in root.winfo_children():
        widget.destroy()

    # 창 크기 설정
    root.geometry("500x600")

    # 결과를 표시할 프레임 생성 및 배치
    result_frame = ttk.Frame(root)
    result_frame.place(x=10, y=20, width=480, height=500)

    # Treeview에 표시할 컬럼 정의 ('mistakes'는 제거됨)
    columns = ("Word", "Meaning", "correctness")

    # Treeview 위젯 생성
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20, style="Custom.Treeview")

    # 각 컬럼의 헤더와 너비 설정
    for col, width in zip(columns, [110, 110, 80]):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    # Treeview 배치
    tree.pack(side="left", fill="both", expand=True)

    # 스크롤바 생성 및 Treeview에 연결
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Treeview에 단어 데이터 삽입
    for i, word_info in enumerate(word_list):
        word = word_info["english"]
        meaning = word_info["meaning"]
        correctness = "O" if word_list_answer[i] == 1 else "X"  # 정답 여부 표시
        tree.insert("", "end", iid=i, values=(word, meaning, correctness))

    # '메인 메뉴' 버튼 클릭 시 실행되는 함수
    def go_to_main_menu():
        main_menu(root, user_number)

    # '메인 메뉴' 버튼 생성 및 배치
    exit_btn = ttk.Button(root, text="메인 메뉴", bootstyle="success", command=go_to_main_menu)
    exit_btn.place(x=370, y=540)