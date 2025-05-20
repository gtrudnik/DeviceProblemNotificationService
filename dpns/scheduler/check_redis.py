import redis
from dpns.config import settings

r = redis.Redis(host='localhost', port=6379, db=0, username=settings.redis_user, password=settings.redis_user_password)

try:
    info = r.info()
    response = r.ping()
    if response:
        print("Подключение успешно! Версия Redis:", info['redis_version'])
    else:
        print("Не удалось подключиться к Redis.")
except redis.exceptions.RedisError as e:
    print(f"Ошибка: {e}")