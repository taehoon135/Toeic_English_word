import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def settings_window(root):
    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()
    root.title("설정")
    root.geometry("400x500")
    
    label = ttk.Label(root, text="설정 화면", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)
    
    exit_button = ttk.Button(root, text="닫기", bootstyle="danger", command=root.destroy)
    exit_button.pack(pady=20)
    
    

if __name__ == "__main__":
    root = tk.Tk()
    settings_window(root)
    root.mainloop()
