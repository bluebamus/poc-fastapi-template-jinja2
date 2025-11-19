from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.common import lifespan
from app.home.api.routers.v1.router import router as home_router
from app.lyrics.api.routers.v1.router import router as lyrics_router

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

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
