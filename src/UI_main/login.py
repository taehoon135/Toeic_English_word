import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def sign_login(root):
    from create_account import register

    # Placeholder 설정 함수 (비밀번호 입력 포함)
    def set_placeholder(entry_widget, placeholder_text, is_password=False):
        """입력 필드에 플레이스홀더를 설정 (비밀번호 필드 대응)"""
        entry_widget.insert(0, placeholder_text)
        entry_widget.has_placeholder = True  # 플레이스홀더 활성화 상태 저장
        entry_widget.config(style="Placeholder.TEntry")  # 회색 텍스트 스타일

        def on_focus_in(event):
            """클릭하면 플레이스홀더 제거"""
            if entry_widget.has_placeholder:
                entry_widget.delete(0, tk.END)
                entry_widget.config(style="Normal.TEntry")  # 검은색 텍스트 스타일
                if is_password:
                    entry_widget.config(show="*")  # 비밀번호 입력 시 * 표시
                entry_widget.has_placeholder = False  # 플레이스홀더 비활성화

        def on_focus_out(event):
            """입력 없이 포커스를 잃으면 다시 플레이스홀더 표시"""
            if not entry_widget.get().strip():  # 공백 입력 방지
                entry_widget.insert(0, placeholder_text)
                entry_widget.config(style="Placeholder.TEntry")  # 다시 회색 텍스트 스타일
                if is_password:
                    entry_widget.config(show="")  # 플레이스홀더 상태일 때는 평문 표시
                entry_widget.has_placeholder = True  # 플레이스홀더 다시 활성화

        entry_widget.bind("<FocusIn>", on_focus_in)
        entry_widget.bind("<FocusOut>", on_focus_out)

    # 로그인
    def login_action(id, password):
        #입력이 안된 상태 고려
        if (id.has_placeholder or id.get().strip() == ""):
            messagebox.showwarning("경고", "아이디가 입력되지 않았습니다.")
            return
        elif (password.has_placeholder or password.get().strip() == ""):
            messagebox.showwarning("경고", "비밀번호가 입력되지 않았습니다.")
            return

        #if문을 사용해서 데이터베이스에 있는 파일과 비교 후 아이디가 일치하면
        #main_menu 함수 호출
        print("test")
        
    #회원가입 화면으로 이동
    def signup_action():
        register(root)  #화면 이동

    def switch_to_login():
        for widget in root.winfo_children():  #기존 UI들 제거
                widget.destroy()  

        # 앱 타이틀
        title_label = ttk.Label(root, text="영단어 학습 프로그램", font=("Arial", 18, "bold"), bootstyle="primary")
        title_label.pack(pady=20)

        # ID 입력
        id_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        id_entry.pack(pady=5)
        set_placeholder(id_entry, "ID")  # 플레이스홀더 설정

        # 비밀번호 입력
        password_entry = ttk.Entry(root, width=30, bootstyle="info", style="Placeholder.TEntry")
        password_entry.pack(pady=5)
        set_placeholder(password_entry, "Password", is_password=True)  # 비밀번호 플레이스홀더 적용

        #엔터키로 입력
        id_entry.bind("<Return>", lambda event: login_action(id_entry, password_entry))
        password_entry.bind("<Return>", lambda event: login_action(id_entry, password_entry))

        # 버튼 컨테이너 프레임 (로그인 & 회원가입)
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=15)

        # 로그인 버튼
        login_button = ttk.Button(button_frame, text="로그인", bootstyle="success", command=lambda: login_action(id_entry, password_entry))
        login_button.pack(pady=5, fill=X)

        # 회원가입 버튼
        signup_button = ttk.Button(button_frame, text="회원가입", bootstyle="info", command=signup_action)
        signup_button.pack(pady=5, fill=X)

        # 종료 버튼 (하단 중앙 정렬)
        exit_button = ttk.Button(root, text="종료", bootstyle="danger", command=root.quit)
        exit_button.pack(side=BOTTOM, pady=15)

    switch_to_login()


