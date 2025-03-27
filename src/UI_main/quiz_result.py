import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_result(root, word_list, word_list_answer):

    for widget in root.winfo_children():
            widget.destroy()  

    # 마우스 휠 스크롤 이벤트 함수
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    root.geometry("600x600")

    # 결과 프레임 (스크롤 포함)
    result_frame = tk.Frame(root, bg="white", relief="solid", bd=1)
    result_frame.place(x=20, y=20, width=500, height=500)

    canvas = tk.Canvas(result_frame, bg="white")
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas, bg="white")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 마우스 휠 스크롤 이벤트 바인딩
    root.bind("<MouseWheel>", on_mouse_wheel)

    def go_to_main_menu():
        root.quit()
        #main_menu()

    # 카테고리 리스트를 데이터베이스에서 받았다고 가정
    categories = ["전체", "카테고리2", "카테고리3", "카테고리4"]

    # 단어 리스트 출력
    for i, (word, meaning, mistakes, category) in enumerate(word_list):
        # 카테고리 (OptionMenu)
        #if (category not in categories):
        #   category = categories[0]

        category_var = tk.StringVar()
        category_var.set(category)  # 기본 선택값을 명시적으로 설정

        category_menu = ttk.OptionMenu(scrollable_frame, category_var, category, *categories)
        category_menu.grid(row=i, column=0, padx=12, pady=5)
        
        # 단어 (조금 오른쪽으로 이동)
        tk.Label(scrollable_frame, text=word, width=15, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=1, padx=15, pady=5)
        
        # 단어 해석
        tk.Label(scrollable_frame, text=meaning, width=10, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=2, padx=5, pady=5)
        
        # 오답 횟수
        tk.Label(scrollable_frame, text=f"{mistakes}회", width=5, anchor="center", bg="white", font=("Arial", 10)).grid(row=i, column=3, padx=5, pady=5)
        
        # 정답 여부 (O/X)
        if (word_list_answer[i] == 1): #맞춘 케이스
            correctness_label = tk.Label(scrollable_frame, text="O", width=5, anchor="center", bg="white", font=("Arial", 10, "bold"))
            correctness_label.grid(row=i, column=4, padx=5, pady=5)
        elif (word_list_answer[i] == 0): #틀린 케이스
            correctness_label = tk.Label(scrollable_frame, text="X", width=5, anchor="center", bg="white", font=("Arial", 10, "bold"))
            correctness_label.grid(row=i, column=4, padx=5, pady=5)

    # 종료 버튼
    exit_btn = ttk.Button(root, text="메인 메뉴", bootstyle="success", command=go_to_main_menu)
    exit_btn.place(x=440, y=540)
