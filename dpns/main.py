import uvicorn
import asyncio
from fastapi import FastAPI
from config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.0.1",
)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)