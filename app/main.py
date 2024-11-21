from fastapi import FastAPI
import uvicorn

from app.db.database import board_collection

app = FastAPI()


@app.get("/")
async def root():
    return {"I'm ready": await board_collection.find_one(filter={})}


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
