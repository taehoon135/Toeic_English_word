import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_interpret(root1, user_number, category_id_str):
    from quiz_result import quiz_result
    from assist_module import category_id_search, word_id_search, word_id_search_ver2

    # Add the project root to the Python path
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

    import sys
    import os

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
    from database.word_db import WordDB
    from database.category_db import CategoryDB

    # Create db
    import pandas as pd
    from quiz_generation.short_answer_quiz import ShortAnswerKEQuizModel

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

        #print(word_list_category)

    #새로 생성한 리스트의 단어 개수만큼 정답지 생성
    word_list_answer = [0 for _ in range(len(word_list_category))]

    # Create model -> 문제 생성기
    model = ShortAnswerKEQuizModel(word_list_category)

    #튜플을 리스트로 변환
    question = [list(item) for item in model]

    # Print quiz
    # for i in question:
    #     print(i)

    def enter(entered_text):
        nonlocal current_index
        nonlocal correct_answer

        if (entered_text == correct_answer):
            word_list_answer[current_index] = 1
        else:
            word_list_answer[current_index] = 0

            #오답의 경우 단어의 id 검색
            if (category_id_str == "전체"):
                word_id = word_id_search_ver2(word_list_category, correct_answer)
            else:
                word_id = word_id_search(word_list_category, correct_answer)
            
            #DB 틀린 횟수 증가
            if (word_db.update_wrong_count(word_id) == False):
                print("문제 발생")
        
        current_index += 1
        next_word()

    def next_word():
        nonlocal current_index
        nonlocal correct_answer
        
        #만약 모든 워드 리스트를 다 탐색했다면
        if (current_index >= len(word_list_answer)):
            messagebox.showinfo("", "모든 단어를 완료했습니다!")
            quiz_result(root1, user_number, word_list_category, word_list_answer)
        else:
            #정답 저장
            correct_answer = question[current_index][1]
            
            #문제 갱신
            question_split = question[current_index][0].split(":")
            new_question = question_split[0] + "\n\n" + question_split[1].strip()

            word_label.config(text= new_question, font=("Arial", 15))
            count_word.config(text=f"남은 단어 갯수: {len(word_list_category) - current_index}", font=("나눔 고딕", 16))
            answer.delete(0, tk.END)
            hint_label.grid_forget()  # 다음 단어로 넘어갈 때 힌트 숨기기

    def show_hint():
        nonlocal current_index
        hint_label.config(text=question[current_index][2])
        hint_label.grid(row=0, column=1)  # 버튼 오른쪽에 표시

    current_index = 0 #현재 문제 번호
    correct_answer = question[current_index][1] #정답 값 저장

    #프레임 초기화와 크기 조정
    root1.geometry("500x400")
    root1.title("퀴즈")
    for widget in root1.winfo_children():
        widget.destroy()  

    tk.Label(root1, text="정답을 입력하세요", font=("나눔 고딕", 16)).pack(pady=20)

    question_split = question[current_index][0].split(":")
    new_question = question_split[0] + ":\n\n" + question_split[1].strip()

    word_label = tk.Label(root1, text=new_question, font=("Arial", 15))
    word_label.pack(pady=20)

    answer = tk.Entry(root1)
    answer.place(relx=0.5, rely=0.5, anchor="center", width=200, height=25)

    submit_button = tk.Button(root1, text="입력", command=lambda: enter(answer.get()))
    submit_button.place(relx=0.8, rely=0.5, anchor="e", width=40)

    #엔터키로도 입력 가능
    answer.bind("<Return>", lambda event: enter(answer.get()))

    #힌트 버튼 프레임
    hint_frame = tk.Frame(root1)
    hint_frame.place(relx=0.15, rely=0.7)  # 입력 아래 왼쪽 (조절 가능)

    hint_button = tk.Button(hint_frame, text="힌트", command=show_hint, width=5, height=2)
    hint_button.grid(row=0, column=0, padx=(0, 10))  # 왼쪽
    hint_label = tk.Label(hint_frame, text=question[current_index][2], font=("나눔 고딕", 14), foreground="gray")

    count_word = tk.Label(root1, text=f"남은 단어 갯수: {len(word_list_category) - current_index}", font=("나눔 고딕", 16))
    count_word.pack(side="bottom", pady=10)
