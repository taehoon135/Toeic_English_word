import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_interpret(root1, user_number, category_id_str, count=None):
    from quiz_result import quiz_result
    from assist_module import start_quiz, record_answer
    from quiz_generation.short_answer_quiz import ShortAnswerEKQuizModel

    #카테고리(이름)에서 문제로 쓸 단어를 뽑고 퀴즈 세션 생성
    quiz_id, word_list_category = start_quiz(user_number, category_id_str, "short_answer_ek", count)
    if not word_list_category:
        messagebox.showwarning("경고", "퀴즈를 낼 단어가 없습니다.")
        return

    #새로 생성한 리스트의 단어 개수만큼 정답지 생성
    word_list_answer = [0 for _ in range(len(word_list_category))]

    # Create model -> 문제 생성기
    model = ShortAnswerEKQuizModel(word_list_category)

    #튜플을 리스트로 변환
    question = [list(item) for item in model]

    # Print quiz
    # for i in question:
    #     print(i)

    def enter(entered_text):
        nonlocal current_index
        nonlocal correct_answer

        is_correct = entered_text.strip().lower() == correct_answer.strip().lower()
        word_list_answer[current_index] = 1 if is_correct else 0
        #결과 기록 (오답 횟수 +1 / 정답 -1)
        record_answer(user_number, quiz_id, word_list_category[current_index]["word_id"], is_correct)

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
