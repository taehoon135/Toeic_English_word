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
def setup_quiz_data(db_path, user_db_for_quiz, word_db_for_quiz, category_db_for_quiz):
    test_user_id = user_db_for_quiz.register_user("quiz_user_specific_2", "pw", "Quiz User Specific 2")
    assert test_user_id is not None
    test_word_id1 = word_db_for_quiz.add_word("quiz_word_s2_1", "퀴즈단어_s2_1", "noun")
    assert test_word_id1 is not None
    test_word_id2 = word_db_for_quiz.add_word("quiz_word_s2_2", "퀴즈단어_s2_2", "verb")
    assert test_word_id2 is not None
    test_category_id = category_db_for_quiz.create_category(test_user_id, "Quiz Category Specific 2")
    assert test_category_id is not None
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id1)
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id2)
    return test_user_id, test_word_id1, test_word_id2, test_category_id

def test_create_new_quiz_with_category(quiz_db_instance, setup_quiz_data):
    """Test Case: 특정 카테고리로 새 퀴즈 생성"""
    # Arrange
    user_id, _, _, category_id = setup_quiz_data
    quiz_type = "four_choice"
    
    # Act
    quiz_id = quiz_db_instance.create_quiz(quiz_type, user_id, category_id)
    
    # Assert
    assert quiz_id is not None
    retrieved_quiz = quiz_db_instance.fetch_one("SELECT * FROM quiz WHERE quiz_id = ?", (quiz_id,))
    assert retrieved_quiz is not None
    assert retrieved_quiz['category_id'] == category_id 