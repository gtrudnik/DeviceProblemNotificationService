from pydantic import BaseModel
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Response, Depends
from dpns.libs.user_auth import create_access_token
from dpns.db.connector import controller
from dpns.libs.token_auth import has_token
from dpns.libs.user_auth import get_token
from dpns.libs.accesses import get_access

auth_router = APIRouter()


class LoginForm(BaseModel):
    user: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    email: str
    role: str


@auth_router.post("/auth")
async def auth(response: Response, login_form: LoginForm) -> AuthResponse:
    """ Auth route by AD, if successful set jwt token in cookies """
    if login_form.password == "12345678":
        print(1)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong login or password")
    token = await create_access_token({"login": login_form.user})
    response.set_cookie("access_token", token, httponly=True, secure=True, samesite='none')
    user = await controller.get_user(login=login_form.user)
    return AuthResponse(access_token=token, token_type="jwt", email=login_form.user, role=user.role)


@auth_router.post("/logout")
async def logout(response: Response):
    """Logout route to clear the access token cookie"""
    response.delete_cookie("access_token", httponly=True, secure=True, samesite='none')
    return {"detail": "Successfully logged out"}


@auth_router.post("/connect_tg")
async def connect_tg(jwt_data: Annotated[dict | None, Depends(get_token)],
                     token_data: Annotated[dict | None, Depends(has_token)],
                     tg_id: int, tg_code: int):
    """ Connect tg """
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    res = await controller.check_tg_code(tg_id=tg_id, tg_code=tg_code)
    print(res)
    if res["message"] == "Accepted":
        await controller.connect_tg(user_id=jwt_data['id'], tg_id=tg_id)

    return res


@auth_router.post("/unconnect_tg")
async def unconnect_tg(jwt_data: Annotated[dict | None, Depends(get_token)],
                       token_data: Annotated[dict | None, Depends(has_token)],):
    """ Unconnect tg """
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    await controller.unconnect_tg(user_id=jwt_data['id'])


@auth_router.post("/get_tg")
async def get_tg(jwt_data: Annotated[dict | None, Depends(get_token)],
                       token_data: Annotated[dict | None, Depends(has_token)],):
    """ Get tg """
    auth_type = await get_access(token_data=token_data, jwt_data=jwt_data)
    user = await controller.get_user(user_id=jwt_data['id'])
    return {"tg_id": user.tg_id}


