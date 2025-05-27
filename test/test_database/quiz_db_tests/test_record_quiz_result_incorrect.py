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
    test_user_id = user_db_for_quiz.register_user("quiz_user_incorrect", "pw", "Quiz User Incorrect")
    assert test_user_id is not None
    test_word_id1 = word_db_for_quiz.add_word("quiz_word_incorrect", "퀴즈단어_오답")
    assert test_word_id1 is not None
    return test_user_id, test_word_id1, None, None 

def test_record_quiz_result_incorrect(quiz_db_instance, word_db_for_quiz, setup_quiz_data):
    """Test Case: 오답인 퀴즈 결과 기록 (wrong_count 1 증가)"""
    # Arrange
    user_id, word_id, _, _ = setup_quiz_data
    quiz_id = quiz_db_instance.create_quiz("type_incorrect", user_id) # 고유한 퀴즈 타입
    initial_word_state = word_db_for_quiz.fetch_one("SELECT wrong_count FROM Word WHERE word_id = ?", (word_id,))
    initial_wrong_count = initial_word_state['wrong_count']

    # Act
    success = quiz_db_instance.record_quiz_result(user_id, quiz_id, word_id, is_correct=False)
    
    # Assert
    assert success is True
    result_entry = quiz_db_instance.fetch_one(
        "SELECT * FROM quiz_result WHERE user_id = ? AND quiz_id = ? AND word_id = ?",
        (user_id, quiz_id, word_id)
    )
    assert result_entry is not None
    assert result_entry['is_correct'] == 0 # False는 0으로 저장
    
    final_word_state = word_db_for_quiz.fetch_one("SELECT wrong_count FROM Word WHERE word_id = ?", (word_id,))
    assert final_word_state['wrong_count'] == initial_wrong_count + 1 