import jwt
from fastapi import Depends, Header, HTTPException, status

from app import oauth2_scheme
from app.core.config import config


admin_username_list = [config.admin_username_master, config.admin_username_shpark, config.admin_username_jsshin, config.admin_username_doctor, config.admin_username_doctor2, config.admin_username_doctor3]
admin_password_list = [config.admin_password_master, config.admin_password_shpark, config.admin_password_jsshin, config.admin_password_doctor, config.admin_password_doctor2, config.admin_username_doctor3]

async def check_jwt(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)
        username: str = payload.get("username")
        password: str = payload.get("password")
        if username not in admin_username_list or password not in admin_password_list:
            raise credentials_exception
    except:
        raise credentials_exception
    return True
    # credentials_exception = HTTPException()
    # try:
    #     token = token.split(' ')[1]
    #     payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
    #     if payload['email'] not in admin_email_list or payload['pwd'] not in admin_pwd_list:
    #         raise Exception("로그인에 실패하였습니다.")
    # except jwt.exceptions.InvalidTokenError:
    #     raise credentials_exception
    # return True

# async def check_jwt(token: str = Header(None, convert_underscores=False)):
#     credentials_exception = HTTPException()
#     try:
#         token = token.split(' ')[1]
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
#         if payload['email'] not in admin_email_list or payload['pwd'] not in admin_pwd_list:
#             raise Exception("로그인에 실패하였습니다.")
#     except jwt.exceptions.InvalidTokenError:
#         raise credentials_exception
#     return True