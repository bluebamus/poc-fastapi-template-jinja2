from fastapi import APIRouter, Depends, Request  # , Form, UploadFile, File, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from config import templates

router = APIRouter(tags=["home"])


@router.get("/db")
async def db_health_check(session: AsyncSession = Depends(get_session)):
    """DB 연결 상태 확인"""
    try:
        result = await session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "test_query": result.scalar(),
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@router.get("/")
async def home(
    request: Request,
    conn: AsyncSession = Depends(get_session),
):
    print("session_user:")
    return templates.TemplateResponse(request=request, name="home.html", context={})
