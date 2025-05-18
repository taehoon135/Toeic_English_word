import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd

admin_info = {
    "ID": "1234",
    "password": "1234"
}

# 메뉴로 이동 함수: root 인자를 받도록 수정
def go_to_menu(root):
    from menu import main_menu
    main_menu(root)

# 관리자 페이지 UI
def admin_window(root):
    # 기존 UI 제거
    for widget in root.winfo_children():
        widget.destroy()

    root.title("관리자 페이지")

    # 타이틀
    title_label = ttk.Label(root, text="관리자 페이지", font=("Arial", 20, "bold"), bootstyle="dark")
    title_label.pack(pady=30)

    # 버튼 프레임
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    # 단어 추가
    add_button = ttk.Button(btn_frame, text="단어 추가", width=30, bootstyle="success", command=lambda: handle_add_word(root))
    add_button.pack(pady=10)

    # 단어 삭제
    delete_button = ttk.Button(btn_frame, text="단어 삭제", width=30, bootstyle="danger", command=lambda: handle_delete_word(root))
    delete_button.pack(pady=10)

    # 단어 수정
    update_button = ttk.Button(btn_frame, text="단어 수정", width=30, bootstyle="warning", command=lambda: handle_update_word(root))
    update_button.pack(pady=10)

    # 관리자 정보 수정 (root 전달하도록 lambda 사용)
    edit_info_button = ttk.Button(
        btn_frame,
        text="관리자 정보 수정",
        width=30,
        bootstyle="info",
        command=lambda: admin_info_edit(root)
    )
    edit_info_button.pack(pady=10)

    # 로그아웃 버튼: 로그인 화면으로 이동
    from login import sign_login
    logout_button = ttk.Button(
        root,
        text="로그아웃",
        bootstyle="danger",
        command=lambda: sign_login(root)
    )
    logout_button.pack(pady=10)

# 관리자 정보 수정 UI
def admin_info_edit(root):
    # 기존 UI 제거
    for widget in root.winfo_children():
        widget.destroy()

    root.title("관리자 정보 수정")

    label = ttk.Label(root, text="관리자 정보 수정", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)

    ID_var = tk.StringVar(value=admin_info["ID"])
    password_var = tk.StringVar()

    ttk.Label(root, text="아이디").pack()
    ttk.Entry(root, textvariable=ID_var).pack(pady=5)

    ttk.Label(root, text="새 비밀번호").pack()
    ttk.Entry(root, textvariable=password_var, show="*").pack(pady=5)

    def admin_save_changes():
        admin_info["ID"] = ID_var.get()
        if password_var.get():
            admin_info["password"] = password_var.get()
        admin_window(root)

    save_button = ttk.Button(root, text="저장", bootstyle="success", command=admin_save_changes)
    save_button.pack(pady=10)

    cancel_button = ttk.Button(root, text="취소", bootstyle="danger", command=lambda: admin_window(root))
    cancel_button.pack(pady=5)

import pandas as pd

def add_word_ui(root):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="단어 추가", font=("Arial", 18, "bold"), bootstyle="primary").pack(pady=20)

    ttk.Label(root, text="단어를 입력하세요 \n(예: adaptable,적응력 있는,adjective,She is very adaptable to new situations.)").pack(pady=10)
    entry = ttk.Entry(root, width=100)
    entry.pack(pady=5)

    def add_word_to_csv_with_input():
        csv_path = "toeic_words.csv"
        parts = [p.strip() for p in entry.get().split(",")]

        if len(parts) != 4:
            messagebox.showerror("입력 오류", "형식이 잘못되었습니다.\n예: adaptable,적응력 있는,adjective,She is very adaptable to new situations.")
            return

        new_word = {
            "english": parts[0],
            "meaning": parts[1],
            "part_of_speech": parts[2],
            "example_sentence": parts[3]
        }

        try:
            df = pd.read_csv(csv_path)
            df = df.append(new_word, ignore_index=True)
            df = df.sort_values(by="english")
            df.to_csv(csv_path, index=False, encoding="utf-8")
            messagebox.showinfo("성공", f"단어 '{new_word['english']}'가 추가되었습니다.")
            admin_window(root)  # 저장 후 관리자 메뉴로 이동
        except Exception as e:
            messagebox.showerror("오류", f"CSV 처리 중 오류 발생:\n{e}")

    ttk.Button(root, text="추가", bootstyle="success", command=add_word_to_csv_with_input).pack(pady=10)
    ttk.Button(root, text="뒤로가기", bootstyle="secondary outline", command=lambda: admin_window(root)).pack(pady=5)

def delete_word_ui(root):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="단어 삭제", font=("Arial", 18, "bold"), bootstyle="danger").pack(pady=20)

    ttk.Label(root, text="삭제할 단어 입력 (예: adaptable)").pack(pady=10)
    word_entry = ttk.Entry(root, width=50)
    word_entry.pack(pady=5)

    def delete_word():
        word_to_delete = word_entry.get().strip()
        if not word_to_delete:
            messagebox.showerror("오류", "삭제할 단어를 입력하세요.")
            return

        try:
            df = pd.read_csv("toeic_words.csv")
            original_len = len(df)
            df = df[df['english'] != word_to_delete]

            if len(df) == original_len:
                messagebox.showwarning("실패", f"'{word_to_delete}' 단어가 존재하지 않습니다.")
            else:
                df.to_csv("toeic_words.csv", index=False, encoding="utf-8")
                messagebox.showinfo("성공", f"'{word_to_delete}' 단어가 삭제되었습니다.")
                admin_window(root)

        except Exception as e:
            messagebox.showerror("오류", f"삭제 중 오류 발생: {e}")

    ttk.Button(root, text="삭제", bootstyle="danger", command=delete_word).pack(pady=10)
    ttk.Button(root, text="뒤로가기", bootstyle="secondary outline", command=lambda: admin_window(root)).pack(pady=5)

def update_word_ui(root):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="단어 수정", font=("Arial", 18, "bold"), bootstyle="warning").pack(pady=20)

    ttk.Label(root, text="수정할 단어 입력 (예: adaptable)").pack(pady=10)
    search_entry = ttk.Entry(root, width=50)
    search_entry.pack(pady=5)

    def load_word():
        target_word = search_entry.get().strip()
        try:
            df = pd.read_csv("toeic_words.csv")
            match = df[df['english'] == target_word]

            if match.empty:
                messagebox.showwarning("실패", f"'{target_word}' 단어가 존재하지 않습니다.")
                return

            for widget in root.winfo_children():
                widget.destroy()

            ttk.Label(root, text=f"'{target_word}' 단어 수정", font=("Arial", 18, "bold"), bootstyle="warning").pack(pady=20)

            meaning_var = tk.StringVar(value=match.iloc[0]['meaning'])
            pos_var = tk.StringVar(value=match.iloc[0]['part_of_speech'])
            example_var = tk.StringVar(value=match.iloc[0]['example_sentence'])

            ttk.Label(root, text="뜻").pack()
            ttk.Entry(root, textvariable=meaning_var).pack(pady=3)

            ttk.Label(root, text="품사").pack()
            ttk.Entry(root, textvariable=pos_var).pack(pady=3)

            ttk.Label(root, text="예문").pack()
            ttk.Entry(root, textvariable=example_var, width=80).pack(pady=3)

            def save_update():
                df.loc[df['english'] == target_word, ['meaning', 'part_of_speech', 'example_sentence']] = [
                    meaning_var.get(),
                    pos_var.get(),
                    example_var.get()
                ]
                df = df.sort_values(by="english")
                df.to_csv("toeic_words.csv", index=False, encoding="utf-8")
                messagebox.showinfo("성공", f"'{target_word}' 단어가 수정되었습니다.")
                admin_window(root)

            ttk.Button(root, text="저장", bootstyle="success", command=save_update).pack(pady=10)
            ttk.Button(root, text="취소", bootstyle="danger", command=lambda: admin_window(root)).pack(pady=5)

        except Exception as e:
            messagebox.showerror("오류", f"불러오기 중 오류 발생: {e}")

    ttk.Button(root, text="불러오기", bootstyle="info", command=load_word).pack(pady=10)
    ttk.Button(root, text="뒤로가기", bootstyle="secondary outline", command=lambda: admin_window(root)).pack(pady=5)


def handle_add_word(root):
    add_word_ui(root)

def handle_delete_word(root):
    delete_word_ui(root)

def handle_update_word(root):
    update_word_ui(root)
    

