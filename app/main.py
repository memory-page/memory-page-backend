from fastapi import FastAPI
import uvicorn
from typing import Any, Dict

from app.domain.board.router import router as board_router
from app.domain.board.login.router import router as login_router

app = FastAPI()

app.include_router(router=board_router)
app.include_router(router=login_router)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
