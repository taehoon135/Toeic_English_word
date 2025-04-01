import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_menu(root):
    # 기존 UI 삭제 (기존 창을 유지한 채 변경)
    for widget in root.winfo_children():
        widget.destroy()

    from quiz_interpret import quiz_interpret

    def go_to_menu(root): # 수정해야함
        for widget in root.winfo_children():
            widget.destroy()
        from menu import main_menu
        main_menu(root)  # 메뉴 화면으로 이동

    # 홈 버튼 (오른쪽 상단)
    home_button = ttk.Button(root, text="🏠 홈", bootstyle="secondary", command=go_to_menu)
    home_button.pack(anchor="ne", padx=10, pady=10)

    # 옵션 선택 (OptionMenu)
    option_var = tk.StringVar(value="Category 1")
    options = ["Category 1", "Category 1", "Category 2", "Category 3", "Category 4"]
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

    def handle_mode_change(selected_mode):
        index = modes.index(selected_mode) - 1
        if index < 0:
            index += 1
        label_display1.config(text=mode_explain[index])

    mode_menu = ttk.OptionMenu(root, mode_var, *modes, command=handle_mode_change)
    mode_menu.pack(pady=10)

    # 라벨을 위한 프레임 생성
    frame_display = ttk.Frame(root)
    frame_display.pack(pady=20)

    label_display1 = ttk.Label(
        frame_display,
        text=mode_explain[0],
        font=("나눔고딕", 16, "bold"),
        foreground="#3F7D58",
        wraplength=250,
        justify="center"
    )
    label_display1.pack(pady=20, fill="both", expand=True)

    # Start 버튼 클릭 시 실행될 함수
    def start_button_clicked():
        selected_mode = mode_var.get()
        selected_category = option_var.get()
        print(f"Start 버튼 클릭됨! 선택된 카테고리: {selected_category}, 모드: {selected_mode}")

        if selected_mode == "해석 맞추기":
            print("Mode 1 실행 중...")
        elif selected_mode == "단어 맞추기":
            quiz_interpret(root)
        elif selected_mode == "산성비 게임":
            print("Mode 3 실행 중...")
        elif selected_mode == "문장 채우기 게임":
            print("Mode 4 실행 중...")
        else:
            print("올바른 모드를 선택해주세요.")

    # 시작 버튼
    start_button = ttk.Button(root, text="시작", bootstyle="success", command=start_button_clicked)
    start_button.pack(pady=20, padx=120, fill="x")


if __name__ == "__main__":
    quiz_menu()