from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from dpns.db.db import use_db
from dpns.libs.token_generator import generate_token, hash_md5
from dpns.db.models.token import Token
from dpns.db.models.user import User
from dpns.db.models.device import Device
from dpns.db.models.device_type import DeviceType
from dpns.db.models.device_admin import DeviceAdmin
from dpns.db.models.problem import Problem
from dpns.db.models.problem_type import ProblemType
from dpns.db.models.problem_author import ProblemAuthor
from dpns.db.models.tg_chat import TgChat
from dpns.db.models.tg_code import TgCode
from random import randint
from datetime import datetime


class Controller():
    """ Devices """

    @use_db
    async def create_device(self,
                            session: AsyncSession,
                            name: str,
                            building: str,
                            floor: int,
                            room: str,
                            location_description: str | None = None,
                            description: str | None = None,
                            type_device: int | None = None):
        device = Device(name=name, building=building,
                        floor=floor, room=room,
                        location_description=location_description,
                        description=description,
                        type_device=type_device)
        session.add(device)
        await session.commit()
        return device.id

    @use_db
    async def update_device(self,
                            session: AsyncSession,
                            device_id: int,
                            building: str | None = None,
                            floor: int | None = None,
                            room: str | None = None,
                            location_description: str | None = None,
                            description: str | None = None):
        device = (await session.execute(select(Device).filter(Device.id == device_id))).scalar()
        if device is None:
            return "Device with this id doesn't exist"
        if building is not None:
            device.building = building
        if floor is not None:
            device.floor = floor
        if room is not None:
            device.room = room
        if location_description is not None:
            device.location_description = location_description
        if description is not None:
            device.description = description
        await session.commit()

    @use_db
    async def add_admin_device(self,
                               session: AsyncSession,
                               device_id: int,
                               admin_id: int):
        device_admin = DeviceAdmin(device=device_id, admin=admin_id)
        session.add(device_admin)
        await session.commit()

    @use_db
    async def delete_admin_device(self,
                                  session: AsyncSession,
                                  device_id: int,
                                  admin_id: int):
        await session.execute(
            delete(DeviceAdmin).filter(and_(DeviceAdmin.admin == admin_id, DeviceAdmin.device == device_id)))
        await session.commit()

    @use_db
    async def delete_device(self, session: AsyncSession, device_id: int):
        await session.execute(delete(Device).filter(Device.id == device_id))
        await session.commit()

    @use_db
    async def get_device_by_id(self, session: AsyncSession, device_id: int):
        device = (await session.execute(select(Device).filter(Device.id == device_id))).scalar()
        device_type = await self.get_type_device(type_device_id=device.type_device)
        device_type = device_type.type_device if device_type is not None else None
        if device is None:
            return None, None
        return device, device_type

    @use_db
    async def get_list_devices(self, session: AsyncSession, device_id: list[int]):
        devices = (await session.execute(select(Device).filter(Device.id.in_(device_id)))).scalars().all()
        return devices

    @use_db
    async def get_all_devices(self, session: AsyncSession):
        devices = (await session.execute(select(Device))).scalars().all()
        return devices

    @use_db
    async def get_admin_devices(self, session: AsyncSession, admin_id: int):
        """ Get all devices of admin """
        query = (select(DeviceAdmin).
                 filter(DeviceAdmin.admin == admin_id).
                 outerjoin(Device).where(DeviceAdmin.device == Device.id))
        devices = (await session.execute(query)).scalars().all()
        return [i.devices for i in devices]

    @use_db
    async def get_device_admins(self, session: AsyncSession, device_id: int):
        """ Get all admins of device """
        query = (select(DeviceAdmin, User).filter(DeviceAdmin.device == device_id).
                 outerjoin(User).where(DeviceAdmin.admin == User.id))
        res = (await session.execute(query)).scalars().all()
        admins = [i.admins for i in res]
        return admins

    """ Device types """

    @use_db
    async def create_device_type(self,
                                 session: AsyncSession,
                                 name: str):
        device_type = DeviceType(type_device=name)
        session.add(device_type)
        await session.commit()

    @use_db
    async def get_all_types_devices(self, session: AsyncSession):
        device_types = (await session.execute(select(DeviceType))).scalars().all()
        return device_types

    @use_db
    async def get_type_device(self, session: AsyncSession, type_device_id: int):
        device_type = (await session.execute(select(DeviceType).filter(DeviceType.id == type_device_id))).scalar()
        return device_type

    """ Problems """

    @use_db
    async def create_problem(self,
                             session: AsyncSession,
                             author_id: int,
                             device_id: int,
                             description: str | None = None,
                             type_problem: str | None = None):
        # problem = (await session.execute(select(Problem).filter(
        #     and_(Problem.device == device_id, Problem.type_problem == type_problem,
        #          Problem.status == "active")))).scalar()
        # if problem is None or type_problem is None:
        problem = Problem(device=device_id, description=description, type_problem=type_problem)
        session.add(problem)
        # else:
        #     problem.description = problem.description + "|\n|" + description
        await session.commit()
        await self.add_problem_author(problem_id=problem.id, author_id=author_id)

    @use_db
    async def create_problem_type(self,
                                  session: AsyncSession,
                                  type_device_id: int,
                                  name: str,
                                  description: str | None = None):
        problem_type = ProblemType(type_device=type_device_id,
                                   name_problem=name, description=description)
        session.add(problem_type)
        await session.commit()

    @use_db
    async def add_problem_author(self,
                                 session: AsyncSession,
                                 problem_id: int,
                                 author_id: int):
        problem_author = ProblemAuthor(problem=problem_id, author=author_id)
        session.add(problem_author)
        await session.commit()

    @use_db
    async def add_problem_feedback(self,
                                   session: AsyncSession,
                                   problem_id: int,
                                   author_id: int,
                                   grade: int,
                                   comment: str | None = None):
        problem_author = (await session.execute(select(ProblemAuthor).filter(
            and_(ProblemAuthor.problem == problem_id, ProblemAuthor.author == author_id)))).scalar()
        if problem_author is None:
            return "Problem with this author doesn't exist"
        problem_author.grade = grade
        problem_author.comment = comment
        await session.commit()

    @use_db
    async def change_problem_status(self,
                                    session: AsyncSession,
                                    problem_id: int,
                                    status: str):
        problem = (await session.execute(select(Problem).filter(Problem.id == problem_id))).scalar()
        if problem is None:
            return "Problem with this id doesn't exist"
        problem.status = status
        await session.commit()

    @use_db
    async def set_problem_resolver(self,
                                   session: AsyncSession,
                                   problem_id: int,
                                   resolver: int):
        problem = (await session.execute(select(Problem).filter(Problem.id == problem_id))).scalar()
        if problem is None:
            return "Problem with this id doesn't exist"
        if problem.resolver:
            return "This problem already have resolver"
        problem.resolver = resolver
        await session.commit()

    @use_db
    async def delete_problem_resolver(self,
                                      session: AsyncSession,
                                      problem_id: int):
        problem = (await session.execute(select(Problem).filter(Problem.id == problem_id))).scalar()
        if problem is None:
            return "Problem with this id doesn't exist"
        if problem.resolver is None:
            return "This problem already don't have resolver"
        problem.resolver = None
        await session.commit()

    @use_db
    async def get_problems_by_resolver(self,
                                       session: AsyncSession,
                                       resolver: int):
        problems = (await session.execute(select(Problem).filter(Problem.resolver == resolver))).scalars().all()
        return problems

    @use_db
    async def get_problems_by_author(self,
                                     session: AsyncSession,
                                     author: int):
        query = (select(ProblemAuthor, Problem).
                 filter(ProblemAuthor.author == author).
                 outerjoin(Problem).where(ProblemAuthor.problem == Problem.id))
        problems = (await session.execute(query)).scalars().all()
        return [(i.problems, i.grade, i.comment) for i in problems]

    @use_db
    async def get_authors_by_problem(self,
                                     session: AsyncSession,
                                     problem: int):
        query = (select(ProblemAuthor, User).
                 filter(ProblemAuthor.problem == problem).
                 outerjoin(User).where(ProblemAuthor.author == User.id))
        authors = (await session.execute(query)).scalars().all()
        return [i.authors for i in authors]

    @use_db
    async def get_problem_by_id(self,
                                session: AsyncSession,
                                problem_id: int):
        problem = (await session.execute(select(Problem).filter(Problem.id == problem_id))).scalar()
        if problem is None:
            return "Problem with this id doesn't exist"
        return problem

    @use_db
    async def get_new_problems_by_devices(self,
                                session: AsyncSession,
                                devices_id: list[int]):
        problem = (await session.execute(select(Problem).
                                         filter(and_(Problem.device.in_(devices_id),
                                                     Problem.resolver.is_(None)
                                                                     )))).scalars().all()
        if problem is None:
            return "Problem with this id doesn't exist"
        return problem


    @use_db
    async def get_all_problems(self,
                               session: AsyncSession):
        problems = (await session.execute(select(Problem))).scalars().all()
        return problems

    @use_db
    async def get_problem_types(self,
                                session: AsyncSession,
                                type_device: int | None = None,
                                device_id: int | None = None):
        if type_device is None:
            device = (await session.execute(
                select(Device).filter(Device.id == device_id))
                      ).scalar()
            type_device = device.type_device
        problem_types = (await session.execute(
            select(ProblemType).filter(ProblemType.type_device == type_device))
                         ).scalars().all()
        return problem_types

    """ Users """

    @use_db
    async def create_user(self, session: AsyncSession, login: str | None = None, tg_id: int | None = None,
                          role: str = "user"):
        if login is None and tg_id is None:
            return "User must have tg_id or login"
        user = User(login=login, tg_id=tg_id, role=role)
        session.add(user)
        await session.commit()
        return user

    @use_db
    async def get_all_users(self, session: AsyncSession):
        users = (await session.execute(select(User))).scalars().all()
        return users

    @use_db
    async def get_user(self, session: AsyncSession, user_id: int | None = None, login: str | None = None,
                       tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if tg_id is not None:
            user = (await session.execute(select(User).filter(User.tg_id == tg_id))).scalar()
        return user

    @use_db
    async def change_role(self, session: AsyncSession, new_role: str, user_id: int | None = None,
                          login: str | None = None, tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if tg_id is not None:
            user = (await session.execute(select(User).filter(User.tg_id == tg_id))).scalar()
        user.role = new_role
        await session.commit()
        return user

    @use_db
    async def delete_user(self, session: AsyncSession, user_id: int | None = None, login: str | None = None,
                          tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            await session.execute(delete(User).filter(User.id == user_id))
        if login is not None:
            await session.execute(delete(User).filter(User.login == login))
        if tg_id is not None:
            await session.execute(delete(User).filter(User.tg_id == tg_id))
        await session.commit()

    @use_db
    async def connect_tg(self, session: AsyncSession, tg_id: int | None = None,
                         user_id: int | None = None, login: str | None = None):
        if [user_id, login].count(None) != 1:
            return "You should choose one parameter: user_id or login"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if user.tg_id is not None:
            return "User already connect tg"

        user_tg = await self.get_user(tg_id=tg_id)
        # problems on tg id redirect to user
        await session.execute(update(ProblemAuthor).
                              where(ProblemAuthor.author == user_tg.id).values(author=user.id))
        await session.execute(delete(User).filter(User.tg_id == tg_id))  # delete old tg id user
        await session.execute(update(User).where(User.id == user.id).values(tg_id=tg_id))  # set tg id
        await session.commit()

    @use_db
    async def unconnect_tg(self, session: AsyncSession,
                           user_id: int | None = None,
                           login: str | None = None):
        if [user_id, login].count(None) != 1:
            return "You should choose one parameter: user_id or login"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if user.tg_id is None:
            return "User not connected tg"

        await session.execute(update(User).where(User.id == user.id).values(tg_id=None))
        await session.commit()
        return "User unconnected tg"

    @use_db
    async def delete_tg(self, session: AsyncSession, user_id: int | None = None, login: str | None = None):
        if [user_id, login].count(None) != 1:
            return "You should choose one parameter: user_id or login"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if user.tg_id is None:
            return "User didn't connected tg"
        user.tg_id = None
        await session.commit()

    """ Tokens """

    @use_db
    async def add_token(self, session: AsyncSession, name: str, role: str):
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is not None:
            return "Token with this name already exist"
        token_text = generate_token()
        token_hash = hash_md5(token_text)
        token = Token(name=name, token=token_hash, role=role)
        session.add(token)
        await session.commit()
        return token_text

    @use_db
    async def del_token(self, session: AsyncSession, name):
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is None:
            return "Token with this name don't exist"
        await session.execute(delete(Token).filter(Token.name == name))
        await session.commit()
        return "Token deleted"

    @use_db
    async def check_token(self, session: AsyncSession, token_text: str):
        res = (await session.execute(select(Token).filter(Token.token == hash_md5(token_text)))).scalar()
        await session.commit()

        return res

    """ Tg chats """

    @use_db
    async def get_tg_chat(self, session: AsyncSession, tg_id: int):
        chat = (await session.execute(select(TgChat).filter(TgChat.tg_id == tg_id))).scalar()
        if chat is None:
            chat = TgChat(tg_id=tg_id, stage="start")
            session.add(chat)
        await session.commit()
        return chat

    @use_db
    async def update_tg_chat(self,
                             session: AsyncSession,
                             tg_id: int,
                             stage: str | None = None,
                             device_id: int | None = None,
                             problem_type: str | None = None,
                             description: str | None = None):
        chat = (await session.execute(select(TgChat).filter(TgChat.tg_id == tg_id))).scalar()
        if stage is not None:
            chat.stage = stage
        if device_id is not None:
            chat.device_id = device_id
        if problem_type is not None:
            chat.problem_type = problem_type
        if description is not None:
            chat.description = description
        await session.commit()

    @use_db
    async def clear_tg_chat(self,
                             session: AsyncSession,
                             tg_id: int):
        chat = (await session.execute(select(TgChat).filter(TgChat.tg_id == tg_id))).scalar()
        chat.stage = "start"
        chat.device_id = None
        chat.problem_type = None
        chat.description = None
        await session.commit()

    """ Tg codes """

    @use_db
    async def check_tg_code(self, session: AsyncSession, tg_id: int, tg_code: int):
        code = (await session.execute(select(TgCode).filter(TgCode.tg_id == tg_id))).scalar()
        if code is None:
            return {"message": "Tg code is not created"}
        elif code.attempts <= 0:
            return {"message": "Attempts ended"}
        elif code.code == tg_code:
            await session.delete(code)
            await session.commit()
            return {"message": "Accepted"}
        else:
            code.attempts -= 1
            await session.commit()
            return {"message": "Bad code", "attempts": code.attempts}

    @use_db
    async def create_tg_code(self, session: AsyncSession, tg_id: int):
        code = (await session.execute(select(TgCode).filter(TgCode.tg_id == tg_id))).scalar()
        tg_code = randint(100000, 999999)
        if code is None:
            code = TgCode(tg_id=tg_id, code=tg_code)
            session.add(code)
        else:
            code.code = tg_code
            code.attempts = 3
            code.date_created = datetime.utcnow()
        await session.commit()
        return code.code


controller = Controller()

# test
import asyncio

# asyncio.run(controller.create_device(name="pantum m5200x", building="A", floor=6, room="615"))
# asyncio.run(controller.delete_device(device_id=1))
# print(asyncio.run(controller.get_device_by_id(device_id=2)).name)
# print(asyncio.run(controller.get_all_devices()))
# asyncio.run(controller.update_device(device_id=2, floor=11))
# asyncio.run(controller.create_device_type(name="компьютер"))
# print(asyncio.run(controller.create_problem(device_id=3)))
# asyncio.run(controller.change_problem_status(problem_id=2, status="resolved"))
# asyncio.run(controller.set_problem_resolver(problem_id=2, resolver=1))
# asyncio.run(controller.add_admin_device(device_id=3, admin_id=1))
# print(asyncio.run(controller.get_admin_devices(admin_id=1)))
# print(asyncio.run(controller.get_device_admins(device_id=2)))
# asyncio.run(controller.add_problem_author(author_id=1, problem_id=2))
# asyncio.run(controller.add_problem_feedback(author_id=1, problem_id=2, grade=4, comment="Сделали всё хорошо и быстро"))
# asyncio.run(controller.create_problem_type(type_device_id=1, name="замятие бумаги"))
# asyncio.run(controller.create_user(login="lol888"))
# asyncio.run(controller.change_role(login="lol888", new_role="admin"))
# asyncio.run(controller.delete_user(login="lol888"))
# asyncio.run(controller.connect_tg(login="lol647", tg_id=12312312312))
# asyncio.run(controller.delete_tg(login="lol647"))
# print(asyncio.run(controller.add_token("lol", "admin")))
# print(asyncio.run(controller.check_token("4c10953948de466caaac1b98619ec8b1")))
# print(asyncio.run(controller.del_token("lol")))
# print(asyncio.run(controller.create_tg_code(331467077)))
# print(asyncio.run(controller.check_tg_code(331467077, 549335)))
# asyncio.run(controller.unconnect_tg(user_id=9))
