from fastapi import FastAPI
import uvicorn
from typing import Any, Dict

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
