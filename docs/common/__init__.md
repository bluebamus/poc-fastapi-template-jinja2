# Python `__init__.py` 완벽 가이드

## 목차
1. [기본 개념](#1-기본-개념)
2. [역사적 배경과 버전별 차이](#2-역사적-배경과-버전별-차이)
3. [__init__.py의 핵심 역할](#3-__init__py의-핵심-역할)
4. [실전 활용 패턴](#4-실전-활용-패턴)
5. [고급 활용 기법](#5-고급-활용-기법)
6. [일반적인 실수와 해결책](#6-일반적인-실수와-해결책)
7. [프로젝트별 권장사항](#7-프로젝트별-권장사항)

---

## 1. 기본 개념

### 1.1 모듈(Module)과 패키지(Package)의 정의

**모듈(Module):**
```python
# utils.py 파일 자체가 하나의 모듈
def hello():
    return "Hello"

# 다른 파일에서
import utils
utils.hello()
```

**패키지(Package):**
```
mypackage/              # 디렉토리 = 패키지
├── __init__.py        # 이 파일이 디렉토리를 패키지로 만듦
├── module1.py         # 패키지 내의 모듈
└── module2.py         # 패키지 내의 모듈
```

### 1.2 Python이 import를 해석하는 방식

```python
# from app.api.v1.router import get_user
# Python이 이 문장을 해석하는 순서:

1. sys.path에서 'app' 찾기
2. app/__init__.py 존재 확인 → app을 패키지로 인식
3. app/api/__init__.py 존재 확인 → app.api를 패키지로 인식
4. app/api/v1/__init__.py 존재 확인 → app.api.v1을 패키지로 인식
5. app/api/v1/router.py 찾기
6. router.py에서 get_user 찾기
```

**중요:** 중간 경로 중 하나라도 `__init__.py`가 없으면 (Python 3.3 이전에서는) import 실패

---

## 2. 역사적 배경과 버전별 차이

### 2.1 Python 2.x ~ 3.2 (Regular Packages)

```
mypackage/
├── __init__.py        # 필수! 없으면 패키지로 인식 안 됨
└── module.py
```

- `__init__.py`가 **반드시 필요**
- 없으면 `ImportError` 발생
- 빈 파일이어도 됨 (단순히 마커 역할)

### 2.2 Python 3.3+ (Namespace Packages 도입)

**PEP 420 - Implicit Namespace Packages**

```
# __init__.py 없이도 작동
mypackage/
└── module.py          # import mypackage.module 가능!
```

**Namespace Package의 특징:**
1. `__init__.py` 없어도 import 가능
2. 여러 경로에 분산된 같은 이름의 패키지 병합 가능
3. `__file__` 속성 없음

**하지만 여전히 Regular Package가 권장되는 이유:**

```python
# 1. 명시성: 의도가 명확함
# __init__.py가 있으면 "이건 패키지입니다"라고 선언하는 것

# 2. 초기화 코드 실행 가능
# app/__init__.py
print("패키지가 처음 import될 때 실행됨")

# 3. __all__ 정의 가능
__all__ = ['User', 'Post']

# 4. 편의 import 제공 가능
from .models.user import User
from .models.post import Post
```

### 2.3 Regular Package vs Namespace Package 비교

| 특징 | Regular Package | Namespace Package |
|------|----------------|-------------------|
| `__init__.py` | 필요 | 불필요 |
| 초기화 코드 | 실행 가능 | 실행 불가 |
| `__file__` 속성 | 있음 | 없음 |
| `__path__` | 리스트 | 읽기 전용 iterable |
| 분산 패키지 | 불가능 | 가능 |
| 사용 권장도 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 3. `__init__.py`의 핵심 역할

### 3.1 패키지 마커 (Package Marker)

**가장 기본적인 역할:**
```python
# 빈 __init__.py 파일
# 단순히 "이 디렉토리는 Python 패키지입니다"를 선언
```

```
myproject/
├── app/
│   ├── __init__.py           # app을 패키지로 표시
│   ├── models/
│   │   ├── __init__.py       # app.models를 패키지로 표시
│   │   └── user.py
│   └── api/
│       ├── __init__.py       # app.api를 패키지로 표시
│       └── router.py
```

### 3.2 패키지 초기화 (Package Initialization)

**패키지가 처음 import될 때 실행할 코드:**

```python
# app/__init__.py
print(f"app 패키지 초기화: {__name__}")

# 전역 설정
import logging
logging.basicConfig(level=logging.INFO)

# 데이터베이스 연결 풀 생성
from .database import create_pool
db_pool = create_pool()

# 환경 변수 검증
import os
if not os.getenv("SECRET_KEY"):
    raise ValueError("SECRET_KEY 환경 변수가 필요합니다")
```

**실행 순서:**
```python
# main.py
from app import models  # 1. app/__init__.py 실행
                        # 2. app/models/__init__.py 실행
```

**중요:** 각 패키지의 `__init__.py`는 **단 한 번만** 실행됨 (캐싱)

```python
from app import models  # app/__init__.py 실행
from app import api     # app/__init__.py 다시 실행 안 됨 (캐시)
```

### 3.3 네임스페이스 제어 (Namespace Control)

**3.3.1 `__all__` 변수로 공개 API 정의:**

```python
# app/models/__init__.py
from .user import User, UserRole
from .post import Post, Comment
from .internal import _InternalHelper

# 공개 API 명시
__all__ = ['User', 'UserRole', 'Post', 'Comment']
# _InternalHelper는 의도적으로 제외

# 다른 파일에서
from app.models import *  # User, UserRole, Post, Comment만 import됨
                          # _InternalHelper는 import 안 됨
```

**`__all__`의 효과:**
1. `from package import *` 시 import 대상 제한
2. 문서화 도구가 공개 API 파악
3. IDE 자동완성 힌트 제공

**주의:** `__all__` 없이 `from package import *` 하면?
```python
# __all__이 없으면
# _ 로 시작하지 않는 모든 이름이 import됨
```

**3.3.2 편의 Import 경로 제공:**

**Before (불편함):**
```python
# 깊은 import 경로
from app.models.user import User
from app.models.post import Post
from app.api.v1.auth.handlers import login, logout
from app.utils.validators.email import validate_email
```

**After (`__init__.py` 활용):**
```python
# app/models/__init__.py
from .user import User, UserRole
from .post import Post, Comment

# app/api/__init__.py
from .v1.auth.handlers import login, logout

# app/utils/__init__.py
from .validators.email import validate_email

# 이제 간단하게
from app.models import User, Post
from app.api import login, logout
from app.utils import validate_email
```

**3.3.3 하위 모듈 자동 로드:**

```python
# app/plugins/__init__.py
import os
import importlib

# plugins 디렉토리의 모든 .py 파일 자동 로드
plugin_dir = os.path.dirname(__file__)
for filename in os.listdir(plugin_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'.{module_name}', package=__name__)

print(f"로드된 플러그인: {len(os.listdir(plugin_dir)) - 1}개")
```

### 3.4 버전 정보 및 메타데이터 제공

```python
# mypackage/__init__.py
__version__ = '1.2.3'
__author__ = 'Your Name'
__email__ = 'your@email.com'
__license__ = 'MIT'
__description__ = 'My awesome package'

# 외부에서
import mypackage
print(mypackage.__version__)  # 1.2.3
```

### 3.5 하위 호환성 유지

```python
# app/utils/__init__.py

# 옛날 API (deprecated)
from .old_helper import old_function

# 새 API
from .new_helper import new_function

# 경고 추가
import warnings

def old_function(*args, **kwargs):
    warnings.warn(
        "old_function은 deprecated되었습니다. new_function을 사용하세요.",
        DeprecationWarning,
        stacklevel=2
    )
    return _old_function_impl(*args, **kwargs)

__all__ = ['new_function', 'old_function']  # 둘 다 노출
```

---

## 4. 실전 활용 패턴

### 4.1 최소 패턴 (빈 파일)

```python
# app/core/__init__.py
# (비어있음)
```

**언제 사용:**
- 단순히 패키지 마커만 필요할 때
- 하위 모듈을 개별적으로 import하는 것이 명확할 때

### 4.2 Simple Import 패턴

```python
# app/models/__init__.py
from .user import User
from .post import Post
from .comment import Comment

__all__ = ['User', 'Post', 'Comment']
```

**효과:**
```python
# Before
from app.models.user import User
from app.models.post import Post

# After
from app.models import User, Post
```

### 4.3 Lazy Import 패턴 (성능 최적화)

```python
# app/__init__.py

def __getattr__(name):
    """지연 로딩: 실제 사용될 때만 import"""

    if name == 'heavy_module':
        from . import heavy_module
        return heavy_module

    if name == 'User':
        from .models.user import User
        return User

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = ['heavy_module', 'User']
```

**장점:**
- 패키지 import 속도 향상
- 불필요한 모듈 로딩 방지
- 메모리 사용량 감소

### 4.4 Configuration 패턴

```python
# app/__init__.py
import os
from pathlib import Path

# 패키지 루트 경로
PACKAGE_ROOT = Path(__file__).parent

# 환경 변수 기반 설정
ENV = os.getenv('APP_ENV', 'development')
DEBUG = ENV == 'development'

# 환경별 설정 로드
if ENV == 'production':
    from .config.production import config
elif ENV == 'testing':
    from .config.testing import config
else:
    from .config.development import config

# 공개
__all__ = ['config', 'ENV', 'DEBUG', 'PACKAGE_ROOT']
```

### 4.5 Plugin System 패턴

```python
# app/plugins/__init__.py
from typing import Dict, Type

# 플러그인 레지스트리
_plugins: Dict[str, Type] = {}

def register(name: str):
    """데코레이터로 플러그인 등록"""
    def decorator(cls):
        _plugins[name] = cls
        return cls
    return decorator

def get_plugin(name: str):
    """플러그인 조회"""
    return _plugins.get(name)

def list_plugins():
    """등록된 모든 플러그인 목록"""
    return list(_plugins.keys())

__all__ = ['register', 'get_plugin', 'list_plugins']
```

```python
# app/plugins/email.py
from . import register

@register('email')
class EmailPlugin:
    pass
```

### 4.6 Facade 패턴 (통합 인터페이스)

```python
# app/database/__init__.py
"""데이터베이스 관련 모든 기능을 하나의 인터페이스로"""

from .connection import connect, disconnect
from .models import Base, Session
from .query import Query
from .transaction import transaction
from .migrations import migrate, rollback

# 사용자는 하나의 import로 모든 기능 사용
__all__ = [
    # 연결
    'connect', 'disconnect',
    # 모델
    'Base', 'Session',
    # 쿼리
    'Query',
    # 트랜잭션
    'transaction',
    # 마이그레이션
    'migrate', 'rollback'
]
```

```python
# 사용
from app.database import connect, Session, Query, transaction
```

---

## 5. 고급 활용 기법

### 5.1 동적 모듈 로딩

```python
# app/handlers/__init__.py
import importlib
import pkgutil

# 현재 패키지의 모든 서브모듈 자동 발견 및 로드
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    # 서브모듈 import
    module = importlib.import_module(f'.{module_name}', __name__)

    # 모듈의 모든 공개 속성을 현재 네임스페이스에 추가
    for attr_name in dir(module):
        if not attr_name.startswith('_'):
            globals()[attr_name] = getattr(module, attr_name)
            __all__.append(attr_name)
```

### 5.2 조건부 Import (선택적 의존성)

```python
# app/cache/__init__.py

# Redis가 설치되어 있으면 Redis 캐시 사용
try:
    import redis
    from .redis_cache import RedisCache as Cache
    CACHE_BACKEND = 'redis'
except ImportError:
    # 없으면 메모리 캐시로 폴백
    from .memory_cache import MemoryCache as Cache
    CACHE_BACKEND = 'memory'
    import warnings
    warnings.warn("Redis를 사용할 수 없어 메모리 캐시를 사용합니다.")

__all__ = ['Cache', 'CACHE_BACKEND']
```

### 5.3 Type Hints 재export

```python
# app/types/__init__.py
"""타입 힌트를 한 곳에 모아서 재export"""

from typing import TYPE_CHECKING

# 타입 체킹 시에만 import (런타임 오버헤드 없음)
if TYPE_CHECKING:
    from .models import User, Post
    from .protocols import Cacheable, Serializable

# 실제 런타임에서 사용할 타입들
from .custom_types import UserId, PostId, Timestamp
from .generics import Repository, Service

__all__ = [
    # Runtime types
    'UserId', 'PostId', 'Timestamp',
    'Repository', 'Service',

    # Type checking only (실제로는 import 안 됨)
    'User', 'Post',
    'Cacheable', 'Serializable',
]
```

### 5.4 Singleton 패턴

```python
# app/config/__init__.py

class Config:
    """싱글톤 설정 객체"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 최초 1회만 초기화
        self.database_url = os.getenv('DATABASE_URL')
        self.secret_key = os.getenv('SECRET_KEY')
        self._initialized = True

# 패키지 레벨에서 인스턴스 생성
config = Config()

__all__ = ['config', 'Config']
```

```python
# 어디서든 같은 인스턴스 사용
from app.config import config
print(config.database_url)
```

### 5.5 Context Manager 제공

```python
# app/database/__init__.py
from contextlib import contextmanager

@contextmanager
def get_session():
    """데이터베이스 세션 컨텍스트 매니저"""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

__all__ = ['get_session']
```

```python
# 사용
from app.database import get_session

with get_session() as session:
    session.add(user)
```

---

## 6. 일반적인 실수와 해결책

### 6.1 순환 Import (Circular Import)

**문제 상황:**
```python
# app/models/user.py
from app.models.post import Post

class User:
    def get_posts(self) -> list[Post]:
        pass

# app/models/post.py
from app.models.user import User

class Post:
    def get_author(self) -> User:
        pass
```

**에러:**
```
ImportError: cannot import name 'User' from partially initialized module
```

**해결책 1: TYPE_CHECKING 사용**
```python
# app/models/user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.post import Post

class User:
    def get_posts(self) -> list['Post']:  # 문자열 annotation
        pass
```

**해결책 2: 지연 Import**
```python
# app/models/user.py
class User:
    def get_posts(self):
        from app.models.post import Post  # 함수 내에서 import
        return Post.query.filter_by(user_id=self.id).all()
```

**해결책 3: `__init__.py`에서 순서 조정**
```python
# app/models/__init__.py
# 의존성 순서대로 import
from .base import Base      # 의존성 없음
from .user import User      # Base에만 의존
from .post import Post      # Base, User에 의존

__all__ = ['Base', 'User', 'Post']
```

### 6.2 `__init__.py`가 너무 무거움

**문제:**
```python
# app/__init__.py
import pandas as pd           # 5초
import tensorflow as tf       # 10초
from .heavy_module import *   # 3초

# 총 18초 소요!
```

**영향:**
```python
# 단순히 버전만 확인하려 해도 18초 대기
import app
print(app.__version__)  # 18초 후 출력
```

**해결책: Lazy Import**
```python
# app/__init__.py
__version__ = '1.0.0'

def __getattr__(name):
    if name == 'pandas':
        import pandas
        return pandas

    if name == 'tensorflow':
        import tensorflow
        return tensorflow

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
```

### 6.3 `__all__`과 실제 import의 불일치

**문제:**
```python
# app/utils/__init__.py
from .helpers import helper1, helper2

__all__ = ['helper1', 'helper2', 'helper3']  # helper3은 import 안 함!
```

**결과:**
```python
from app.utils import *
print(helper3)  # NameError!
```

**해결책:**
```python
# app/utils/__init__.py
from .helpers import helper1, helper2, helper3

__all__ = ['helper1', 'helper2', 'helper3']  # 일치
```

### 6.4 변경 가능한(mutable) 객체를 패키지 레벨에서 생성

**문제:**
```python
# app/__init__.py
users = []  # 전역 리스트

def add_user(user):
    users.append(user)
```

**위험:**
- 모든 import에서 같은 객체 공유
- 테스트 간 상태 오염
- 멀티스레딩 환경에서 race condition

**해결책:**
```python
# app/__init__.py
def create_user_manager():
    """팩토리 함수로 격리된 인스턴스 생성"""
    return UserManager()

class UserManager:
    def __init__(self):
        self._users = []

    def add_user(self, user):
        self._users.append(user)
```

### 6.5 상대 Import vs 절대 Import 혼용

**비권장:**
```python
# app/api/v1/router.py
from ...models import User      # 상대
from app.database import db     # 절대
```

**권장: 일관성 유지**
```python
# 옵션 1: 절대 import만 사용 (권장)
from app.models import User
from app.database import db

# 옵션 2: 상대 import만 사용
from ...models import User
from ...database import db
```

---

## 7. 프로젝트별 권장사항

### 7.1 FastAPI 프로젝트

```python
# app/__init__.py
from fastapi import FastAPI

def create_app() -> FastAPI:
    """애플리케이션 팩토리 패턴"""
    app = FastAPI(
        title="My API",
        version="1.0.0",
    )

    # 라우터 등록
    from .api.v1 import router as api_v1_router
    app.include_router(api_v1_router, prefix="/api/v1")

    return app

__all__ = ['create_app']
```

```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(posts_router, prefix="/posts", tags=["posts"])

__all__ = ['router']
```

```python
# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 모든 모델 import (Alembic이 인식하도록)
from .user import User
from .post import Post
from .comment import Comment

__all__ = ['Base', 'User', 'Post', 'Comment']
```

### 7.2 Django 스타일 프로젝트

```python
# myapp/__init__.py
default_app_config = 'myapp.apps.MyAppConfig'

__version__ = '0.1.0'
```

### 7.3 라이브러리/패키지 개발

```python
# mylib/__init__.py
"""
MyLib - A Python library for awesome things

Example:
    >>> from mylib import Thing
    >>> thing = Thing()
    >>> thing.do_something()
"""

__version__ = '1.2.3'
__author__ = 'Your Name'
__license__ = 'MIT'

# 공개 API
from .core import Thing, AnotherThing
from .utils import helper_function
from .exceptions import MyLibError, ConfigError

__all__ = [
    # Core
    'Thing',
    'AnotherThing',

    # Utils
    'helper_function',

    # Exceptions
    'MyLibError',
    'ConfigError',
]

# 버전 체크
import sys
if sys.version_info < (3, 8):
    raise RuntimeError("mylib requires Python 3.8+")
```

### 7.4 테스트 프로젝트

```python
# tests/__init__.py
"""
테스트 공통 유틸리티와 픽스처
"""
import os
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# 테스트 설정
TEST_DATABASE_URL = "sqlite:///:memory:"
TEST_SECRET_KEY = "test-secret-key"

# 공통 픽스처
from .fixtures import (
    sample_user,
    sample_post,
    db_session,
)

__all__ = [
    'TEST_DATABASE_URL',
    'TEST_SECRET_KEY',
    'sample_user',
    'sample_post',
    'db_session',
]
```

```python
# tests/unit/__init__.py
# 보통 비워둠
```

```python
# tests/integration/__init__.py
# 보통 비워둠
```

### 7.5 마이크로서비스 구조

```python
# services/user_service/__init__.py
"""User Service"""

from .app import create_app
from .models import User
from .schemas import UserSchema

__version__ = '1.0.0'
__service_name__ = 'user-service'

__all__ = ['create_app', 'User', 'UserSchema']
```

---

## 8. 체크리스트

### 8.1 `__init__.py`를 만들어야 하는 경우

- [x] 디렉토리를 Python 패키지로 만들고 싶을 때
- [x] 하위 모듈을 더 쉽게 import하고 싶을 때
- [x] 패키지 초기화 코드가 필요할 때
- [x] 공개 API를 명시하고 싶을 때
- [x] 패키지 메타데이터를 제공하고 싶을 때

### 8.2 `__init__.py`를 비워둬도 되는 경우

- [x] 단순히 패키지 마커만 필요할 때
- [x] 하위 모듈을 직접 import하는 것이 더 명확할 때
- [x] 초기화 코드가 없을 때

### 8.3 `__init__.py`가 필요 없는 경우

- [x] 단순 스크립트 디렉토리 (scripts/)
- [x] 문서 디렉토리 (docs/)
- [x] 설정 파일 디렉토리 (.github/, .vscode/)
- [x] 정적 파일 디렉토리 (static/, assets/)

---

## 9. 실전 예제: 완전한 FastAPI 프로젝트 구조

```
myproject/
├── app/
│   ├── __init__.py              # 애플리케이션 팩토리
│   ├── main.py                  # 진입점
│   │
│   ├── core/
│   │   ├── __init__.py          # 설정 export
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── __init__.py          # Base + 모든 모델 export
│   │   ├── base.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/
│   │   ├── __init__.py          # 모든 스키마 export
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── api/
│   │   ├── __init__.py          # 비어있음
│   │   └── v1/
│   │       ├── __init__.py      # 통합 라우터
│   │       ├── users.py
│   │       └── posts.py
│   │
│   ├── services/
│   │   ├── __init__.py          # 모든 서비스 export
│   │   ├── user_service.py
│   │   └── post_service.py
│   │
│   └── database/
│       ├── __init__.py          # 세션, 연결 함수
│       └── session.py
│
├── tests/
│   ├── __init__.py              # 테스트 유틸리티
│   ├── conftest.py              # pytest fixtures
│   ├── unit/
│   │   ├── __init__.py          # 비어있음
│   │   └── test_services.py
│   └── integration/
│       ├── __init__.py          # 비어있음
│       └── test_api.py
│
└── scripts/
    └── seed_data.py             # __init__.py 없음 (단독 스크립트)
```

**각 `__init__.py` 내용:**

```python
# app/__init__.py
from fastapi import FastAPI
from .core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
    )

    from .api.v1 import router
    app.include_router(router, prefix="/api/v1")

    return app

__all__ = ['create_app']
```

```python
# app/core/__init__.py
from .config import settings
from .security import create_access_token, verify_password

__all__ = ['settings', 'create_access_token', 'verify_password']
```

```python
# app/models/__init__.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .post import Post

__all__ = ['Base', 'User', 'Post']
```

```python
# app/schemas/__init__.py
from .user import UserCreate, UserRead, UserUpdate
from .post import PostCreate, PostRead, PostUpdate

__all__ = [
    'UserCreate', 'UserRead', 'UserUpdate',
    'PostCreate', 'PostRead', 'PostUpdate',
]
```

```python
# app/api/__init__.py
# 비어있음
```

```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(posts_router, prefix="/posts", tags=["posts"])

__all__ = ['router']
```

```python
# app/services/__init__.py
from .user_service import UserService
from .post_service import PostService

__all__ = ['UserService', 'PostService']
```

```python
# app/database/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ['engine', 'SessionLocal', 'get_db']
```

```python
# tests/__init__.py
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

TEST_DATABASE_URL = "sqlite:///:memory:"

__all__ = ['TEST_DATABASE_URL']
```

```python
# tests/unit/__init__.py
# 비어있음
```

```python
# tests/integration/__init__.py
# 비어있음
```

---

## 10. 핵심 정리

### `__init__.py`의 5가지 핵심 역할

1. **패키지 마커**: 디렉토리를 Python 패키지로 표시
2. **초기화**: 패키지 import 시 실행할 코드 정의
3. **네임스페이스 제어**: `__all__`로 공개 API 정의
4. **편의성**: 깊은 import 경로를 간단하게
5. **메타데이터**: 버전, 작성자 등 정보 제공

### 황금률

1. **명시성 > 암묵성**: 빈 파일이라도 만들어라
2. **일관성**: 프로젝트 전체에서 같은 패턴 사용
3. **단순성**: 너무 많은 로직을 넣지 마라
4. **지연 로딩**: 무거운 모듈은 필요할 때 import
5. **문서화**: 패키지의 목적과 사용법 명시

### 언제 사용하나?

| 디렉토리 유형 | `__init__.py` | 이유 |
|--------------|---------------|------|
| app/, src/ | ✅ 필수 | 애플리케이션 코드 |
| models/, api/, services/ | ✅ 필수 | 패키지 구조 |
| tests/ | ✅ 권장 | 공유 픽스처/유틸리티 |
| tests/unit/, tests/integration/ | ⚠️ 선택 | 상대 import 사용 시 |
| scripts/ | ❌ 불필요 | 단독 스크립트 |
| docs/, static/ | ❌ 불필요 | 비 Python 파일 |
