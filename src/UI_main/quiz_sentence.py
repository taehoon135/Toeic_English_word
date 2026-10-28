import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_sentence(root1, user_number, category_id_str, count=None):
    from quiz_result import quiz_result
    from assist_module import start_quiz, record_answer
    from quiz_generation.cloze_quiz import ClozeQuizModel

    #카테고리(이름)에서 문제로 쓸 단어를 뽑고 퀴즈 세션 생성
    quiz_id, word_list_category = start_quiz(user_number, category_id_str, "cloze", count)
    if not word_list_category:
        messagebox.showwarning("경고", "퀴즈를 낼 단어가 없습니다.")
        return

    #API값을 가져오기 위한 작업
    from database.user_db import user_db
    api_key = user_db.get_api_key(user_number)

    # Create model -> 문제 생성기 (Gemini 호출: 키 오류/네트워크 오류 가능)
    try:
        model = ClozeQuizModel(word_list_category, api_key)
        question = [list(item) for item in model]
    except Exception as e:
        messagebox.showerror("오류", f"문제 생성에 실패했습니다. API 키를 확인해주세요.\n{e}")
        return
    if not question:
        messagebox.showerror("오류", "문제 생성 결과가 비어 있습니다. 다시 시도해주세요.")
        return

    #LLM이 일부 단어를 빠뜨리거나 순서를 바꿀 수 있으므로 정답(영단어)으로 문제-단어를 다시 맞춤
    by_english = {w["english"].lower(): w for w in word_list_category}
    question = [q for q in question if q[1].strip().lower() in by_english]
    word_list_category = [by_english[q[1].strip().lower()] for q in question]
    if not question:
        messagebox.showerror("오류", "문제 생성 결과가 올바르지 않습니다. 다시 시도해주세요.")
        return

    #문제 개수만큼 정답지 생성
    word_list_answer = [0 for _ in range(len(word_list_category))]

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
            #new_sentence = remove_word_case_insensitive(word_list[current_index][0], word_list[current_index][1]) #문장 교채

            #정답 저장
            correct_answer = question[current_index][1]

            word_label.config(text=question[current_index][0], font=("Arial", 15))
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

    #처음 화면에 띄우는 경우
    #new_sentence = remove_word_case_insensitive(word_list[current_index][0], word_list[current_index][1]) #문장 교채

    word_label = tk.Label(root1, text=question[current_index][0], font=("Arial", 15))
    word_label.pack(pady=20)

    #입력창
    answer = tk.Entry(root1)
    answer.place(relx=0.5, rely=0.5, anchor="center", width=200, height=25)

    #입력 버튼
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
