from fastapi import HTTPException, status


async def get_access(token_data, jwt_data, roles: tuple = ("user", "admin", "super_admin")):
    if token_data is None and jwt_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if token_data:
        if token_data["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User without permission')
        return "token"
    if jwt_data:
        if jwt_data["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User without permission')
        return "jwt"

