from fastapi import APIRouter
tokens_router = APIRouter()


@tokens_router.post("/create")
async def create_token():
    pass


@tokens_router.delete("/delete")
async def delete_token():
    pass
