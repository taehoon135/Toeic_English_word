from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def ranking(root, user_number):
    # 메인 메뉴 함수 import
    from quiz_menu import quiz_menu

    #DB 연결
    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.user_db import UserDB
    from database.game_db import GameDB

    user_db = UserDB()
    game_db = GameDB()

    # 기존 창의 모든 위젯 제거 (화면 초기화)
    for widget in root.winfo_children():
        widget.destroy()

    # 창 크기 설정
    root.geometry("500x600")
    root.title("랭킹")

    # '메인 메뉴' 버튼 클릭 시 실행되는 함수
    def go_to_quiz_menu():
        quiz_menu(root, user_number)

    #사용자 정보와 뒤로가기 프레임 생성
    user_frame = ttk.Frame(root, borderwidth=2, relief="solid", padding=1)
    user_frame.place(x=5, y=10, width=200, height=50)

    #유저 아이디 검색
    user_info = user_db.get_user_by_id(user_number)
    print(user_info)

    #유저 점수 검색
    highest_score = game_db.get_user_high_score(user_number)

    info_label = ttk.Label(user_frame, text= "사용자 ID: " + user_info["user_name"], font=("Arial", 11))
    info_label.pack(anchor="w")
    rank_label = ttk.Label(user_frame, text= "최고 점수: " + str(highest_score), font=("Arial", 11))
    rank_label.pack(anchor="w")

    # '메인 메뉴' 버튼 생성 및 배치
    exit_btn = ttk.Button(root, text="뒤로가기", bootstyle="success", command=go_to_quiz_menu)
    exit_btn.pack(anchor="e", padx=10, pady=10)

    # 결과를 표시할 프레임 생성 및 배치
    result_frame = ttk.Frame(root)
    result_frame.place(x=10, y=80, width=480, height=500)

    # Treeview에 표시할 컬럼 정의 ('mistakes'는 제거됨)
    columns = ("순위", "사용자ID", "최고점수")

    # Treeview 위젯 생성
    tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=20, style="Custom.Treeview")

    # 각 컬럼의 헤더와 너비 설정
    for col, width in zip(columns, [100, 100, 100]):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="center")

    # Treeview 배치
    tree.pack(side="left", fill="both", expand=True)

    # 스크롤바 생성 및 Treeview에 연결
    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    #순위권 유저 가져오기
    ranker_top100 = game_db.get_rain_game_ranking(100)

    #Treeview에 단어 데이터 삽입
    rank = 1
    for data in ranker_top100:
        tree.insert("", "end", values=(rank, data["user_name"], data["high_score"]))
        rank += 1
    
    #print(game_db.get_rain_game_ranking(10))