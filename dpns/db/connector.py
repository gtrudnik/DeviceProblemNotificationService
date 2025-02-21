from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from dpns.db.db import get_session
from dpns.libs.token_generator import generate_token, hash_md5
from dpns.db.models.token import Token
from dpns.db.models.user import User
from dpns.db.models.device import Device
from dpns.db.models.device_type import DeviceType
from dpns.db.models.device_admin import DeviceAdmin
from dpns.db.models.problem import Problem
from dpns.db.models.problem_type import ProblemType
from dpns.db.models.problem_author import ProblemAuthor


class Controller():
    """ Tokens """

    @staticmethod
    async def add_token(name: str, role: str):
        session: AsyncSession = await get_session()
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is not None:
            return "Token with this name already exist"
        token_text = generate_token()
        token_hash = hash_md5(token_text)
        token = Token(name=name, token=token_hash, role=role)
        session.add(token)
        await session.commit()
        return token_text

    @staticmethod
    async def del_token(name):
        session: AsyncSession = await get_session()
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is None:
            return "Token with this name don't exist"
        await session.execute(delete(Token).filter(Token.name == name))
        await session.commit()
        return "Token deleted"

    @staticmethod
    async def check_token(token_text: str):
        session: AsyncSession = await get_session()

        res = (await session.execute(select(Token).filter(Token.token == hash_md5(token_text)))).scalar()
        await session.commit()

        if res is not None:
            return res.role
        return False


controller = Controller()

# test
# import asyncio
# print(asyncio.run(controller.add_token("lol", "admin")))
# print(asyncio.run(controller.check_token("4c10953948de466caaac1b98619ec8b1")))
# print(asyncio.run(controller.del_token("lol")))