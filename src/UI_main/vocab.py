import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def vocab_window(root):
    for widget in root.winfo_children():  # 기존 UI 제거
        widget.destroy()
    root.title("단어장")
    
    label = ttk.Label(root, text="단어장 화면", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)
    
    exit_button = ttk.Button(root, text="닫기", bootstyle="danger", command=root.destroy)
    exit_button.pack(pady=20)
    
    root.mainloop()
    
    

if __name__ == "__main__":
    vocab_window()
    
