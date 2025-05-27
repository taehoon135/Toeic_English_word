import pytest
from database.base_db import BaseDatabase
import os

# conftest.py 의 db_path fixture 를 사용합니다.

def test_database_connection(db_path):
    """Test Case: 데이터베이스 연결 및 해제"""
    # Arrange & Act
    db = None
    try:
        db = BaseDatabase(db_path)
        # Assert
        assert db.conn is not None, "데이터베이스 연결에 실패했습니다."
        assert os.path.exists(db_path), "데이터베이스 파일이 생성되지 않았습니다."
    finally:
        if db:
            db.close() 