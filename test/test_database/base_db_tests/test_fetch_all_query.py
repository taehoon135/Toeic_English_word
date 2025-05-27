import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_fetch_all_query(db_path):
    """Test Case: fetch_all 로 여러 행 조회"""
    # Arrange
    db = BaseDatabase(db_path)
    db.execute("CREATE TABLE IF NOT EXISTS TestTable (id INTEGER, name TEXT)")
    db.execute("INSERT INTO TestTable (id, name) VALUES (1, 'Name1')")
    db.execute("INSERT INTO TestTable (id, name) VALUES (2, 'Name2')")
    if not hasattr(db, 'autocommit') or not db.autocommit:
        db.commit()

    # Act
    all_results = db.fetch_all("SELECT * FROM TestTable ORDER BY id")

    # Assert
    assert len(all_results) == 2, "조회된 행의 수가 일치하지 않습니다."
    assert all_results[0]['name'] == 'Name1'
    assert all_results[1]['name'] == 'Name2'

    db.close() 