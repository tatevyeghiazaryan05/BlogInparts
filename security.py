import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer

from passlib.context import CryptContext
from jose import jwt


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/users/auth/login")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

ACCESS_TOKEN_SECRET_KEY = "G SICUNGYU BY7G 6 &tuv^  gf76G F7E4G 5Y7N GFH78 gg"


def create_access_token(user_info: dict):
    try:
        expire_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

        user_info['exp'] = expire_time
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    try:
        token = jwt.encode(user_info, ACCESS_TOKEN_SECRET_KEY, algorithm="HS256")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=['HS256'])
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return payload


def get_current_user(token=Depends(oauth2_schema)):
    try:
        payload = verify_access_token(token)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
    return payload
