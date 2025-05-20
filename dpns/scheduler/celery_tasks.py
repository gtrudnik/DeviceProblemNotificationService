from celery import Celery
from dpns.config import settings
from dpns.tg_bot import send_message
import asyncio


app = Celery('tasks', broker=f"redis://{settings.redis_user}:{settings.redis_user_password}@localhost:6379")
app.conf.timezone = 'UTC'


@app.task
def schedule_send_message(chat_id: int | list[int], message: str):
    asyncio.run(send_message(chat_id, message))
    return f"message '{message}' to {chat_id} "

