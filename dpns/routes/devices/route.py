from fastapi import APIRouter
from dpns.db.connector import controller
from pydantic import BaseModel

devices_router = APIRouter()


class DeviceResponse(BaseModel):
    device_id: int
    name: str
    building: str
    floor: int
    room: str
    location_description: str | None = None
    description: str | None = None
    type_device: int | None = None


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
async def get_device(device_id: int):
    device_db = await controller.get_device_by_id(device_id=device_id)
    return device_db
    # return DeviceResponse(device_id=device_db.id,
    #                       name=device_db.name,
    #                       building=device_db.building,
    #                       floor=device_db.floor,
    #                       room=device_db.room,
    #                       location_description=device_db.location_description,
    #                       description=device_db.description,
    #                       type_device=device_db.type_device)


@devices_router.get("/get_by_admin")
async def get_device_by_admin(admin_id: int):
    devices = await controller.get_admin_devices(admin_id=admin_id)
    return devices


@devices_router.get("/get_all")
async def get_all_devices():
    devices = await controller.get_all_devices()
    return devices


@devices_router.delete("/delete")
async def delete_device(device_id: int):
    await controller.delete_device(device_id=device_id)
