from fastapi import APIRouter, Depends, Request
from dpns.db.connector import controller
from dpns.schemas.status import Status
from dpns.tg_bot import send_message
from typing import Annotated
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access

problems_router = APIRouter()


@problems_router.post("/create")
async def create_problem(jwt_data: Annotated[dict | None, Depends(get_token)],
                         token_data: Annotated[dict | None, Depends(has_token)],
                         device_id: int,
                         description: str | None = None,
                         type_problem: str | None = None):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    await controller.create_problem(author_id=1,
                                    device_id=device_id,
                                    description=description,
                                    type_problem=type_problem)
    admins = await controller.get_device_admins(device_id=device_id)
    tg_admins = [admin.tg_id for admin in admins if admin.tg_id is not None]
    await send_message(tg_admins, "test_for_admin")
    # TODO: user who create problem


@problems_router.post("/change_status")
async def change_status_problem(problem_id: int,
                                status: Status):
    await controller.change_problem_status(problem_id=problem_id, status=status)
    authors = await controller.get_authors_by_problem(problem=problem_id)
    tg_authors = [author.tg_id for author in authors if author.tg_id is not None]
    await send_message(tg_authors, "test_for_authors")


@problems_router.post("/set_resolver")
async def set_resolver_problem(problem_id: int,
                               resolver: int):
    await controller.set_problem_resolver(problem_id=problem_id, resolver=resolver)


@problems_router.post("/feedback")
async def feedback_problem(problem_id: int,
                           author_id: int,
                           grade: int,
                           comment: str | None = None):
    # TODO: get author by auth
    await controller.add_problem_feedback(problem_id=problem_id,
                                          author_id=author_id,
                                          grade=grade,
                                          comment=comment)


@problems_router.get("/get")
async def get_problem(problem_id: int):
    problem = await controller.get_problem_by_id(problem_id=problem_id)
    return problem


@problems_router.get("/get_by_author")
async def get_problems_by_author(jwt_data: Annotated[dict | None, Depends(get_token)],
                                 token_data: Annotated[dict | None, Depends(has_token)],
                                 author: int):
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    problems = await controller.get_problems_by_author(author=author)
    return problems


@problems_router.get("/get_by_resolver")
async def get_problems_by_resolver(resolver: int):
    problems = await controller.get_problems_by_resolver(resolver=resolver)
    return problems


@problems_router.get("/get_all")
async def get_all_problems(jwt_data: dict = Depends(get_token)):
    print(jwt_data)
    problems = await controller.get_all_problems()
    return problems


@problems_router.get("/get_types")
async def get_problems_types(type_device: int):
    problem_types = await controller.get_problem_types(type_device=type_device)
    return problem_types
