from datetime import datetime, timezone, timedelta
from jose import jwt, ExpiredSignatureError
from dpns.config import settings
from fastapi import HTTPException, status, Request, Response
from dpns.db.connector import controller


async def create_access_token(data: dict) -> str:
    """ Create jwt token """
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=30)})
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.secret_algorithm)
    return token


async def get_data_from_token(token):
    """ Decode token """
    return jwt.decode(token, settings.secret_key, settings.secret_algorithm)


async def get_token(request: Request, response: Response):
    """ Get token from cookies and check if it's expired.
    If it will be expired in short time, update token.
    """
    token = request.cookies.get('access_token')
    if not token:
        return False
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    try:
        await get_data_from_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')
    data = await get_data_from_token(token)
    login = data["login"]
    user = await controller.get_user(login=login)
    if datetime.fromtimestamp(data["exp"], tz=timezone.utc) - datetime.now(timezone.utc) < timedelta(minutes=10):
        token = await create_access_token({"login": login})
        response.set_cookie("access_token", token, httponly=True)
    # if user.role == "Banned":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User without permission')
    return {"id": user.id, "role": user.role}
