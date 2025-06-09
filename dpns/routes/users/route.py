from fastapi import APIRouter, Depends
from typing import Annotated
from dpns.db.connector import controller
from dpns.schemas.role import Roles
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access

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


# @users_router.post("/connect_tg")
# async def connect_tg():
#     pass


@users_router.get("/get")
async def get_user(jwt_data: Annotated[dict | None, Depends(get_token)],
                   token_data: Annotated[dict | None, Depends(has_token)],
                   user_id: int | None = None,
                   tg_id: int | None = None,
                   login: str | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    user = await controller.get_user(user_id=user_id, tg_id=tg_id, login=login)
    if user is None:
        return "User is not exist"
    return user


@users_router.get("/get_all")
async def get_user(jwt_data: Annotated[dict | None, Depends(get_token)],
                   token_data: Annotated[dict | None, Depends(has_token)]):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("super_admin",))
    users = await controller.get_all_users()
    return users