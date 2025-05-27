import pytest
import os
import shutil

# 테스트용 데이터베이스 파일 경로
TEST_DB_DIR = os.path.join(os.path.dirname(__file__), "test_temp_db_files")
TEST_DB_PATH = os.path.join(TEST_DB_DIR, "test_main_app.db") # 모든 모듈이 공유할 DB 파일

@pytest.fixture(scope="session", autouse=True)
def setup_test_database_directory():
    """세션 시작 시 테스트 DB 디렉토리를 만들고, 세션 종료 시 삭제합니다."""
    if os.path.exists(TEST_DB_DIR):
        shutil.rmtree(TEST_DB_DIR)
    os.makedirs(TEST_DB_DIR, exist_ok=True)
    
    # src 경로를 sys.path에 추가 (모듈 임포트를 위해)
    # 이 부분은 pytest 실행 환경(예: 프로젝트 루트에서 실행)에 따라 필요 없을 수 있습니다.
    # pytest.ini 또는 pyproject.toml에서 python_paths 설정을 사용하는 것이 더 일반적입니다.
    import sys
    project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    yield # 테스트 세션 실행
    
    # 세션 종료 후 디렉토리 정리
    # shutil.rmtree(TEST_DB_DIR) # 필요하다면 세션 종료 후 삭제

@pytest.fixture
def db_path():
    """테스트용 데이터베이스 파일 경로를 제공하고, 각 테스트 전에 DB 파일을 초기화 (삭제)합니다."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    # 각 테스트는 깨끗한 DB 파일에서 시작
    return TEST_DB_PATH

# 다른 공통 fixture (예: 각 DB 모듈 인스턴스)도 여기에 추가할 수 있습니다.
# 예시:
# from database.base_db import BaseDatabase
# @pytest.fixture
# def base_db(db_path):
#     db = BaseDatabase(db_path)
#     yield db
#     db.close() 