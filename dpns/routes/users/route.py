from fastapi import APIRouter
users_router = APIRouter()


# @users_router.post("/create")
# async def create_user():
#     pass


@users_router.post("/change_role")
async def change_role():
    pass


@users_router.post("/connect_tg")
async def connect_tg():
    pass


@users_router.get("/get")
async def get_user():
    pass

