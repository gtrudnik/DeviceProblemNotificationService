from fastapi import APIRouter
from dpns.db.connector import controller
from enum import Enum


class Status(str, Enum):
    active = "active"
    resolved = 'resolved'


problems_router = APIRouter()


@problems_router.post("/create")
async def create_problem(device_id: int,
                         description: str | None = None,
                         type_problem: str | None = None):
    await controller.create_problem(device_id=device_id,
                                    description=description,
                                    type_problem=type_problem)
    # TODO: user who create problem


@problems_router.post("/change_status")
async def change_status_problem(problem_id: int,
                                status: Status):
    await controller.change_problem_status(problem_id=problem_id, status=status)


@problems_router.post("/set_resolver")
async def set_resolver_problem(problem_id: int,
                               resolver: int):
    await controller.set_problem_resolver(problem_id=problem_id, resolver=resolver)


@problems_router.post("/feedback")
async def feedback_problem():
    pass


@problems_router.get("/get")
async def get_problem(problem_id: int):
    problem = await controller.get_problem_by_id(problem_id=problem_id)
    return problem


@problems_router.get("/get_by_user")
async def get_problems_by_user():
    pass


@problems_router.get("/get_by_resolver")
async def get_problems_by_resolver():
    pass


@problems_router.get("/get_all")
async def get_all_problems():
    problems = await controller.get_all_problems()
    return problems


@problems_router.get("/get_types")
async def get_problems_types():
    pass
