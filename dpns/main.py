import uvicorn
import asyncio
from fastapi import FastAPI
from config import settings
from routes.users.route import users_router
from routes.tokens.route import tokens_router
from routes.devices.route import devices_router
from routes.problems.route import problems_router
from routes.auth.route import auth_router
from multiprocessing import Process
from tg_bot import start_bot

app = FastAPI(
    title=settings.app_name,
    version="0.0.1",
)


app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(devices_router, tags=['Devices'], prefix='/devices')
app.include_router(problems_router, tags=['Problems'], prefix='/problems')
app.include_router(users_router, tags=['Users'], prefix='/users')
app.include_router(tokens_router, tags=['Tokens'], prefix='/tokens')


def bot_app():
    asyncio.run(start_bot())


@app.on_event('startup')
async def on_startup():
    """Function for starting TelegramBot"""
    try:
        proc = Process(target=bot_app)
        proc.start()
    except:
        pass


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)