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
    test_user_id = user_db_for_quiz.register_user("quiz_user_cascade", "pw", "Quiz User Cascade")
    assert test_user_id is not None
    test_word_id1 = word_db_for_quiz.add_word("quiz_word_cascade", "퀴즈단어_캐스케이드")
    assert test_word_id1 is not None
    return test_user_id, test_word_id1, None, None 

def test_delete_quiz_cascade(quiz_db_instance, setup_quiz_data):
    """Test Case: 퀴즈 삭제 시 관련 문제 및 결과 연쇄 삭제"""
    # Arrange
    user_id, word_id, _, _ = setup_quiz_data
    quiz_id = quiz_db_instance.create_quiz("cascade_test_del", user_id) # 고유한 퀴즈 타입
    quiz_db_instance.add_quiz_question(quiz_id, "Q1_del", "A1_del", word_id=word_id)
    quiz_db_instance.record_quiz_result(user_id, quiz_id, word_id, True)

    assert quiz_db_instance.fetch_one("SELECT * FROM quiz WHERE quiz_id = ?", (quiz_id,)) is not None
    assert quiz_db_instance.fetch_one("SELECT * FROM quiz_question WHERE quiz_id = ?", (quiz_id,)) is not None
    assert quiz_db_instance.fetch_one("SELECT * FROM quiz_result WHERE quiz_id = ?", (quiz_id,)) is not None

    # Act
    # QuizDB에 퀴즈 삭제 전용 메소드가 있다면 그것을 사용하는 것이 좋음.
    # 여기서는 execute를 직접 사용 (테이블 스키마에 ON DELETE CASCADE가 설정되어 있어야 함)
    # QuizDB의 initialize_tables를 보면 quiz_question과 quiz_result 모두 quiz(quiz_id)를
    # 참조하며 ON DELETE CASCADE가 설정되어 있음.
    delete_success = quiz_db_instance.execute("DELETE FROM quiz WHERE quiz_id = ?", (quiz_id,))
    # BaseDB의 execute는 INSERT/UPDATE/DELETE 시 자동 커밋하도록 수정되었으므로 별도 커밋 불필요
    assert delete_success is True # execute는 rowcount 또는 True/False를 반환할 수 있음. 여기선 True로 가정.

    # Assert
    assert quiz_db_instance.fetch_one("SELECT * FROM quiz WHERE quiz_id = ?", (quiz_id,)) is None
    assert quiz_db_instance.fetch_one("SELECT * FROM quiz_question WHERE quiz_id = ?", (quiz_id,)) is None, \
        "퀴즈 삭제 시 관련 문제들이 연쇄 삭제되어야 합니다."
    assert quiz_db_instance.fetch_one("SELECT * FROM quiz_result WHERE quiz_id = ?", (quiz_id,)) is None, \
        "퀴즈 삭제 시 관련 결과들이 연쇄 삭제되어야 합니다." 