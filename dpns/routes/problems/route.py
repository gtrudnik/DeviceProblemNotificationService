from fastapi import APIRouter, Depends, Request
from dpns.db.connector import controller
from dpns.schemas.status import Status
from dpns.tg_bot import send_message
from dpns.scheduler import celery_tasks
from typing import Annotated
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access
from pydantic import BaseModel
from datetime import datetime

problems_router = APIRouter()


class ProblemResponse(BaseModel):
    id: int
    description: str | None = None
    status: str
    resolver: int | None
    type_problem: str | None = None
    date_created: datetime

    device_id: int
    device_name: str
    device_building: str
    device_floor: int
    device_room: str

    grade: int | None = None
    feedback: str | None = None


@problems_router.post("/create")
async def create_problem(jwt_data: Annotated[dict | None, Depends(get_token)],
                         token_data: Annotated[dict | None, Depends(has_token)],
                         device_id: int,
                         description: str | None = None,
                         type_problem: str | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    await controller.create_problem(author_id=jwt_data["id"],
                                    device_id=device_id,
                                    description=description,
                                    type_problem=type_problem)
    admins = await controller.get_device_admins(device_id=device_id)
    tg_admins = [admin.tg_id for admin in admins if admin.tg_id is not None]
    try:
        # await send_message(tg_admins, "test_for_admin")
        celery_tasks.schedule_send_message.apply_async(args=[tg_admins, "test_for_admin"])
    except:
        print("error tg send")


@problems_router.post("/change_status")
async def change_status_problem(jwt_data: Annotated[dict | None, Depends(get_token)],
                                token_data: Annotated[dict | None, Depends(has_token)],
                                problem_id: int,
                                status: Status):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
    await controller.change_problem_status(problem_id=problem_id, status=status)
    authors = await controller.get_authors_by_problem(problem=problem_id)
    tg_authors = [author.tg_id for author in authors if author.tg_id is not None]
    try:
        # await send_message(tg_authors, "test_for_authors")
        celery_tasks.schedule_send_message.apply_async(args=[tg_authors, "test_for_authors"])
    except:
        print("error tg send")


@problems_router.post("/set_resolver")
async def set_resolver_problem(jwt_data: Annotated[dict | None, Depends(get_token)],
                               token_data: Annotated[dict | None, Depends(has_token)],
                               problem_id: int,
                               resolver: int | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
    await controller.set_problem_resolver(problem_id=problem_id, resolver=resolver if resolver is not None else jwt_data["id"])


@problems_router.post("/feedback")
async def feedback_problem(jwt_data: Annotated[dict | None, Depends(get_token)],
                           token_data: Annotated[dict | None, Depends(has_token)],
                           problem_id: int,
                           grade: int,
                           comment: str | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    await controller.add_problem_feedback(problem_id=problem_id,
                                          author_id=jwt_data["id"],
                                          grade=grade,
                                          comment=comment)


@problems_router.post("/create_problem_type")
async def get_problems_types(jwt_data: Annotated[dict | None, Depends(get_token)],
                             token_data: Annotated[dict | None, Depends(has_token)],
                             type_device_id: int,
                             name: str,
                             description: str | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    problem_types = await controller.create_problem_type(name=name, description=description,
                                                         type_device_id=type_device_id)
    return problem_types


@problems_router.get("/get")
async def get_problem(problem_id: int):
    problem = await controller.get_problem_by_id(problem_id=problem_id)
    return problem


@problems_router.get("/get_by_author")
async def get_problems_by_author(jwt_data: Annotated[dict | None, Depends(get_token)],
                                 token_data: Annotated[dict | None, Depends(has_token)],
                                 author: int | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    problems = await controller.get_problems_by_author(author=author if author is not None else jwt_data["id"])
    devices_id = [i[0].device for i in problems]
    devices = await controller.get_list_devices(devices_id)
    problems_response = []
    for problem_ in problems:
        problem, grade, feedback = problem_
        for device in devices:
            if device.id == problem.device:
                problems_response.append(ProblemResponse(
                    id=problem.id,
                    description=problem.description,
                    status=problem.status,
                    resolver=problem.resolver,
                    type_problem=problem.type_problem,
                    date_created=problem.date_created,

                    device_id=device.id,
                    device_name=device.name,
                    device_building=device.building,
                    device_floor=device.floor,
                    device_room=device.room,

                    grade=grade,
                    feedback=feedback,
                ))
    return problems_response


@problems_router.get("/get_by_resolver")
async def get_problems_by_resolver(jwt_data: Annotated[dict | None, Depends(get_token)],
                                   token_data: Annotated[dict | None, Depends(has_token)],
                                   resolver: int|None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data, roles=("admin", "super_admin"))
    problems = await controller.get_problems_by_resolver(resolver=resolver if resolver is not None else jwt_data["id"])
    devices_id = [i.device for i in problems]

    admin_devices = await controller.get_admin_devices(admin_id=resolver if resolver is not None else jwt_data["id"])
    admin_devices_id = [i.id for i in admin_devices]
    new_problems = await controller.get_new_problems_by_devices(devices_id=admin_devices_id)

    devices = await controller.get_list_devices(devices_id + admin_devices_id)

    problems_response = []
    for problem in problems + new_problems:
        for device in devices:
            if device.id == problem.device:
                problems_response.append(ProblemResponse(
                    id=problem.id,
                    description=problem.description,
                    status=problem.status,
                    resolver=problem.resolver,
                    type_problem=problem.type_problem,
                    date_created=problem.date_created,

                    device_id=device.id,
                    device_name=device.name,
                    device_building=device.building,
                    device_floor=device.floor,
                    device_room=device.room,
                ))

    return problems_response


@problems_router.get("/get_all")
async def get_all_problems(jwt_data: dict = Depends(get_token)):
    problems = await controller.get_all_problems()
    return problems


@problems_router.get("/get_types")
async def get_problems_types(jwt_data: Annotated[dict | None, Depends(get_token)],
                             token_data: Annotated[dict | None, Depends(has_token)],
                             type_device: int):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    problem_types = await controller.get_problem_types(type_device=type_device)
    return problem_types
