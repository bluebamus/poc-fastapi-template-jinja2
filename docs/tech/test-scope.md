# Pytest Fixture Scope 가이드

## 1. Fixture Scope 개요

### Scope란?

Pytest의 scope는 fixture가 생성되고 유지되는 범위를 결정합니다.

```python
@pytest.fixture(scope="function")  # 기본값
def my_fixture():
    return "value"
```

### 사용 가능한 Scope

| Scope | 생성 시점 | 소멸 시점 | 사용 사례 |
|-------|----------|----------|-----------|
| function | 각 테스트 함수 실행 전 | 각 테스트 함수 종료 후 | DB 세션, Mock 객체 |
| class | 각 테스트 클래스 실행 전 | 각 테스트 클래스 종료 후 | 클래스별 공통 데이터 |
| module | 각 테스트 파일 로드 시 | 각 테스트 파일 종료 후 | DB 엔진, 설정 객체 |
| package | 각 패키지 로드 시 | 각 패키지 종료 후 | 패키지 공통 리소스 |
| session | 전체 테스트 세션 시작 시 | 전체 테스트 세션 종료 시 | 전역 설정, 캐시 |

### Scope 계층 구조

```text
session (가장 넓음)
  └─ package
      └─ module
          └─ class
              └─ function (가장 좁음, 기본값)
```

**규칙:** 하위 스코프 fixture는 상위 스코프 fixture에 의존 가능, 역은 불가

---

## 2. pytest-asyncio와 Scope 제약

### 핵심 문제

pytest-asyncio는 비동기 fixture 실행을 위해 event loop가 필요합니다.

**중요한 규칙:**

> **비동기 fixture의 scope는 event loop scope보다 넓을 수 없습니다.**

### Event Loop Scope 설정

pyproject.toml에서 설정:

```toml
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "function"  # 기본값
```

| 값 | Event Loop 생명주기 |
|---|-------------------|
| "function" | 테스트 시작/종료마다 생성/삭제 |
| "module" | 모듈 로드/종료 시 생성/삭제 |
| "session" | 세션 시작/종료 시 생성/삭제 |

### Scope 제약 규칙

```python
# asyncio_default_fixture_loop_scope = "function" 설정 시:

# ✓ 가능
@pytest_asyncio.fixture(scope="function")
async def my_fixture():
    ...

# ✗ 불가능
@pytest_asyncio.fixture(scope="module")  # ❌ module > function
async def my_fixture():
    ...

@pytest_asyncio.fixture(scope="session")  # ❌ session > function
async def my_fixture():
    ...
```

---

## 3. ScopeMismatch 에러 해결

### 에러 메시지

```text
ScopeMismatch: You tried to access the function scoped fixture
_function_scoped_runner with a session scoped request object.
```

**의미:** session 스코프 fixture가 function 스코프 event loop를 사용하려 시도

### 발생 원인

```python
# ❌ 에러 발생
# pyproject.toml: asyncio_default_fixture_loop_scope = "function"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(...)
    # async/await 사용 → event loop 필요
    # 하지만 loop는 function scope!
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
```

**문제의 핵심:**

```text
전체 테스트 세션
├─ test_engine (session scope) ─────────────────────────────
│                                                           │
├─ test_1                                                   │
│  └─ event_loop_1 (function scope) ───┐                   │
│     └─ await in test_engine ✓        │                   │
│                                       ↓ 삭제              │
│                                                           │
├─ test_2                                                   │
│  └─ event_loop_2 (function scope) ───┐                   │
│     └─ await in test_engine ❌ (loop_1은 이미 없음!)      │
└───────────────────────────────────────────────────────────┘
```

### 해결 방법

#### 방법 1: Fixture Scope 변경 (권장)

```python
# ✓ 해결: module 스코프로 변경
@pytest_asyncio.fixture(scope="module")
async def test_engine():
    """모듈당 한 번만 생성되는 테스트 엔진"""
    engine = create_async_engine(...)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
```

**장점:**
- 스코프 일치로 에러 해결
- 모듈(파일)당 하나의 엔진으로 성능 최적화
- 테스트 격리 유지

#### 방법 2: Event Loop Scope 변경

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_default_fixture_loop_scope = "session"  # function → session
```

**장점:** session 스코프 비동기 fixture 사용 가능

**단점:**
- 모든 테스트가 같은 event loop 공유
- 테스트 간 격리 감소

#### 방법 3: Function Scope 사용

```python
@pytest_asyncio.fixture  # scope="function" (기본값)
async def db_engine():
    """각 테스트마다 새로운 엔진"""
    ...
```

**장점:** 완벽한 테스트 격리

**단점:** 성능 저하 (매 테스트마다 엔진 생성/삭제)

---

## 4. Scope 선택 가이드

### DB 관련 Fixture 권장 패턴

```python
# ✓ 권장 패턴
@pytest_asyncio.fixture(scope="module")
async def db_engine():
    """모듈당 1개 엔진 (비용이 큼)"""
    engine = create_async_engine(...)

    # 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 테이블 삭제
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    """각 테스트마다 새로운 세션 (격리 보장)"""
    async_session = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()  # 테스트 후 롤백
```

**이유:**
- **엔진 (module)**: 생성 비용이 크므로 모듈당 1번
- **세션 (function)**: 테스트 격리를 위해 매번 새로 생성

### Scope별 사용 사례

| 리소스 | 권장 Scope | 이유 |
|--------|-----------|------|
| DB 엔진 | module | 생성 비용 큼, 모듈 내 재사용 |
| DB 세션 | function | 테스트 격리 필수 |
| FastAPI Client | function | 의존성 오버라이드 격리 |
| Mock 객체 | function | 테스트마다 독립적 |
| 전역 설정 | session | 변하지 않음 |

---

## 5. 실전 예제

### FastAPI + SQLAlchemy 비동기 테스트

```python
# conftest.py
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.database.session import Base
from config import db_settings

# 테스트 DB URL
TEST_DB_URL = db_settings.MYSQL_URL.replace(
    f"/{db_settings.MYSQL_DB}",
    "/test_db",
)


# Module Scope: DB 엔진 (모듈당 1개)
@pytest_asyncio.fixture(scope="module")
async def test_engine():
    """모듈당 한 번만 생성되는 테스트 엔진"""
    engine = create_async_engine(
        TEST_DB_URL,
        poolclass=NullPool,
        echo=True,
    )

    # 테스트 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 테스트 테이블 삭제
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


# Function Scope: DB 세션 (각 테스트마다)
@pytest_asyncio.fixture
async def db_session(test_engine):
    """각 테스트마다 새로운 세션 (격리 보장)"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()


# Function Scope: FastAPI 테스트 클라이언트
@pytest_asyncio.fixture
async def client(db_session):
    """각 테스트마다 새로운 클라이언트"""
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    from app.database.session import get_session

    # DB 세션 의존성 오버라이드
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

### 테스트 작성

```python
# test_users.py
import pytest


@pytest.mark.asyncio
async def test_database_connection(test_engine):
    """test_engine은 module scope - 모듈에서 재사용됨"""
    from sqlalchemy import text

    async with test_engine.begin() as connection:
        result = await connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_user(db_session):
    """db_session은 function scope - 매번 새로 생성"""
    from app.users.models import User

    user = User(email="test@example.com", username="testuser")
    db_session.add(user)
    await db_session.commit()

    assert user.id is not None
```

---

## 6. 트러블슈팅

### 자주 발생하는 에러

#### 에러 1: ScopeMismatch (비동기 fixture)

**증상:**

```text
ScopeMismatch: You tried to access the function scoped fixture
_function_scoped_runner with a session/module scoped request object.
```

**해결:**
1. Fixture scope를 낮춤 (session → module → function)
2. 또는 asyncio_default_fixture_loop_scope 변경

#### 에러 2: ScopeMismatch (의존성 스코프)

**증상:**

```text
ScopeMismatch: You tried to access the function scoped fixture X
with a session scoped request object.
```

**원인:** 상위 scope fixture가 하위 scope fixture 의존

**해결:** 의존 방향 변경 (하위 → 상위만 가능)

### 디버깅 팁

```bash
# fixture 의존성 확인
pytest --fixtures -v

# 특정 테스트의 fixture 추적
pytest tests/test_example.py::test_function --setup-show
```

---

## 7. Best Practices

### Scope 선택 원칙

1. **기본은 function scope**: 의심스러우면 function
2. **생성 비용이 크면 module**: DB 엔진, HTTP 클라이언트
3. **격리가 중요하면 function**: DB 세션, Mock 객체
4. **전역 설정만 session**: 변하지 않는 설정값

### 비동기 Fixture 체크리스트

- [ ] Event loop scope 설정 확인 (pyproject.toml)
- [ ] Fixture scope <= Event loop scope 확인
- [ ] 의존성 방향 확인 (하위 → 상위만)
- [ ] 테스트 격리 검증 (서로 영향 없는지)

---

## 요약

### 핵심 규칙

1. **비동기 fixture scope <= event loop scope**
2. **하위 scope → 상위 scope 의존만 가능**
3. **의심스러우면 function scope**
4. **격리 > 성능** (테스트 신뢰성 우선)

### Scope 선택 치트시트

| 상황 | 권장 Scope | 이유 |
|------|-----------|------|
| DB 엔진 | module | 생성 비용 큼 |
| DB 세션 | function | 테스트 격리 필수 |
| FastAPI Client | function | 의존성 오버라이드 격리 |
| Mock 객체 | function | 테스트마다 독립적 |
| 전역 설정 | session | 변하지 않음 |

---

**이제 Pytest fixture scope를 올바르게 사용할 수 있습니다!**
