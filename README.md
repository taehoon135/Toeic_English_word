# 영단어 학습 프로그램 (sw-egineering)

TOEIC 영단어 학습용 데스크톱 앱. Python + tkinter/ttkbootstrap + SQLite, 퀴즈 문장 생성에 Gemini API 사용.

## 실행

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/UI_main/main.py     # UI_main 내부가 서로를 flat import 하므로 이 경로로 실행
.venv/bin/python -m pytest               # 테스트 (pytest.ini가 src 경로 처리)
```

## 구조

```
src/
  UI_main/           화면. 파일 1개 = 화면 1개, 함수 호출로 전환 (root의 자식 위젯을 destroy 후 재구성)
    main.py          엔트리포인트 → login.sign_login(root)
    login.py / create_account.py
    menu.py          메인 메뉴 (단어장 / 퀴즈 / 설정)
    vocab.py         단어장 조회·검색
    category_*.py    카테고리 생성(make) / 관리(manage) / 수정(adjust)
    quiz_menu.py     퀴즈 선택 → quiz_word / quiz_four_choice / quiz_sentence /
                     quiz_interpret / quiz_rain, 결과는 quiz_result.py
    ranking.py       빗방울 게임 랭킹
    settings.py      테마·API 키·계정 설정
    admin.py         관리자 화면 (단어 CRUD, CSV 임포트)
    assist_module.py 이름→id 조회 헬퍼
    asset/           아이콘·게임 예시 이미지
  database/          SQLite 접근 계층. BaseDatabase(ABC) 상속
    base_db.py       연결/execute/fetch_one/fetch_all/commit/rollback
    user_db.py       회원가입·로그인·비밀번호 변경·API 키
    word_db.py       단어 CRUD, toeic_words.csv 임포트, 오답 카운트
    category_db.py   카테고리 CRUD + 단어 매핑 (user_id로 권한 확인)
    quiz_db.py       퀴즈/문항 생성, 랜덤 단어 추출, 결과 기록
    game_db.py       빗방울 게임 점수·랭킹
  quiz_generation/   (Question, Answer, Hint) 생성기. BaseQuizModel(ABC) 상속, iterable
    short_answer_quiz.py  영→한 / 한→영 (jamo로 초성 힌트)
    four_choice_quiz.py   4지선다
    cloze_quiz.py         빈칸 채우기 (LLM으로 예문 생성, API 키 필요)
    rain_quiz.py          빗방울 게임용
  LLM/LLMResponse.py Gemini 호출 래퍼 (google-genai)
  API specification/ 각 모델의 인터페이스 예시 코드 (문서용, 실행 안 됨)
test/
  test_case_0~19.py        quiz_generation 단위 테스트
  test_database/**         DB 계층 단위 테스트 (conftest.py가 임시 DB 제공)
```

## DB

`src/database/toeic_vocabulary.db` 하나만 사용 (`base_db.DB_PATH`). 모든 연결에서 `PRAGMA foreign_keys = ON`.

- 스키마는 `base_db.SCHEMA` 한 곳에서 관리. 어떤 DB 클래스로 열어도 전 테이블이 생성됨
- 스키마를 바꿀 땐 `SCHEMA_VERSION`을 올릴 것 → 기존 DB는 열릴 때 재구성되고 고아·제약 위반 행은 삭제됨
- 모든 사용자 하위 데이터(카테고리, 오답 횟수, 퀴즈 기록, 점수)는 사용자 삭제 시 CASCADE
- 배포용 DB 상태: 관리자 계정(`123`/`123`) 1개 + 단어 957개, 테스트 계정/데이터 없음

| 테이블 | 용도 |
|---|---|
| User | 계정. `is_admin=1`이 관리자 (기본 계정 `123`/`123`, 관리자 정보 수정에서 변경) |
| Word | 단어 (`toeic_words.csv` 957개와 동일). DB가 비어 있으면 CSV로 채움 |
| UserWord | 사용자별 틀린 횟수 (`user_id, word_id, wrong_count`, 행이 없으면 0) |
| Category / WordCategory | 사용자별 카테고리, 단어 매핑. 이름 `전체`는 필터 예약어라 DB가 거부 |
| quiz / quiz_result | 퀴즈 1회 = quiz 1행, 문항별 정오답 = quiz_result. 오답 시 그 사용자의 wrong_count +1, 정답 시 -1 |
| quiz_question | 문항 저장용 (현재 UI는 미사용) |
| Rain_Game_Score | 산성비 게임 점수 / 랭킹 |

단어 조회 결과의 `wrong_count`는 항상 해당 사용자 기준 (`get_all_words(user_id)`, `get_words_in_category`는 카테고리 소유자).
퀴즈 단어는 `QuizDB.get_random_words_for_quiz`가 그 사용자의 `wrong_count + 1` 가중치로 뽑음 (회의록 2차 4.b).
UI는 `assist_module.start_quiz / record_answer`로만 퀴즈 DB에 접근.

## 실행 환경 주의

ttkbootstrap은 Tk 8.6이 필요. Homebrew Python이면 `brew install python-tk@3.14` 후 venv를 다시 만들 것
(`/usr/bin/python3`의 Tk 8.5로는 실행 불가).

`pytest`: test_case_16은 실제 Gemini API 키가 필요해 키 없이는 실패함.
