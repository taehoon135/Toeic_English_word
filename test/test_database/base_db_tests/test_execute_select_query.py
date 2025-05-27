import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_execute_select_query(db_path):
    """Test Case: 간단한 SELECT 쿼리 실행"""
    # Arrange
    db = BaseDatabase(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS TestTable (id INTEGER, name TEXT)")
    db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'TestName')")
    db.commit() # BaseDB의 자동 커밋 로직을 테스트하는 것이 아니라면 명시적 커밋 필요
    
    # Act
    result = db.fetch_one("SELECT name FROM TestTable WHERE id = ?", (1,))
    
    # Assert
    assert result is not None, "데이터를 찾지 못했습니다."
    assert result['name'] == 'TestName', "조회된 데이터가 일치하지 않습니다."
    
    db.close() 