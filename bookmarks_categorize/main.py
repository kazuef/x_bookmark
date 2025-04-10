from fastapi import FastAPI
from routers.bookmark import router as bookmark_router

app = FastAPI()

app.include_router(bookmark_router, prefix="/bookmarks", tags=["bookmarks"])