import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def toggle_dark_mode(root):
    current_theme = root.style.theme_use()
    new_theme = "darkly" if current_theme == "flatly" else "flatly"
    root.style.theme_use(new_theme)

def settings_window(root):
    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()
    root.title("설정")
    
    label = ttk.Label(root, text="설정 화면", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)
    
    # 개인정보 표시
    info_frame = ttk.Frame(root)
    info_frame.pack(pady=10)
    ttk.Label(info_frame, text="이름: 홍길동", font=("Arial", 12)).pack()
    ttk.Label(info_frame, text="이메일: example@email.com", font=("Arial", 12)).pack()
    
    # 개인정보 수정 버튼
    edit_button = ttk.Button(root, text="개인정보 수정", bootstyle="info")
    edit_button.pack(pady=10)
    
    # 색반전 모드 버튼
    dark_mode_button = ttk.Button(root, text="색반전 모드", bootstyle="secondary", command=lambda: toggle_dark_mode(root))
    dark_mode_button.pack(pady=10)
    
    # 로그아웃 버튼
    logout_button = ttk.Button(root, text="로그아웃", bootstyle="warning")
    logout_button.pack(pady=10)
    
    # 닫기 버튼
    exit_button = ttk.Button(root, text="닫기", bootstyle="danger", command=root.destroy)
    exit_button.pack(pady=20)

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    settings_window(root)
    root.mainloop()
