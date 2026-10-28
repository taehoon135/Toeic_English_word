import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.word_db import word_db
from database.user_db import user_db

#영어 단어 정확히 일치하는 항목 찾기 (search_words는 부분 일치라 다른 단어가 걸릴 수 있음)
def find_exact_word(english):
    return next((w for w in word_db.search_words(english) if w["english"].lower() == english.lower()), None)

# 관리자 페이지 UI
def admin_window(root, admin_id):
    # 기존 UI 제거
    for widget in root.winfo_children():
        widget.destroy()

    root.title("관리자 페이지")
    root.geometry("440x550")  # ✅ 초기 창 크기 설정 (원래 크기로)

    # 타이틀
    title_label = ttk.Label(root, text="관리자 페이지", font=("Arial", 20, "bold"), bootstyle="dark")
    title_label.pack(pady=30)

    # 버튼 프레임
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    # 단어 추가
    add_button = ttk.Button(btn_frame, text="단어 추가", width=30, bootstyle="success", command=lambda: handle_add_word(root, admin_id))
    add_button.pack(pady=10)

    # 단어 삭제
    delete_button = ttk.Button(btn_frame, text="단어 삭제", width=30, bootstyle="danger", command=lambda: handle_delete_word(root, admin_id))
    delete_button.pack(pady=10)

    # 단어 수정
    update_button = ttk.Button(btn_frame, text="단어 수정", width=30, bootstyle="warning", command=lambda: handle_update_word(root, admin_id))
    update_button.pack(pady=10)

    # 관리자 정보 수정 (root 전달하도록 lambda 사용)
    edit_info_button = ttk.Button(
        btn_frame,
        text="관리자 정보 수정",
        width=30,
        bootstyle="info",
        command=lambda: admin_info_edit(root, admin_id)
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
def admin_info_edit(root, admin_id):
    # 기존 UI 제거
    for widget in root.winfo_children():
        widget.destroy()

    root.title("관리자 정보 수정")

    label = ttk.Label(root, text="관리자 정보 수정", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)

    ID_var = tk.StringVar(value=user_db.get_user_by_id(admin_id)["user_login_id"])
    password_var = tk.StringVar()
    #api_var = tk.StringVar()

    ttk.Label(root, text="아이디").pack()
    ttk.Entry(root, textvariable=ID_var).pack(pady=5)

    ttk.Label(root, text="새 비밀번호").pack()
    ttk.Entry(root, textvariable=password_var, show="*").pack(pady=5)
    
    #ttk.Label(root, text="API KEY (선택사항)").pack()
    #ttk.Entry(root, textvariable=api_var, width=50).pack(pady=5)


    def admin_save_changes():
        new_id = ID_var.get().strip()
        if not new_id:
            messagebox.showwarning("입력 오류", "아이디를 입력해주세요.")
            return
        if not user_db.update_login(admin_id, new_id, password_var.get() or None):
            messagebox.showerror("실패", "이미 사용 중인 아이디입니다.")
            return
        messagebox.showinfo("성공", "관리자 정보가 수정되었습니다.")
        admin_window(root, admin_id)

    save_button = ttk.Button(root, text="저장", bootstyle="success", command=admin_save_changes)
    save_button.pack(pady=10)

    cancel_button = ttk.Button(root, text="취소", bootstyle="danger", command=lambda: admin_window(root, admin_id))
    cancel_button.pack(pady=5)

def add_word_ui(root, admin_id):
    for widget in root.winfo_children():
        widget.destroy()
    
    ttk.Label(root, text="단어 추가", font=("Arial", 18, "bold"), bootstyle="success").pack(pady=20)

    top_bar = ttk.Frame(root)
    top_bar.pack(fill=tk.X, pady=5, padx=10)
    
    labels = ["영어 단어", "뜻", "품사", "예문"]
    entries = {}

    for label in labels:
        ttk.Label(root, text=label).pack()
        entry = ttk.Entry(root, width=50)
        entry.pack(pady=5)
        entries[label] = entry

    def handle_add():
        english = entries["영어 단어"].get().strip()
        meaning = entries["뜻"].get().strip()
        pos = entries["품사"].get().strip()
        example = entries["예문"].get().strip()

        if not english or not meaning:
            messagebox.showwarning("입력 오류", "단어와 뜻은 필수입니다.")
            return

        word_id = word_db.add_word(english, meaning, pos, example)
        if word_id:
            messagebox.showinfo("성공", f"단어가 추가되었습니다 (ID: {word_id})")
            admin_window(root, admin_id)
        else:
            messagebox.showerror("실패", "단어 추가에 실패했습니다.")

    ttk.Button(root, text="추가", bootstyle="success", command=handle_add).pack(pady=10)
    back_button = ttk.Button(top_bar, text="← 뒤로가기", command=lambda: admin_window(root, admin_id), style="Big.TButton")
    back_button.pack(side=tk.RIGHT)
    
def delete_word_ui(root, admin_id):
    for widget in root.winfo_children():
        widget.destroy()

    top_bar = ttk.Frame(root)
    top_bar.pack(fill=tk.X, pady=5, padx=10)
    
    ttk.Label(root, text="단어 삭제", font=("Arial", 18, "bold"), bootstyle="danger").pack(pady=20)

    ttk.Label(root, text="삭제할 단어 입력 (영어)").pack()
    word_entry = ttk.Entry(root, width=50)
    word_entry.pack(pady=5)

    def handle_delete():
        word = word_entry.get().strip()
        if not word:
            messagebox.showwarning("입력 오류", "단어를 입력해주세요.")
            return

        found = find_exact_word(word)
        if not found:
            messagebox.showerror("오류", "해당 단어를 찾을 수 없습니다.")
            return

        if not messagebox.askyesno("단어 삭제", f"'{found['english']}' 단어를 삭제하시겠습니까?"):
            return
        word_id = found["word_id"]
        success = word_db.delete_word(word_id)
        if success:
            messagebox.showinfo("성공", f"단어(ID {word_id})가 삭제되었습니다.")
            admin_window(root, admin_id)
        else:
            messagebox.showerror("실패", "단어 삭제에 실패했습니다.")

    ttk.Button(root, text="삭제", bootstyle="danger", command=handle_delete).pack(pady=10)
    back_button = ttk.Button(top_bar, text="← 뒤로가기", command=lambda: admin_window(root, admin_id), style="Big.TButton")
    back_button.pack(side=tk.RIGHT)
    
# 단어 수정 UI
def update_word_ui(root, admin_id):
    for widget in root.winfo_children():
        widget.destroy()

    top_bar = ttk.Frame(root)
    top_bar.pack(fill=tk.X, pady=5, padx=10)
    
    ttk.Label(root, text="단어 수정", font=("Arial", 18, "bold"), bootstyle="warning").pack(pady=20)

    # 수정할 단어명 입력
    ttk.Label(root, text="수정할 단어 입력 (영어)").pack()
    search_entry = ttk.Entry(root, width=50)
    search_entry.pack(pady=5)

    def load_word():
        word = search_entry.get().strip()
        if not word:
            messagebox.showwarning("입력 오류", "단어를 입력해주세요.")
            return

        word_info = find_exact_word(word)
        if not word_info:
            messagebox.showerror("오류", "해당 단어를 찾을 수 없습니다.")
            return

        show_update_form(word_info)

    def show_update_form(word_info):
        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text="단어 수정", font=("Arial", 18, "bold"), bootstyle="warning").pack(pady=20)

        entries = {}
        fields = {
            "영어 단어": word_info["english"],
            "뜻": word_info["meaning"],
            "품사": word_info.get("part_of_speech") or "",
            "예문": word_info.get("example_sentence") or ""
        }

        for label, value in fields.items():
            ttk.Label(root, text=label).pack()
            entry = ttk.Entry(root, width=50)
            entry.insert(0, value)
            entry.pack(pady=5)
            entries[label] = entry

        def handle_update():
            new_word = entries["영어 단어"].get().strip()
            meaning = entries["뜻"].get().strip()
            pos = entries["품사"].get().strip()
            example = entries["예문"].get().strip()

            if not new_word or not meaning:
                messagebox.showwarning("입력 오류", "단어와 뜻은 필수입니다.")
                return

            success = word_db.update_word(word_info["word_id"], new_word, meaning, pos, example)
            if success:
                messagebox.showinfo("성공", "단어가 수정되었습니다.")
                admin_window(root, admin_id)
            else:
                messagebox.showerror("실패", "단어 수정에 실패했습니다.")

        ttk.Button(root, text="수정", bootstyle="warning", command=handle_update).pack(pady=10)
        ttk.Button(root, text="뒤로가기", bootstyle="secondary outline", command=lambda: admin_window(root, admin_id)).pack(pady=5)

    ttk.Button(root, text="불러오기", bootstyle="info", command=load_word).pack(pady=10)
    back_button = ttk.Button(top_bar, text="← 뒤로가기", command=lambda: admin_window(root, admin_id), style="Big.TButton")
    back_button.pack(side=tk.RIGHT)



def handle_add_word(root, admin_id):
    add_word_ui(root, admin_id)

def handle_delete_word(root, admin_id):
    delete_word_ui(root, admin_id)

def handle_update_word(root, admin_id):
    update_word_ui(root, admin_id)
