import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_execute_update_query_and_rollback(db_path):
    """Test Case: UPDATE 쿼리 실행 및 rollback"""
    # Arrange
    db = BaseDatabase(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS TestTable (id INTEGER, name TEXT)")
    db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'OldName')")
    if not hasattr(db, 'autocommit') or not db.autocommit:
        db.commit()
    
    # Act
    db.execute("UPDATE TestTable SET name = 'UpdatedName' WHERE id = 1")
    db.rollback() # 변경 사항 롤백
    
    # Assert
    result = db.fetch_one("SELECT name FROM TestTable WHERE id = ?", (1,))
    assert result is not None, "롤백 후 데이터를 찾지 못했습니다."
    assert result['name'] == 'OldName', "롤백 후 데이터가 이전 상태로 돌아가지 않았습니다."
    
    db.close() 