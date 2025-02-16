from fastapi import APIRouter
devices_router = APIRouter()


@devices_router.post("/create")
async def create_device():
    pass


@devices_router.post("/update")
async def update_device():
    pass


@devices_router.post("/set_admin")
async def set_admin_device():
    pass


@devices_router.post("/new_type")
async def new_device_type():
    pass


@devices_router.get("/get")
async def get_device():
    pass


@devices_router.get("/get_by_user")
async def get_device_by_user():
    pass


@devices_router.get("/get_by_admin")
async def get_device_by_admin():
    pass


@devices_router.get("/get_all")
async def get_all_devices():
    pass


@devices_router.delete("/delete")
async def delete_device():
    pass
