from fastapi import APIRouter, Depends, Request  # , Form, UploadFile, File, status
from sqlalchemy import Connection

from app.database.session import get_session

router = APIRouter(prefix="/lyrics", tags=["lyrics"])


@router.get("/")
async def home(
    request: Request,
    conn: Connection = Depends(get_session),
):
    print("session_user:")

    # return templates.TemplateResponse(
    #     request=request,
    #     name="index.html",
    #     context={"all_blogs": all_blogs, "session_user": session_user},
    # )
