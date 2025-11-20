from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.admin_manager import init_admin
from app.core.common import lifespan
from app.database.session import engine
from app.home.api.routers.v1.router import router as home_router
from app.lyrics.api.routers.v1.router import router as lyrics_router
from app.utils.cors import CustomCORSMiddleware
from config import prj_settings

app = FastAPI(
    title=prj_settings.PROJECT_NAME,
    version=prj_settings.VERSION,
    description=prj_settings.DESCRIPTION,
    lifespan=lifespan,
)

init_admin(app, engine)

custom_cors_middleware = CustomCORSMiddleware(app)
custom_cors_middleware.configure_cors()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    max_age=-1,
)

app.include_router(home_router)
app.include_router(lyrics_router)
