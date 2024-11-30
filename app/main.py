from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Any, Dict

from app.domain.board.router import router as board_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=board_router)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
