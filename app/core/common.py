# app/main.py
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 애플리케이션 생명주기 관리"""
    # Startup - 애플리케이션 시작 시
    print("Starting up...")

    try:
        # 데이터베이스 테이블 생성
        from app.database.session import create_db_tables

        await create_db_tables()
        print("Database tables ready")
    except asyncio.TimeoutError:
        print("Database initialization timed out")
        # 타임아웃 시 앱 시작 중단하려면 raise, 계속하려면 pass
        raise
    except Exception as e:
        print(f"Database initialization failed: {e}")
        # 에러 시 앱 시작 중단하려면 raise, 계속하려면 pass
        raise

    yield  # 애플리케이션 실행 중

    # Shutdown - 애플리케이션 종료 시
    print("Shutting down...")
    from app.database.session import engine

    await engine.dispose()
    print("Database engine disposed")


# FastAPI 앱 생성 (lifespan 적용)
app = FastAPI(title="POC FastAPI Template", lifespan=lifespan)
