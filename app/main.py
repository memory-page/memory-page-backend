from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Any, Dict

from app.domain.board.router import router as board_router
from app.domain.memo.router import router as memo_router
from app.domain.developer.router import router as developer_router
from app.base.settings import settings

mode = settings.MODE

app = FastAPI(
    openapi_url=None if mode == "MAIN" else "/openapi.json",
    docs_url=None if mode == "MAIN" else "/docs",
    redoc_url=None if mode == "MAIN" else "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=board_router)
app.include_router(router=memo_router)
app.include_router(router=developer_router)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
