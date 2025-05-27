import pytest
from database.quiz_db import QuizDB
from database.user_db import UserDB
from database.word_db import WordDB
from database.category_db import CategoryDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_for_quiz(db_path):
    db = UserDB(db_path)
    yield db
    db.close()

@pytest.fixture
def word_db_for_quiz(db_path):
    db = WordDB(db_path)
    yield db
    db.close()

@pytest.fixture
def category_db_for_quiz(db_path, user_db_for_quiz):
    db = CategoryDB(db_path)
    yield db
    db.close()

@pytest.fixture
def quiz_db_instance(db_path, user_db_for_quiz, word_db_for_quiz, category_db_for_quiz):
    db = QuizDB(db_path)
    yield db
    db.close()

@pytest.fixture
def setup_quiz_data_for_category_test(db_path, user_db_for_quiz, word_db_for_quiz, category_db_for_quiz):
    test_user_id = user_db_for_quiz.register_user("quiz_user_cat_test", "pw", "Quiz User Cat Test")
    assert test_user_id is not None

    # 카테고리 A용 단어들
    word_a1_id = word_db_for_quiz.add_word("cat_word_a1", "카테고리단어A1")
    word_a2_id = word_db_for_quiz.add_word("cat_word_a2", "카테고리단어A2")
    # 카테고리 B용 단어
    word_b1_id = word_db_for_quiz.add_word("cat_word_b1", "카테고리단어B1")

    category_a_id = category_db_for_quiz.create_category(test_user_id, "Category A for Quiz")
    assert category_a_id is not None
    category_db_for_quiz.add_word_to_category(category_a_id, word_a1_id)
    category_db_for_quiz.add_word_to_category(category_a_id, word_a2_id)

    category_b_id = category_db_for_quiz.create_category(test_user_id, "Category B for Quiz")
    assert category_b_id is not None
    category_db_for_quiz.add_word_to_category(category_b_id, word_b1_id)
    
    return test_user_id, {"A": [word_a1_id, word_a2_id], "B": [word_b1_id]}, {"A": category_a_id, "B": category_b_id}

def test_get_random_words_for_quiz_with_category(quiz_db_instance, setup_quiz_data_for_category_test):
    """Test Case: 특정 카테고리에서 랜덤 단어 조회"""
    # Arrange
    user_id, category_words, category_ids = setup_quiz_data_for_category_test
    target_category_id = category_ids["A"]
    words_in_target_category = category_words["A"]
    count = 1 
    
    # Act
    random_words = quiz_db_instance.get_random_words_for_quiz(count=count, category_id=target_category_id)
    
    # Assert
    assert len(random_words) == count
    assert random_words[0]['word_id'] in words_in_target_category
    assert 'category_name' in random_words[0]
    if random_words[0]['category_name']:
      # CategoryDB를 새로 만들어서 조회 (quiz_db_instance.db_path 사용)
      retrieved_cat = CategoryDB(quiz_db_instance.db_path).get_category(target_category_id)
      assert random_words[0]['category_name'] == retrieved_cat['name']

    # 카테고리 B에서 단어 조회 테스트 추가
    target_category_id_b = category_ids["B"]
    words_in_target_category_b = category_words["B"]
    random_words_b = quiz_db_instance.get_random_words_for_quiz(count=1, category_id=target_category_id_b)
    assert len(random_words_b) == 1
    assert random_words_b[0]['word_id'] in words_in_target_category_b

    # 카테고리 B에서 단어 조회 테스트 추가
    target_category_id_b = category_ids["B"]
    words_in_target_category_b = category_words["B"]
    random_words_b = quiz_db_instance.get_random_words_for_quiz(count=1, category_id=target_category_id_b)
    assert len(random_words_b) == 1
    assert random_words_b[0]['word_id'] in words_in_target_category_b

    # 카테고리 B에서 단어 조회 테스트 추가
    target_category_id_b = category_ids["B"]
    words_in_target_category_b = category_words["B"]
    random_words_b = quiz_db_instance.get_random_words_for_quiz(count=1, category_id=target_category_id_b)
    assert len(random_words_b) == 1
    assert random_words_b[0]['word_id'] in words_in_target_category_b

    # 카테고리 B에서 단어 조회 테스트 추가
    target_category_id_b = category_ids["B"]
    words_in_target_category_b = category_words["B"]
    random_words_b = quiz_db_instance.get_random_words_for_quiz(count=1, category_id=target_category_id_b)
    assert len(random_words_b) == 1
    assert random_words_b[0]['word_id'] in words_in_target_category_b 