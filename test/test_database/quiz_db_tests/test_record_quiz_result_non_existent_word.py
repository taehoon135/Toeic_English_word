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
    test_user_id = user_db_for_quiz.register_user("quiz_user_non_exist_word", "pw", "Quiz User NonExist Word")
    assert test_user_id is not None
    # 이 테스트는 존재하지 않는 단어를 사용하므로, 단어 생성 불필요
    return test_user_id, None, None, None 

def test_record_quiz_result_non_existent_word(quiz_db_instance, setup_quiz_data):
    """Test Case: 존재하지 않는 단어에 대한 퀴즈 결과 기록 시도 (실패)"""
    # Arrange
    user_id, _, _, _ = setup_quiz_data
    quiz_id = quiz_db_instance.create_quiz("type_non_exist", user_id) # 고유한 퀴즈 타입
    non_existent_word_id = 99999
    
    # Act
    success = quiz_db_instance.record_quiz_result(user_id, quiz_id, non_existent_word_id, is_correct=False)
    
    # Assert
    assert success is False, "존재하지 않는 단어에 대한 결과 기록은 실패해야 합니다."
    result_entry = quiz_db_instance.fetch_one(
        "SELECT * FROM quiz_result WHERE word_id = ?", (non_existent_word_id,)
    )
    assert result_entry is None 