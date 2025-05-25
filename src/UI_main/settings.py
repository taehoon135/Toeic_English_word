import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from login import sign_login # ✅ 로그인 함수 import
from database.user_db import user_db  # ✅ 인스턴스 import로 변경

def toggle_dark_mode(root):
    style = ttk.Style()
    current_theme = style.theme_use()
    new_theme = "darkly" if current_theme == "flatly" else "flatly"
    style.theme_use(new_theme)

def settings_window(root, user_number):
    for widget in root.winfo_children():
        widget.destroy()
    root.title("설정")
    
    
    # ✅ 데이터베이스에서 실제 사용자 정보 가져오기
    user_info = user_db.get_user_by_id(user_number)
    if not user_info:
        print("사용자 정보를 찾을 수 없습니다.")
        return
    
    def go_to_menu():
        from menu import main_menu
        main_menu(root, user_number)

    label = ttk.Label(root, text="설정 화면", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)

    info_frame = ttk.Frame(root)
    info_frame.pack(pady=10)
    ttk.Label(info_frame, text=f"이름: {user_info['user_name']}", font=("Arial", 12)).pack()
    ttk.Label(info_frame, text=f"로그인 ID: {user_info['user_login_id']}", font=("Arial", 12)).pack()
    if user_info['user_phone']:
        ttk.Label(info_frame, text=f"전화번호: {user_info['user_phone']}", font=("Arial", 12)).pack()
    
    # ✅ API 키 표시 (마스킹 처리)
    api_key = user_info.get('user_api', '')
    if api_key:
        masked_api = api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else api_key[:4] + '*' * (len(api_key) - 4)
        ttk.Label(info_frame, text=f"API 키: {masked_api}", font=("Arial", 12)).pack()
    else:
        ttk.Label(info_frame, text="API 키: 미설정", font=("Arial", 12)).pack()

    edit_button = ttk.Button(root, text="개인정보 수정", bootstyle="info", command=lambda: verify_password(root, user_number))
    edit_button.pack(pady=10)

    dark_mode_button = ttk.Button(root, text="색반전 모드", bootstyle="secondary", command=lambda: toggle_dark_mode(root))
    dark_mode_button.pack(pady=10)

    logout_button = ttk.Button(root, text="로그아웃", bootstyle="warning", command=lambda: sign_login(root))
    logout_button.pack(pady=10)

    back_button = ttk.Button(root, text="뒤로가기", bootstyle="danger", command=go_to_menu)
    back_button.pack(pady=10)


def verify_password(root, user_number):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("비밀번호 확인")
    

    label = ttk.Label(root, text="현재 비밀번호를 입력하세요", font=("Arial", 14, "bold"))
    label.pack(pady=20)

    password_var = tk.StringVar()
    password_entry = ttk.Entry(root, textvariable=password_var, show="*")
    password_entry.pack(pady=10)

    error_label = ttk.Label(root, text="", font=("Arial", 10))
    error_label.pack()

    def check_password():
        # ✅ 데이터베이스에서 현재 비밀번호 확인
        user_info = user_db.get_user_by_id(user_number)
        if user_info and password_var.get() == user_info["user_pw"]:
            edit_info_window(root, user_number)
        else:
            error_label.config(text="비밀번호가 일치하지 않습니다.", bootstyle="danger")

    confirm_button = ttk.Button(root, text="확인", bootstyle="primary", command=check_password)
    confirm_button.pack(pady=10)

    cancel_button = ttk.Button(root, text="취소", bootstyle="secondary", command=lambda: settings_window(root, user_number))
    cancel_button.pack(pady=5)


def edit_info_window(root, user_number):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("개인정보 수정")
    

    # ✅ 데이터베이스에서 현재 사용자 정보 가져오기
    user_info = user_db.get_user_by_id(user_number)
    if not user_info:
        print("사용자 정보를 찾을 수 없습니다.")
        return

    label = ttk.Label(root, text="개인정보 수정", font=("Arial", 18, "bold"), bootstyle="primary")
    label.pack(pady=20)

    # ✅ 현재 DB 정보로 초기화
    name_var = tk.StringVar(value=user_info["user_name"])
    phone_var = tk.StringVar(value=user_info["user_phone"] if user_info["user_phone"] else "")
    password_var = tk.StringVar()
    api_var = tk.StringVar(value=user_info["user_api"] if user_info["user_api"] else "")

    # 이름 입력
    ttk.Label(root, text="이름", font=("Arial", 12)).pack(pady=(10, 5))
    ttk.Entry(root, textvariable=name_var, width=40).pack(pady=5)

    # 전화번호 입력
    ttk.Label(root, text="전화번호", font=("Arial", 12)).pack(pady=(10, 5))
    ttk.Entry(root, textvariable=phone_var, width=40).pack(pady=5)

    # 비밀번호 입력
    ttk.Label(root, text="새 비밀번호", font=("Arial", 12)).pack(pady=(10, 5))
    password_entry = ttk.Entry(root, textvariable=password_var, show="*", width=40)
    password_entry.pack(pady=5)

    # API 키 입력
    ttk.Label(root, text="API 키", font=("Arial", 12)).pack(pady=(10, 5))
    api_entry = ttk.Entry(root, textvariable=api_var, show="*", width=40)
    api_entry.pack(pady=5)

    # API 키 표시/숨기기 기능
    show_api = tk.BooleanVar()
    show_password = tk.BooleanVar()
    
    def toggle_password_visibility():
        if show_password.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")
    
    def toggle_api_visibility():
        if show_api.get():
            api_entry.config(show="")
        else:
            api_entry.config(show="*")
    
    # 체크박스들
    checkbox_frame = ttk.Frame(root)
    checkbox_frame.pack(pady=10)
    
    ttk.Checkbutton(checkbox_frame, text="비밀번호 표시", variable=show_password, command=toggle_password_visibility).pack(side=tk.LEFT, padx=10)
    ttk.Checkbutton(checkbox_frame, text="API 키 표시", variable=show_api, command=toggle_api_visibility).pack(side=tk.LEFT, padx=10)

    result_label = ttk.Label(root, text="", font=("Arial", 10))
    result_label.pack(pady=5)

    def save_changes():
        new_name = name_var.get().strip()
        new_phone = phone_var.get().strip() if phone_var.get().strip() else None
        new_pw = password_var.get().strip() if password_var.get().strip() else None
        new_api = api_var.get().strip() if api_var.get().strip() else None
        
        # ✅ 입력 검증
        if not new_name:
            result_label.config(text="이름을 입력해주세요.", bootstyle="danger")
            return
        
        # ✅ 모든 정보 업데이트
        try:
            # 기본 정보 (이름, 전화번호, 비밀번호) 업데이트
            basic_success = update_user_info(user_number, new_name, new_phone, new_pw)
            
            # API 키 업데이트
            api_success = user_db.update_api_key(user_number, new_api)
            
            if basic_success and api_success:
                result_label.config(text="모든 정보가 성공적으로 수정되었습니다.", bootstyle="success")
                # 2초 후 설정 화면으로 돌아가기
                root.after(2000, lambda: settings_window(root, user_number))
            elif basic_success and not api_success:
                result_label.config(text="기본 정보는 수정되었지만 API 키 수정에 실패했습니다.", bootstyle="warning")
            elif not basic_success and api_success:
                result_label.config(text="API 키는 수정되었지만 기본 정보 수정에 실패했습니다.", bootstyle="warning")
            else:
                result_label.config(text="정보 수정에 실패했습니다.", bootstyle="danger")
        except Exception as e:
            result_label.config(text=f"오류 발생: {str(e)}", bootstyle="danger")

    save_button = ttk.Button(root, text="저장", bootstyle="success", command=save_changes)
    save_button.pack(pady=10)

    cancel_button = ttk.Button(root, text="취소", bootstyle="danger", command=lambda: settings_window(root, user_number))
    cancel_button.pack(pady=5)


def update_user_info(user_id: int, user_name: str, user_phone: str = None, user_pw: str = None) -> bool:
    """
    사용자 정보를 업데이트하는 함수 (전화번호 포함)
    """
    try:
        if user_pw:
            # 비밀번호도 함께 변경
            user_db.execute(
                "UPDATE User SET user_name = ?, user_phone = ?, user_pw = ? WHERE user_id = ?",
                (user_name, user_phone, user_pw, user_id)
            )
        else:
            # 이름과 전화번호만 변경
            user_db.execute(
                "UPDATE User SET user_name = ?, user_phone = ? WHERE user_id = ?",
                (user_name, user_phone, user_id)
            )
        user_db.commit()
        return True
    except Exception as e:
        print(f"사용자 정보 수정 오류: {e}")
        user_db.rollback()
        return False


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    root.geometry("400x500")  # ✅ 초기 창 크기 설정 (원래 크기로)
    root.resizable(True, True)  # ✅ 크기 조정 비활성화
    settings_window(root, user_number=1)
    root.mainloop()
