import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

def quiz_four_choice(root1, user_number, category_id_str):
    from quiz_result import quiz_result

    import sys
    import os

    # Add the project root to the Python path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

    # Create db
    import pandas as pd
    from quiz_generation.four_choice_quiz import FourChoiceQuizModel
    from database.word_db import WordDB
    from database.category_db import CategoryDB

    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 상대 경로를 절대 경로로 변환
    db_path = os.path.join(current_dir, '../../toeic_vocabulary.db')

    if not os.path.exists(db_path):
        print("DB file not found")
        exit()

    word_db = WordDB(db_path=db_path)


    word_db.add_word('apple', '사과', 'noun', 'I like apples.')
    word_db.add_word('banana', '바나나', 'noun', 'I like bananas.')
    word_db.add_word('orange', '오렌지', 'noun', 'I like oranges.')
    word_db.add_word('pear', '배', 'noun', 'I like pears.')
    word_db.add_word('pineapple', '파인애플', 'noun', 'I like pineapples.')


    word_list = word_db.get_all_words()

    if not word_list:
        print("No words found")
        exit()

    print(word_list)

    #받은 카테고리는 str 형태이므로 카테고리 id를 찾음
    category_db = CategoryDB()

    #유저별 카테고리 목록을 불러옴
    category_list = category_db.get_user_categories(user_number)
    
    #선택된 카테고리가 전체인 경우 검색을 수행하지 않고 리스트의 모든 값을 사용해야 함
    if (category_id_str == "전체"):
        word_list_category = word_list
    else:
        for category in category_list:
            if category_id_str == category["name"]: #선택한 카테고리를 유저 카테고리 리스트에서 찾아내면 id를 얻을 수 있음
                category_id = category["category_id"]

        #카테고리에 맞게 word_list를 다시 받음
        word_list_category = word_db.get_words_by_category(category_id)

    #새로 생성한 리스트의 단어 개수만큼 정답지 생성
    word_list_answer = [0 for _ in range(len(word_list_category))]

    # Create model -> 문제 생성기
    model = FourChoiceQuizModel(word_list_category)

    #튜플을 리스트로 변환
    question = [list(item) for item in model]

    # for i in question:
    #     print(i)

    def enter():  #정답 여부 저장
        nonlocal current_index
        nonlocal correct_answer
        selected_word = var.get()
        
        if selected_word == correct_answer: #맞춘 경우 answer배열 값을 1로 바꿈
            word_list_answer[current_index] = 1
        else:
            word_list_answer[current_index] = 0 #틀린 경우 answer배열 값을 0으로 바꿈
            
            #오답인 단어의 id값을 찾아야 함
            for word in word_list_category:
                if correct_answer == word["english"]:
                    word_id = word["id"]

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

            # 체크박스 옵션 갱신
            # options = [answer_list[0]]  #보기에 들어갈 리스트
            # while len(options) < 4:  #보기 개수를 4개로 조절
            #     other = random.choice(answer_list)
            #     if other not in options:  #중복된 단어가 보기로 들어가지 않게 조절함
            #         options.append(other)
            
            #체크박스 옵션 갱신
            random.shuffle(options) # 보기 순서를 랜덤으로 섞음
            for i in range(4):
                checkboxes[i].config(text=options[i], variable=var, value=options[i])

    #윈도우 초기화 과정
    current_index = 0 #인덱스
    correct_answer = "" #정답 값 저장

    root1.geometry("500x400")
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
        cb = tk.Radiobutton(frame, text=f"", variable=var, value=f"", font=("나눔 고딕", 14), indicatoron=0, width=10, height=2, relief="raised")  #랜덤으로 뽑아야 하기에 처음에는 비워둠
        cb.grid(row=i // 2, column=i % 2, padx=10, pady=5)
        checkboxes.append(cb)  #나중에 조작할 수 있도록 저장하는 역할
    
    submit_button = tk.Button(root1, text="확인", command=enter, width=15, height=2)
    submit_button.pack(pady=20)
    root1.bind("<Return>", lambda event: enter())
    
    count_word = tk.Label(root1, text=f"남은 단어 갯수: {len(word_list_category) - current_index}", font=("나눔 고딕", 16))
    count_word.pack(side="bottom", pady=5)

    next_word()  #시작
