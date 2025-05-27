import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_execute_insert_query_and_commit(db_path):
    """Test Case: INSERT 쿼리 실행 및 commit (BaseDB 자동 커밋 의존 또는 명시적 커밋)"""
    # Arrange
    db = BaseDatabase(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS TestTable (id INTEGER, name TEXT)")

    # Act
    # BaseDatabase의 execute가 INSERT 후 자동 commit을 한다고 가정
    # 또는 db.commit()을 명시적으로 호출해야 함
    insert_success = db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'NewName')")
    # 만약 execute가 bool을 반환하지 않는다면, 아래 assert는 수정 필요
    # self.assertTrue(insert_success, "INSERT 실행 실패") 
    # 여기서는 BaseDB의 execute가 자동 커밋을 수행한다고 가정하고 진행
    # 또는, 명시적으로 db.commit() 호출 후 확인
    if not hasattr(db, 'autocommit') or not db.autocommit: # 자동커밋 기능이 없다면 명시적 커밋
        db.commit()

    # Assert
    result = db.fetch_one("SELECT name FROM TestTable WHERE id = ?", (1,))
    assert result is not None, "커밋 후 데이터를 찾지 못했습니다."
    assert result['name'] == 'NewName', "커밋된 데이터가 일치하지 않습니다."
    
    db.close() 