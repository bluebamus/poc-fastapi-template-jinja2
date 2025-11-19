from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import db_settings


class Base(DeclarativeBase):
    pass


# 데이터베이스 엔진 생성
engine = create_async_engine(
    url=db_settings.MYSQL_URL,
    echo=False,
    pool_size=10,
    max_overflow=10,
    pool_timeout=5,
    pool_recycle=3600,
    # pool_pre_ping=True,
    # pool_reset_on_return="rollback",
    # connect_args={
    #     "connect_timeout": 3,
    #     "charset": "utf8mb4",
    # },
)

# Async sessionmaker 생성
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_tables():
    async with engine.begin() as connection:
        # from app.database.models import Seller, Shipment  # noqa: F401

        await connection.run_sync(Base.metadata.create_all)


# FastAPI 의존성용 세션 제너레이터
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # print("Session commited")
            # await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Session rollback due to: {e}")
            raise e
    # async with 종료 시 session.close()가 자동 호출됨


# 앱 종료 시 엔진 리소스 정리 함수
async def dispose_engine() -> None:
    await engine.dispose()
    print("Database engine disposed")
