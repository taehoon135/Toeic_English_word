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
    test_user_id = user_db_for_quiz.register_user("quiz_user_specific_3", "pw", "Quiz User Specific 3")
    assert test_user_id is not None
    test_word_id1 = word_db_for_quiz.add_word("quiz_word_s3_1", "퀴즈단어_s3_1", "noun")
    assert test_word_id1 is not None
    test_word_id2 = word_db_for_quiz.add_word("quiz_word_s3_2", "퀴즈단어_s3_2", "verb")
    assert test_word_id2 is not None
    test_category_id = category_db_for_quiz.create_category(test_user_id, "Quiz Category Specific 3")
    assert test_category_id is not None
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id1)
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id2)
    return test_user_id, test_word_id1, test_word_id2, test_category_id

def test_add_quiz_question_short_answer(quiz_db_instance, setup_quiz_data):
    """Test Case: 퀴즈에 주관식 문제 추가"""
    # Arrange
    user_id, word_id, _, _ = setup_quiz_data
    quiz_id = quiz_db_instance.create_quiz("short_answer_ke", user_id)
    question_text = "사과"
    correct_answer = "apple"
    
    # Act
    question_id = quiz_db_instance.add_quiz_question(
        quiz_id, question_text, correct_answer, word_id=word_id
    )
    
    # Assert
    assert question_id is not None
    assert isinstance(question_id, int) and question_id > 0
    retrieved_q = quiz_db_instance.fetch_one("SELECT * FROM quiz_question WHERE question_id = ?", (question_id,))
    assert retrieved_q['quiz_id'] == quiz_id
    assert retrieved_q['question'] == question_text
    assert retrieved_q['correct_answer'] == correct_answer
    assert retrieved_q['word_id'] == word_id
    assert retrieved_q['options'] is None 