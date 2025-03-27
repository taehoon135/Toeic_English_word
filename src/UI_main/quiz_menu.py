import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# 현재 테마 상태 변수
current_theme = "flatly"  # 기본 테마 (라이트 모드)

# 메인 윈도우 생성
root = ttk.Window(themename=current_theme)  # ttkbootstrap 사용
root.title("영단어 학습 프로그램")
root.geometry("320x450")
root.resizable(False, False)

# 스타일 설정
style = ttk.Style()
style.configure("Placeholder.TEntry", foreground="gray")
style.configure("Normal.TEntry", foreground="black")

def quiz_menu():
    from quiz_interpret import quiz_interpret

    def go_to_menu():
        root.quit()
        #menu() 메뉴화면으로 이동하면서 현재 root는 종료

    # 홈 버튼 (오른쪽 상단)
    home_button = ttk.Button(root, text="🏠 홈", bootstyle="secondary", command=go_to_menu)
    home_button.pack(anchor="ne", padx=10, pady=10)

    # 옵션 선택 (OptionMenu)
    option_var = tk.StringVar(value="Category 1")
    options = ["Category 1", "Category 1", "Category 2", "Category 3", "Category 4"]

    #가젯 생성
    option_menu = ttk.OptionMenu(root, option_var, *options)
    option_menu.pack(pady=10)

    # 모드 선택 (OptionMenu)
    mode_var = tk.StringVar(value="Select Mode")
    modes = ["해석 맞추기", "해석 맞추기", "단어 맞추기", "산성비 게임", "문장 채우기 게임"]

    mode_explain = [
            "해석 -> 단어 모드:\n사용자가 화면에 나오는 해석을 보고 단어를 입력해서 정답을 맞추는 게임.",
            "단어 -> 해석 모드:\n사용자가 화면에 나오는 단어를 보고 해석을 입력해서 정답을 맞추는 게임.",
            "산성비 게임:\n사용자가 화면에서 내려오는 해석을 보고 빠르게 단어를 입력하여 정답을 맞추는 게임.",
            "문장 채우기게임\n사용자가 화면의 문장을 보고 빈칸에 알맞은 단어를 입력하여 정답을 맞추는 게임."
        ]

    # 모드 변경 시 출력
    def handle_mode_change(selected_mode):
        #인덱스 검색
        index = modes.index(selected_mode) - 1 #mode1이 중복되므로 하나 줄여야 함
        if (index < 0):
            index += 1
        
        label_display1.config(text= mode_explain[index])

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
        text=mode_explain[0],  # 모드에 따른 설명 텍스트
        font=("나눔고딕", 16, "bold"),  # 글꼴 설정
        foreground="#3F7D58",
        bootstyle="info",  # 버튼 스타일
        wraplength=250,  # 텍스트가 자동으로 줄바꿈되도록 설정
        justify="center",  # 텍스트 중앙 정렬
        anchor="center",  # 텍스트 중앙 정렬
    
    )
    label_display1.pack(pady=20, fill="both", expand=True)

    # 모드에 따라 다른 함수 실행
    def mode_1_function():
        print("Mode 1 실행 중...")

    def mode_2_function():
        quiz_interpret(root)

    def mode_3_function():
        print("Mode 3 실행 중...")

    def mode_4_function():
        print("Mode 4 실행 중...")

    # Start 버튼 클릭 시 실행될 함수
    def start_button_clicked():
        selected_mode = mode_var.get()
        selected_category = option_var.get()
        
        print(f"Start 버튼 클릭됨! 선택된 카테고리: {selected_category}, 모드: {selected_mode}")

        if selected_mode == "해석 맞추기":
            mode_1_function()
        elif selected_mode == "단어 맞추기":
            mode_2_function()
        elif selected_mode == "산성비 게임":
            mode_3_function()
        elif selected_mode == "문장 채우기 게임":
            mode_4_function()
        else:
            print("올바른 모드를 선택해주세요.")

    # 시작 버튼 (맨 아래 배치)
    start_button = ttk.Button(root, text="시작", bootstyle="success", command=start_button_clicked)
    start_button.pack(pady=20, padx=120, fill="x")

quiz_menu()

# Tkinter 이벤트 루프 실행
root.mainloop()
