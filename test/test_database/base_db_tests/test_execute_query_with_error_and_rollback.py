import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_execute_query_with_error_and_rollback(db_path):
    """Test Case: 잘못된 SQL 실행 시 자동 롤백 (BaseDB의 execute가 예외처리 및 롤백을 한다고 가정)"""
    # Arrange
    db = BaseDatabase(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS TestTable (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'InitialName')")
    if not hasattr(db, 'autocommit') or not db.autocommit: # BaseDB의 execute가 자동커밋 하지 않는 경우
        db.commit()

    initial_data = db.fetch_one("SELECT name FROM TestTable WHERE id = 1")
    assert initial_data['name'] == 'InitialName', "초기 데이터 확인 실패"

    # Act
    try:
        # 일부러 오류 발생 (존재하지 않는 테이블에 INSERT 시도 등)
        # 또는 PRIMARY KEY 중복 에러 유도
        db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'DuplicateName')") 
    except Exception as e:
        print(f"예상된 오류 발생: {e}") # BaseDB의 execute가 예외를 발생시키거나, 내부에서 처리하고 False등을 반환할 수 있음

    # Assert
    # BaseDB의 execute 메서드가 오류 발생 시 트랜잭션을 롤백한다고 가정
    # 그렇지 않다면 이 테스트는 실패할 수 있음
    rolled_back_data = db.fetch_one("SELECT name FROM TestTable WHERE id = 1")
    assert rolled_back_data is not None, "오류 후 데이터 조회 실패"
    assert rolled_back_data['name'] == 'InitialName', "오류 발생 후 데이터가 롤백되지 않았습니다."
    
    db.close() 