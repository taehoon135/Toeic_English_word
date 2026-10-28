import sqlite3
from database.base_db import BaseDatabase, SCHEMA_VERSION


def test_migrate_legacy_schema(db_path):
    """Test Case: 예전 스키마 DB를 열면 현재 스키마로 재구성되고, 데이터는 보존 / 고아 행은 삭제"""
    con = sqlite3.connect(db_path)
    con.executescript("""
        CREATE TABLE User (user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_login_id TEXT UNIQUE NOT NULL,
                           user_pw TEXT NOT NULL, user_name TEXT NOT NULL, user_phone TEXT,
                           is_admin BOOLEAN DEFAULT 0, user_api TEXT);
        CREATE TABLE Word (word_id INTEGER PRIMARY KEY AUTOINCREMENT, english TEXT UNIQUE NOT NULL,
                           meaning TEXT NOT NULL, part_of_speech TEXT, example_sentence TEXT, wrong_count INTEGER DEFAULT 0);
        CREATE TABLE Category (category_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                               user_id INTEGER NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE WordCategory (category_id INTEGER, word_id INTEGER, PRIMARY KEY (category_id, word_id));
        CREATE TABLE Rain_Game_Score (score_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, score INTEGER);
        INSERT INTO User VALUES (1, 'u1', 'pw', 'U1', NULL, 0, NULL);
        INSERT INTO Word VALUES (7, 'apple', '사과', 'noun', NULL, 5);
        INSERT INTO Category VALUES (1, 'fruit', 1, NULL), (2, 'orphan', 99, NULL), (3, '전체', 1, NULL);
        INSERT INTO WordCategory VALUES (1, 7), (2, 7), (1, 404);
        INSERT INTO Rain_Game_Score VALUES (1, 1, 3), (2, 99, 5), (3, 1, NULL);
    """)
    con.close()

    db = BaseDatabase(db_path)
    try:
        assert db.fetch_one("PRAGMA user_version")["user_version"] == SCHEMA_VERSION
        assert "wrong_count" not in [c["name"] for c in db.fetch_all("PRAGMA table_info(Word)")]
        assert db.fetch_one("SELECT english FROM Word WHERE word_id = 7")["english"] == "apple"
        # 고아(존재하지 않는 user/word) 및 제약 위반('전체' 카테고리, NULL 점수) 행 제거, 정상 행 보존
        assert [r["category_id"] for r in db.fetch_all("SELECT category_id FROM Category")] == [1]
        assert db.fetch_all("SELECT category_id, word_id FROM WordCategory") == [{"category_id": 1, "word_id": 7}]
        assert [r["score_id"] for r in db.fetch_all("SELECT score_id FROM Rain_Game_Score")] == [1]
        assert db.fetch_all("PRAGMA foreign_key_check") == []
        # 사용자 삭제 시 하위 데이터 연쇄 삭제 (UserWord 포함)
        db.execute("INSERT INTO UserWord (user_id, word_id, wrong_count) VALUES (1, 7, 2)")
        db.execute("DELETE FROM User WHERE user_id = 1")
        db.commit()
        for t in ("Category", "WordCategory", "Rain_Game_Score", "UserWord"):
            assert db.fetch_one(f"SELECT COUNT(*) n FROM {t}")["n"] == 0, t
    finally:
        db.close()
