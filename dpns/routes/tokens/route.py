from fastapi import APIRouter
from dpns.db.connector import controller

tokens_router = APIRouter()


@tokens_router.post("/create")
async def create_token(name: str, role: str):
    res = await controller.add_token(name=name, role=role)
    return res


@tokens_router.delete("/delete")
async def delete_token(name: str):
    res = await controller.del_token(name=name)
    return res
