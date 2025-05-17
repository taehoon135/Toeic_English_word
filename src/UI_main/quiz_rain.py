import tkinter as tk
import random
from PIL import Image, ImageTk

class AcidRainGame:
    def __init__(self, root, user_number, category_id_str):
        self.user_number = user_number
        self.category_id_str = category_id_str

        from assist_module import category_id_search

        import sys
        import os

        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
        from database.word_db import WordDB
        from database.category_db import CategoryDB
        #from database.game_db import GameScoreDB

        #self.game_db = GameScoreDB()

        # Create db
        import pandas as pd
        from quiz_generation.rain_quiz import RainQuizModel

        self.word_db = WordDB() #데베 클래스 생성

        word_list = self.word_db.get_all_words()

        if not word_list:
            print("No words found")
            exit()

        #받은 카테고리는 str 형태이므로 카테고리 id를 찾음
        self.category_db = CategoryDB()
        
        #선택된 카테고리가 전체인 경우 검색을 수행하지 않고 리스트의 모든 값을 사용해야 함
        if (category_id_str == "전체"):
            self.word_list_category = word_list
        else:
            category_id = category_id_search(user_number, category_id_str)

            #카테고리에 맞게 word_list를 다시 받음
            self.word_list_category = self.category_db.get_words_in_category(category_id)

            #print(word_list_category)

        # Create model -> 문제 생성기
        model = RainQuizModel(self.word_list_category)

        #튜플을 리스트로 변환
        self.question = [list(item) for item in model]

        for widget in root.winfo_children():  # 기존 UI 제거
            widget.destroy()

        self.root = root
        self.root.title("산성비 게임")
        self.canvas_width = 400
        self.canvas_height = 600

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # 이미지 로드
        self.heart_red = ImageTk.PhotoImage(Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\free-icon-red_heart.png").resize((30, 30)))
        self.heart_black = ImageTk.PhotoImage(Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\free-icon-black_heart.png").resize((30, 30)))
        self.wave_img = ImageTk.PhotoImage(Image.open("C:\\github\\sw-egineering\\src\\UI_main\\asset\\free-icon-wave.png").resize((100, 30)))

        # 목숨 표시
        self.max_lives = 3
        self.lives = self.max_lives
        self.hearts = []
        for i in range(self.max_lives):
            heart = self.canvas.create_image(30 + i*35, 30, image=self.heart_red)
            self.hearts.append(heart)

        # 점수
        self.score = 0
        self.score_text = self.canvas.create_text(350, 30, text="점수: 0", font=("Arial", 14), fill="blue")

        # 물결 아이콘 반복 배치
        self.wave_y = 500
        self.wave_items = []
        for x in range(0, self.canvas_width, 50):
            wave = self.canvas.create_image(x + 25, self.wave_y, image=self.wave_img)
            self.wave_items.append(wave)

        # 입력창 (물결 아래)
        self.entry = tk.Entry(root, font=("Arial", 14))
        self.canvas.create_window(self.canvas_width // 2, self.wave_y + 40, window=self.entry)
        self.entry.bind("<Return>", self.check_word)
        self.entry.focus()

        #단어의 힌트 부분 제거
        self.question = [item[:2] for item in self.question]

        #Print quiz
        # for i in self.question:
        #     print(i)

        self.active_words = []
        self.spawn_word()

        self.update()

    #메인 메뉴로 나감
    def go_to_menu(self):
        from menu import main_menu
        main_menu(self.root, self.user_number)
    
    #랭킹 저장을 위한 점수 리턴
    def final_score(self):
        #db에 점수 저장
        #self.game_db.save_score(self.user_number, 'word_rain', self.score)
        print(self.score)

    def spawn_word(self):
        if self.lives <= 0:
            return  # 이미 죽었으면 더 이상 단어 생성하지 않음

        eng, kor = random.choice(self.question)
        x = random.randint(50, 350)
        word_id = self.canvas.create_text(x, 0, text=kor, font=("Arial", 16), fill="black")
        self.active_words.append((word_id, x, 0, eng))  # 영어 단어가 정답으로 저장됨
        self.root.after(2000, self.spawn_word)

    def update(self):
        new_active_words = []
        for word_id, x, y, word in self.active_words:
            y += 5
            self.canvas.coords(word_id, x, y)
            if y >= self.wave_y - 15:
                self.lose_life()
                self.canvas.delete(word_id)
            else:
                new_active_words.append((word_id, x, y, word))

        self.active_words = new_active_words

        if self.lives > 0:
            self.root.after(50, self.update)
        else:
            self.game_over()

    def check_word(self, event):
        typed_eng = self.entry.get().strip()  # 사용자가 입력한 한글 단어 가져오기 (앞뒤 공백 제거)
        self.entry.delete(0, tk.END)  # 입력창 비우기

        # 현재 화면에 떠 있는 단어들과 비교
        for i, (word_id, x, y, correct_eng) in enumerate(self.active_words):
            # 사용자가 입력한 영어 단어와 화면에 있는 정답 영어 단어 비교 (대소문자 무시)
            if typed_eng.lower() == correct_eng.lower():
                self.canvas.delete(word_id)  # 화면에서 해당 단어 삭제
                self.score += 1  # 점수 1점 추가
                self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")  # 점수 텍스트 업데이트
                del self.active_words[i]  # 단어 리스트에서 제거
                break  # 하나 맞추면 루프 종료

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.canvas.itemconfig(self.hearts[self.lives], image=self.heart_black)

    def game_over(self):
        if hasattr(self, 'after_id'):
            self.root.after_cancel(self.after_id)

        # 떠 있는 단어 모두 삭제
        for word_id, _, _, _ in self.active_words:
            self.canvas.delete(word_id)
        self.active_words.clear()

        self.canvas.create_text(200, 250, text="Game Over", font=("Arial", 30), fill="red")
        self.canvas.create_text(200, 300, text=f"최종 점수: {self.score}", font=("Arial", 20), fill="black")
    
        self.final_score()

        btn = tk.Button(self.root, text="종료", font=("Arial", 14), command=self.go_to_menu)
        self.canvas.create_window(200, 350, window=btn)