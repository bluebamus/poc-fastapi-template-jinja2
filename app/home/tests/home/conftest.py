from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.database.session import Base
from config import db_settings

# 테스트 전용 DB URL
TEST_DB_URL = db_settings.MYSQL_URL.replace(
    f"/{db_settings.MYSQL_DB}",
    "/test_db",  # 별도 테스트 DB 사용
)


@pytest_asyncio.fixture
async def test_engine():
    """각 테스트마다 생성되는 테스트 엔진"""
    engine = create_async_engine(
        TEST_DB_URL,
        poolclass=NullPool,  # 테스트에서는 풀 비활성화
        echo=True,  # SQL 쿼리 로깅
    )

    # 테스트 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 테스트 테이블 삭제
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """각 테스트마다 새로운 세션 (격리 보장)"""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()  # 테스트 후 롤백
