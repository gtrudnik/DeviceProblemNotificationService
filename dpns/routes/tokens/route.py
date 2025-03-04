from fastapi import APIRouter, Depends
from dpns.db.connector import controller
from dpns.schemas.role import Roles
from typing import Annotated
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access

tokens_router = APIRouter()


@tokens_router.post("/create")
async def create_token(jwt_data: Annotated[dict | None, Depends(get_token)],
                       token_data: Annotated[dict | None, Depends(has_token)],
                       name: str, role: Roles):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("super_admin",))
    res = await controller.add_token(name=name, role=role)
    return res


@tokens_router.delete("/delete")
async def delete_token(jwt_data: Annotated[dict | None, Depends(get_token)],
                       token_data: Annotated[dict | None, Depends(has_token)],
                       name: str):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("super_admin",))
    res = await controller.del_token(name=name)
    return res
