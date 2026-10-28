#DB연결 (src 경로는 main.py에서 추가됨)
from database.category_db import category_db
from database.quiz_db import quiz_db

#카테고리 이름으로 번호 찾기
def category_id_search(user_number, category_name): #유저 아이디와 검색하고 싶은 카테고리 이름
    for category_search in category_db.get_categories_by_user(user_number):
        if (category_search["name"] == category_name):
            return category_search["category_id"]

    return -1

#단어 이름으로 번호 찾기 (get_all_words / get_words_in_category 모두 word_id 키를 가짐)
def word_id_search(word_list, word_name):
    for word in word_list:
        if word["english"] == word_name:
            return word["word_id"]

    return -1

#퀴즈 시작: 퀴즈 세션을 만들고 문제로 쓸 단어를 뽑음 (틀린 횟수가 많을수록 자주 출제)
def start_quiz(user_number, category_name, quiz_type, count=None):
    category_id = None if category_name == "전체" else category_id_search(user_number, category_name)
    words = quiz_db.get_random_words_for_quiz(count, category_id, user_number)
    quiz_id = quiz_db.create_quiz(quiz_type, user_number, category_id)
    return quiz_id, words

#문제 1개 결과 기록 (오답 +1 / 정답 -1 → 다음 출제 확률에 반영)
def record_answer(user_number, quiz_id, word_id, is_correct):
    return quiz_db.record_quiz_result(user_number, quiz_id, word_id, is_correct)
