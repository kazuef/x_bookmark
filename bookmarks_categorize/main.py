from fastapi import FastAPI
from .routers.bookmark import router as bookmark_router
from .modules.database import init_db

app = FastAPI()

# DB初期化（アプリ起動時に一度だけ実行される）
init_db()

# CORS設定
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:8081"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bookmark_router, prefix="/bookmarks", tags=["bookmarks"])