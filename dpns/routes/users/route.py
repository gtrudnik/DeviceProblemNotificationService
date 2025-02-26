from fastapi import APIRouter
from dpns.db.connector import controller
from enum import Enum


class Roles(str, Enum):
    super_admin = "super_admin"
    admin = 'admin'
    user = 'user'
    banned = 'banned'


users_router = APIRouter()


# @users_router.post("/create")
# async def create_user():
#     pass


@users_router.post("/change_role")
async def change_role(new_role: Roles,
                      user_id: int | None = None,
                      tg_id: int | None = None,
                      login: str | None = None):
    if [user_id, login, tg_id].count(None) != 2:
        return "You should choose one parameter: user_id, login or tg_id"
    user = await controller.change_role(new_role=new_role, user_id=user_id, tg_id=tg_id, login=login)
    if user is None:
        return "User is not exist"
    return "Role updated "


@users_router.post("/connect_tg")
async def connect_tg():
    pass


@users_router.get("/get")
async def get_user(user_id: int | None = None,
                   tg_id: int | None = None,
                   login: str | None = None):
    user = await controller.get_user(user_id=user_id, tg_id=tg_id, login=login)
    if user is None:
        return "User is not exist"
    return user
