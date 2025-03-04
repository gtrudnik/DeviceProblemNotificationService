from fastapi import APIRouter, Depends
from dpns.db.connector import controller
from dpns.schemas.status import Status
from dpns.libs.user_auth import get_token

problems_router = APIRouter()


@problems_router.post("/create")
async def create_problem(device_id: int,
                         description: str | None = None,
                         type_problem: str | None = None):
    await controller.create_problem(author_id=1,
                                    device_id=device_id,
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
async def get_problems_by_author(author: int):
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
