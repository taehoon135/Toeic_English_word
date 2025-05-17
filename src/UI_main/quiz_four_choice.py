import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

def quiz_four_choice(root1, user_number, category_id_str):
    from quiz_result import quiz_result
    from assist_module import category_id_search, word_id_search, word_id_search_ver2

    # # Add the project root to the Python path
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.word_db import WordDB
    from database.category_db import CategoryDB

    # Create db
    import pandas as pd
    from quiz_generation.four_choice_quiz import FourChoiceQuizModel

    # # 현재 파일의 디렉토리 경로
    # current_dir = os.path.dirname(os.path.abspath(__file__))

    # # 상대 경로를 절대 경로로 변환
    # db_path = os.path.join(current_dir, '../../toeic_vocabulary.db')

    # if not os.path.exists(db_path):
    #     print("DB file not found")
    #     exit()

    # word_db = WordDB(db_path=db_path)

    word_db = WordDB() #데베 클래스 생성

    word_list = word_db.get_all_words()

    if not word_list:
        print("No words found")
        exit()

    #받은 카테고리는 str 형태이므로 카테고리 id를 찾음
    category_db = CategoryDB()
    
    #선택된 카테고리가 전체인 경우 검색을 수행하지 않고 리스트의 모든 값을 사용해야 함
    if (category_id_str == "전체"):
        word_list_category = word_list
    else:
        category_id = category_id_search(user_number, category_id_str)

        #카테고리에 맞게 word_list를 다시 받음
        word_list_category = category_db.get_words_in_category(category_id)

        print(word_list_category)

    #새로 생성한 리스트의 단어 개수만큼 정답지 생성
    word_list_answer = [0 for _ in range(len(word_list_category))]

    # Create model -> 문제 생성기
    model = FourChoiceQuizModel(word_list_category)

    #튜플을 리스트로 변환
    question = [list(item) for item in model]

    def enter():  #정답 여부 저장
        nonlocal current_index
        nonlocal correct_answer
        selected_word = var.get()
        
        if selected_word == correct_answer: #맞춘 경우 answer배열 값을 1로 바꿈
            word_list_answer[current_index] = 1
        else:
            word_list_answer[current_index] = 0 #틀린 경우 answer배열 값을 0으로 바꿈
            
            #오답인 단어의 id값을 찾아야 함 (word_id인 경우와 id인 경우를 모름)
            if (category_id_str == "전체"):
                word_id = word_id_search_ver2(word_list_category, correct_answer)
            else:
                word_id = word_id_search(word_list_category, correct_answer)

            #오답의 경우 단어의 오답 횟수를 증가시킴
            if (word_db.update_wrong_count(word_id) == False):
                print("문제 발생")
        
        current_index += 1 #인덱스 증가
        next_word() #문제 업데이트

    def next_word():
        nonlocal current_index
        nonlocal correct_answer

        if (current_index >= len(word_list_answer)):
            messagebox.showinfo("", "모든 단어를 완료했습니다!")
            quiz_result(root1, user_number, word_list_category, word_list_answer) #기본 정보인 루트, 유저 id와 퀴즈를 수행한 단어 리스트, 정답 여부를 보냄
        else:
            word_label.config(text=question[current_index][0], font=("Arial", 20))  #문제 갱신
            count_word.config(text=f"남은 단어 갯수: {len(word_list_category) - current_index}", font=("나눔 고딕", 16))  #남은 단어 갯수 갱신
            var.set(None)  #이전 선택 초기화

            #모델에서 준 문자열 리스트로 변환
            answer = question[current_index][1]
            options = answer.split(",") #보기에 들어갈 값들
            
            correct_answer = options[0] #anwser_list의 0번째 값이 정답
            
            #체크박스 옵션 갱신
            random.shuffle(options) # 보기 순서를 랜덤으로 섞음
            for i in range(4):
                checkboxes[i].config(text=options[i], variable=var, value=options[i])

    #윈도우 초기화 과정
    current_index = 0 #인덱스
    correct_answer = "" #정답 값 저장

    root1.geometry("500x400")
    root1.title("퀴즈")
    for widget in root1.winfo_children():
        widget.destroy()  
    
    tk.Label(root1, text="정답을 선택하세요", font=("나눔 고딕", 16)).pack(pady=20)
    word_label = tk.Label(root1, text=question[current_index][0], font=("Arial", 20))
    word_label.pack(pady=15)

    var = tk.StringVar()  #사용자가 선택했을때 저장될 공간
    var.set(None)  #체크박스 비우기
    checkboxes = []  #체크박스 옆에 보여줄 보기들

    frame = tk.Frame(root1)
    frame.pack(pady=10)

    for i in range(4):
        cb = tk.Radiobutton(frame, text=f"", variable=var, value=f"", font=("나눔 고딕", 14), indicatoron=0, width=15, height=2, relief="raised")  #랜덤으로 뽑아야 하기에 처음에는 비워둠
        cb.grid(row=i // 2, column=i % 2, padx=10, pady=5)
        checkboxes.append(cb)  #나중에 조작할 수 있도록 저장하는 역할
    
    submit_button = tk.Button(root1, text="확인", command=enter, width=15, height=2)
    submit_button.pack(pady=20)
    root1.bind("<Return>", lambda event: enter())
    
    count_word = tk.Label(root1, text=f"남은 단어 갯수: {len(word_list_category) - current_index}", font=("나눔 고딕", 16))
    count_word.pack(side="bottom", pady=5)

    next_word()  #시작
