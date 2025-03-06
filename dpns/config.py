import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = "Device Problem Notification Service"
    db_driver: str = "postgresql+asyncpg"
    postgres_user: str = os.getenv('POSTGRES_USER')
    postgres_password: str = os.getenv('POSTGRES_PASSWORD')
    postgres_host: str = os.getenv('POSTGRES_HOST')
    postgres_port: str = os.getenv('POSTGRES_PORT')
    postgres_db: str = os.getenv('POSTGRES_DB')

    secret_key: str = os.getenv('SECRET_KEY', "")
    secret_algorithm: str = "HS256"

    token: str = os.getenv('TG_TOKEN')


settings = Settings()
