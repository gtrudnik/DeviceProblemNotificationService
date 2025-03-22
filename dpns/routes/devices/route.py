from fastapi import APIRouter, Depends
from dpns.db.connector import controller
from pydantic import BaseModel
from typing import Annotated
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access

devices_router = APIRouter()


class DeviceResponse(BaseModel):
    device_id: int
    name: str
    building: str
    floor: int
    room: str
    location_description: str | None = None
    description: str | None = None
    type_device_id: int | None = None
    type_device: str | None = None


@devices_router.post("/create")
async def create_device(jwt_data: Annotated[dict | None, Depends(get_token)],
                        token_data: Annotated[dict | None, Depends(has_token)],
                        name: str,
                        building: str,
                        floor: int,
                        room: str,
                        location_description: str | None = None,
                        description: str | None = None,
                        type_device: int | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
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
async def new_device_type(name: str):
    await controller.create_device_type(name=name)


@devices_router.get("/get")
async def get_device(device_id: int):
    device_db, type_device = await controller.get_device_by_id(device_id=device_id)
    return DeviceResponse(device_id=device_db.id,
                          name=device_db.name,
                          building=device_db.building,
                          floor=device_db.floor,
                          room=device_db.room,
                          location_description=device_db.location_description,
                          description=device_db.description,
                          type_device_id=device_db.type_device,
                          type_device=type_device)


@devices_router.get("/get_by_admin")
async def get_device_by_admin(jwt_data: Annotated[dict | None, Depends(get_token)],
                              token_data: Annotated[dict | None, Depends(has_token)],
                              admin_id: int | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
    devices = await controller.get_admin_devices(admin_id=admin_id if admin_id is not None else jwt_data['id'])
    return devices


@devices_router.get("/get_all")
async def get_all_devices():
    devices = await controller.get_all_devices()
    return devices


@devices_router.get("/get_all_type_devices")
async def get_all_type_devices(jwt_data: Annotated[dict | None, Depends(get_token)],
                               token_data: Annotated[dict | None, Depends(has_token)],):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
    types_devices = await controller.get_all_types_devices()
    return types_devices


@devices_router.delete("/delete")
async def delete_device(device_id: int):
    await controller.delete_device(device_id=device_id)
