import pytest
from database.quiz_db import QuizDB
from database.user_db import UserDB
from database.word_db import WordDB
from database.category_db import CategoryDB

# conftest.py 의 db_path fixture 를 사용합니다.

@pytest.fixture
def user_db_for_quiz(db_path):
    db = UserDB(db_path)
    # QuizDB 테스트 전에 User 테이블 등이 초기화되어야 함
    # UserDB.initialize_tables()는 UserDB 생성자에서 호출될 수 있음 (구현에 따라 다름)
    # 명시적으로 호출하거나, UserDB 생성 시 자동 초기화를 가정합니다.
    yield db
    db.close()

@pytest.fixture
def word_db_for_quiz(db_path):
    db = WordDB(db_path)
    yield db
    db.close()

@pytest.fixture
def category_db_for_quiz(db_path, user_db_for_quiz): # user_db_for_quiz를 사용하여 User 테이블 확보
    db = CategoryDB(db_path)
    yield db
    db.close()

@pytest.fixture
def quiz_db_instance(db_path, user_db_for_quiz, word_db_for_quiz, category_db_for_quiz):
    """QuizDB 인스턴스를 제공하고, 의존하는 DB들도 초기화합니다."""
    # 각 DB의 initialize_tables()는 해당 DB의 생성자에서 호출되거나 여기서 명시적으로 호출되어야 함.
    # 현재는 각 fixture에서 DB 인스턴스 생성 시 초기화된다고 가정합니다.
    db = QuizDB(db_path)
    yield db
    db.close()

@pytest.fixture
def setup_quiz_data(db_path, user_db_for_quiz, word_db_for_quiz, category_db_for_quiz):
    """퀴즈 테스트에 필요한 기본 사용자, 단어, 카테고리 데이터를 생성합니다."""
    test_user_id = user_db_for_quiz.register_user("quiz_user_specific_1", "pw", "Quiz User Specific 1")
    assert test_user_id is not None

    test_word_id1 = word_db_for_quiz.add_word("quiz_word_s1_1", "퀴즈단어_s1_1", "noun")
    assert test_word_id1 is not None
    test_word_id2 = word_db_for_quiz.add_word("quiz_word_s1_2", "퀴즈단어_s1_2", "verb")
    assert test_word_id2 is not None
    
    test_category_id = category_db_for_quiz.create_category(test_user_id, "Quiz Category Specific 1")
    assert test_category_id is not None
    
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id1)
    category_db_for_quiz.add_word_to_category(test_category_id, test_word_id2)
    
    return test_user_id, test_word_id1, test_word_id2, test_category_id

def test_create_new_quiz_without_category(quiz_db_instance, setup_quiz_data):
    """Test Case: 카테고리 없이 새 퀴즈 생성"""
    # Arrange
    user_id, _, _, _ = setup_quiz_data
    quiz_type = "short_answer_ek"
    
    # Act
    quiz_id = quiz_db_instance.create_quiz(quiz_type, user_id)
    
    # Assert
    assert quiz_id is not None
    assert isinstance(quiz_id, int) and quiz_id > 0
    retrieved_quiz = quiz_db_instance.fetch_one("SELECT * FROM quiz WHERE quiz_id = ?", (quiz_id,))
    assert retrieved_quiz is not None
    assert retrieved_quiz['quiz_type'] == quiz_type
    assert retrieved_quiz['user_id'] == user_id
    assert retrieved_quiz['category_id'] is None 