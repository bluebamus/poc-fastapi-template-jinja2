from fastapi import FastAPI
from sqladmin import Admin

from app.database.session import engine
from app.lyrics.api.routers.lyrics_admin import (
    LyricsAttributeAdmin,
    LyricsPromptTemplateAdmin,
    LyricsSongResultsAllAdmin,
    LyricsSongSampleAdmin,
    LyricsStoreDefaultInfoAdmin,
)
from config import prj_settings

# https://github.com/aminalaee/sqladmin


def init_admin(
    app: FastAPI,
    db_engine: engine,
    base_url: str = prj_settings.ADMIN_BASE_URL,
) -> Admin:
    admin = Admin(
        app,
        db_engine,
        base_url=base_url,
    )

    admin.add_view(LyricsStoreDefaultInfoAdmin)
    admin.add_view(LyricsAttributeAdmin)
    admin.add_view(LyricsSongSampleAdmin)
    admin.add_view(LyricsPromptTemplateAdmin)
    admin.add_view(LyricsSongResultsAllAdmin)

    return admin
