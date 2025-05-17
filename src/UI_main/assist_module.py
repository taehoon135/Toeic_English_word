#DB연결
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  #나보다 위 디렉토리에 있음
from database.word_db import WordDB
from database.category_db import CategoryDB

category_db = CategoryDB()
word_db = WordDB()

#카테고리 이름으로 번호 찾기
def category_id_search(user_number, category_name): #유저 아이디와 검색하고 싶은 카테고리 이름
    for category_search in category_db.get_categories_by_user(user_number):
        if (category_search["name"] == category_name):
            return category_search["category_id"]
    
    return -1
        
#단어 이름으로 번호 찾기
def word_id_search(word_list, word_name):
    for word in word_list:
        if word["english"] == word_name:
            return word["id"]
        
    return -1