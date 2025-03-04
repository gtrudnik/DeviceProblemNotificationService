from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dpns.db.connector import controller

bearer = HTTPBearer(auto_error=False)


async def has_token(token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)]):
    """ Is token exists and valid

                Args:
                    token (Annotated[HTTPAuthorizationCredentials, Depends): bearer token (Authorization: 'bearer {token}')
                    types_token - types token to give permission for this route
                Raises:
                    HTTPException: Bad token

                Returns:
                    bool: bool: True, if token exists, and with token_type
                """
    try:
        if not token.credentials:
            return None
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")
    except:
        return None
    token = await controller.check_token(token.credentials)
    if token is None:
        return None
    return {"id": token.id, "role": token.role}
