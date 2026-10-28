import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

def quiz_four_choice(root1, user_number, category_id_str, count=None):
    from quiz_result import quiz_result
    from assist_module import start_quiz, record_answer
    from quiz_generation.four_choice_quiz import FourChoiceQuizModel

    #카테고리(이름)에서 문제로 쓸 단어를 뽑고 퀴즈 세션 생성
    quiz_id, word_list_category = start_quiz(user_number, category_id_str, "four_choice", count)
    if not word_list_category:
        messagebox.showwarning("경고", "퀴즈를 낼 단어가 없습니다.")
        return

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
        
        is_correct = selected_word == correct_answer
        word_list_answer[current_index] = 1 if is_correct else 0  #맞추면 1, 틀리면 0
        #결과 기록 (오답 횟수 +1 / 정답 -1)
        record_answer(user_number, quiz_id, word_list_category[current_index]["word_id"], is_correct)

        current_index += 1 #인덱스 증가
        next_word() #문제 업데이트

    def next_word():
        nonlocal current_index
        nonlocal correct_answer

        if (current_index >= len(word_list_answer)):
            root1.unbind("<Return>")  #다른 화면에서 엔터가 퀴즈를 호출하지 않도록 해제
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
