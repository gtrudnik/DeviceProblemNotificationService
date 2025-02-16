from fastapi import APIRouter
problems_router = APIRouter()


@problems_router.post("/create")
async def create_problem():
    pass


@problems_router.post("/change_status")
async def change_status_problem():
    pass


@problems_router.post("/set_resolver")
async def set_resolver_problem():
    pass


@problems_router.post("/feedback")
async def feedback_problem():
    pass


@problems_router.get("/get")
async def get_problem():
    pass


@problems_router.get("/get_by_user")
async def get_problems_by_user():
    pass


@problems_router.get("/get_by_resolver")
async def get_problems_by_resolver():
    pass


@problems_router.get("/get_all")
async def get_all_problems():
    pass


@problems_router.get("/get_types")
async def get_problems_types():
    pass
