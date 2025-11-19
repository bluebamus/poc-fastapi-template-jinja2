from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import AsyncQueuePool  # 비동기 풀 클래스

from config import db_settings


# Base 클래스 정의
class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    # MySQL async URL (asyncmy 드라이버)
    url=db_settings.MYSQL_URL,  # 예: "mysql+asyncmy://test:test@host:3306/poc"
    # === Connection Pool 설정 ===
    pool_size=10,  # 기본 풀 크기: 10개 연결 유지
    max_overflow=10,  # 최대 증가: 10개 (총 20개까지 가능)
    poolclass=AsyncQueuePool,  # 비동기 큐 풀 사용 (기본값, 명시적 지정)
    pool_timeout=30,  # 풀에서 연결 대기 시간: 30초 (기본 30초)
    pool_recycle=3600,  # 연결 재사용 주기: 1시간 (기본 3600초)
    pool_pre_ping=True,  # 연결 사용 전 유효성 검사: True로 설정
    pool_reset_on_return="rollback",  # 연결 반환 시 자동 롤백
    # === MySQL 특화 설정 ===
    echo=False,  # SQL 쿼리 로깅 (디버깅 시 True)
    # === 연결 타임아웃 및 재시도 ===
    connect_args={
        "connect_timeout": 10,  # MySQL 연결 타임아웃: 10초
        "read_timeout": 30,  # 읽기 타임아웃: 30초
        "write_timeout": 30,  # 쓰기 타임아웃: 30초
        "charset": "utf8mb4",  # 문자셋 (이모지 지원)
        "sql_mode": "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE",
        "init_command": "SET SESSION time_zone = '+00:00'",  # 초기 연결 시 실행
    },
)

# Async 세션 팩토리 생성
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 커밋 후 객체 상태 유지
    autoflush=True,  # 변경 감지 자동 플러시
)

# async_scoped_session 생성
AsyncScopedSession = async_session_factory(
    async_session_factory,
    scopefunc=current_task,
)


# 테이블 생성 함수
async def create_db_tables() -> None:
    async with engine.begin() as conn:
        # from app.database.models import Shipment, Seller  # noqa: F401
        await conn.run_sync(Base.metadata.create_all)
        print("MySQL tables created successfully")


# 세션 제너레이터 (FastAPI Depends에 사용)
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async 세션 컨텍스트 매니저
    - FastAPI dependency로 사용
    - Connection Pool에서 연결 획득/반환 자동 관리
    """
    async with async_session_factory() as session:
        # pre-commit 훅 (선택적: 트랜잭션 시작 전 실행)
        # await session.begin()  # async_sessionmaker에서 자동 begin

        try:
            yield session
            # FastAPI 요청 완료 시 자동 commit (예외 발생 시 rollback)
        except Exception as e:
            await session.rollback()  # 명시적 롤백 (선택적)
            print(f"Session rollback due to: {e}")  # 로깅
            raise
        finally:
            # 명시적 세션 종료 (Connection Pool에 반환)
            # context manager가 자동 처리하지만, 명시적으로 유지
            await session.close()
            print("session closed successfully")
            # 또는 session.aclose() - Python 3.10+


# 애플리케이션 종료 시 엔진 정리 (선택적)
async def dispose_engine() -> None:
    """애플리케이션 종료 시 모든 연결 해제"""
    await engine.dispose()
    print("Database engine disposed")
