import uvicorn
import asyncio
from fastapi import FastAPI
from config import settings
from routes.users.route import users_router
from routes.tokens.route import tokens_router
from routes.devices.route import devices_router
from routes.problems.route import problems_router

app = FastAPI(
    title=settings.app_name,
    version="0.0.1",
)

app.include_router(devices_router, tags=['Devices'], prefix='/devices')
app.include_router(problems_router, tags=['Problems'], prefix='/problems')
app.include_router(users_router, tags=['Users'], prefix='/users')
app.include_router(tokens_router, tags=['Tokens'], prefix='/tokens')


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)