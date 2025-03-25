import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def quiz_interpret(root1):
    from quiz_result import quiz_result

    #이런 배열을 데베에서 받았다고 가정
    word_list = [
        ["cold", "추운", 0, "카테고리1"],
        ["home", "집", 0, "전체"],
        ["school", "학교", 1, "전체"],
        ["mission", "임무", 0, "전체"],
        ["hot", "뜨거운", 2, "카테고리2"]
    ]
    word_list_anwser = [0 for i in range(len(word_list))]


    def enter(entered_text):
        nonlocal current_index

        if (entered_text == word_list[current_index][1]):
            word_list_anwser[current_index] = 1
        else:
            word_list_anwser[current_index] = 0
            #틀린 횟수 증가
            word_list[current_index][2] += 1 
            
        next_word()


    def next_word():
        nonlocal current_index
        current_index += 1
        
        #만약 모든 워드 리스트를 다 탐색했다면
        if (current_index >= len(word_list_anwser)):
            messagebox.showinfo("", "모든 단어를 완료했습니다!")
            quiz_result(root1, word_list, word_list_anwser)
        else:
            word_label.config(text= word_list[current_index][0], font=("Arial", 25))
            count_word.config(text=f"남은 단어 갯수: {len(word_list) - current_index}", font=("나눔 고딕", 16))
            answer.delete(0, tk.END)


    current_index = 0

    #프레임 초기화와 크기 조정
    root1.geometry("500x400")
    for widget in root1.winfo_children():
        widget.destroy()  

    tk.Label(root1, text="정답을 입력하세요", font=("나눔 고딕", 16)).pack(pady=20)
    word_label = tk.Label(root1, text= word_list[current_index][0], font=("Arial", 25))
    word_label.pack(pady=20)

    answer = tk.Entry(root1)
    answer.place(relx=0.5, rely=0.5, anchor="center", width=200, height=25)

    submit_button = tk.Button(root1, text="입력", command= enter)
    submit_button.place(relx=0.8, rely=0.5, anchor="e", width=40)

    #엔터키로도 입력 가능
    answer.bind("<Return>", lambda event: enter(answer.get()))

    count_word = tk.Label(root1, text=f"남은 단어 갯수: {len(word_list) - current_index}", font=("나눔 고딕", 16))
    count_word.pack(side="bottom", pady=10)
