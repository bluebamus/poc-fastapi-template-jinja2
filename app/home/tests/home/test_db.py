import pytest
from sqlalchemy import text


@pytest.mark.asyncio
async def test_database_connection(test_engine):
    """테스트 엔진을 사용한 연결 테스트"""
    async with test_engine.begin() as connection:
        result = await connection.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_session_usage(db_session):
    """세션을 사용한 테스트"""
    result = await db_session.execute(text("SELECT 1 as num"))
    assert result.scalar() == 1
