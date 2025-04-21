from fastapi import FastAPI
from .routers.bookmark import router as bookmark_router
from .modules.database import init_db

app = FastAPI()

# DB初期化（アプリ起動時に一度だけ実行される）
init_db()

app.include_router(bookmark_router, prefix="/bookmarks", tags=["bookmarks"])