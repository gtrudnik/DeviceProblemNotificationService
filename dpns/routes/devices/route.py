from fastapi import APIRouter
from dpns.db.connector import controller

devices_router = APIRouter()


@devices_router.post("/create")
async def create_device(name: str,
                        building: str,
                        floor: int,
                        room: str,
                        location_description: str | None = None,
                        description: str | None = None,
                        type_device: int | None = None):
    try:
        await controller.create_device(name=name,
                                       type_device=type_device,
                                       building=building,
                                       floor=floor,
                                       room=room,
                                       location_description=location_description,
                                       description=description)
    except Exception as e:
        print(e)
        return "Error while creating device"


@devices_router.post("/update")
async def update_device(device_id: int,
                        building: str | None = None,
                        floor: int | None = None,
                        room: str | None = None,
                        location_description: str | None = None,
                        description: str | None = None):
    try:
        await controller.update_device(device_id=device_id,
                                       building=building,
                                       floor=floor,
                                       room=room,
                                       location_description=location_description,
                                       description=description)
    except:
        return "Error while updating device"


@devices_router.post("/set_admin")
async def set_admin_device(device_id: int,
                           admin_id: int):
    await controller.add_admin_device(device_id=device_id, admin_id=admin_id)


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
async def delete_device(device_id: int):
    await controller.delete_device(device_id=device_id)
