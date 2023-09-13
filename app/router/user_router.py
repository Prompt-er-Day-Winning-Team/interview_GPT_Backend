from os import stat
from typing import Optional, List
from fastapi import APIRouter, Depends

# from app.core.helper import check_jwt
from app.repository.interview_repo import InterviewRepository
from app.domain.request_domain import UserInfo, InterviewCreateInfo
from app.repository.user_repo import UserRepository


user_router = APIRouter(
    prefix="/v1",
    tags=["user"],
    # dependencies=[Depends(check_jwt)],
    responses={404: {"description": "Not Found!!!"}},
)


# 회원가입
@user_router.post(path="/users")
async def create_user(user_info: UserInfo):
    user_repo = UserRepository()
    status = user_repo.create_user(user_info=user_info)
    return status


# 로그인
@user_router.post(path="/login")
async def check_user(user_info: UserInfo):
    user_repo = UserRepository()
    status = user_repo.check_user(user_info=user_info)
    return status
