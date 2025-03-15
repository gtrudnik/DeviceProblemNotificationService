from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Response
from dpns.libs.user_auth import create_access_token

auth_router = APIRouter()


class LoginForm(BaseModel):
    user: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    email: str


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
    return AuthResponse(access_token=token, token_type="jwt", email=login_form.user)
