from os import stat
from typing import Optional, List
from fastapi import APIRouter, Depends

# from app.core.helper import check_jwt
from app.repository.interview_prepare_repo import InterviewPrepareRepository
from app.domain.request_domain import InterviewCreateInfo


interview_prepare_router = APIRouter(
    prefix="/v1/users/{user_id}/prepare/interviews",
    tags=["interview_prepare"],
    # dependencies=[Depends(check_jwt)],
    responses={404: {"description": "Not Found!!!"}},
)


# 인터뷰 기본정보 입력
@interview_prepare_router.post(path="")
async def create_interview(user_id: int, interview_info: InterviewCreateInfo):
    interview_prepare_repo = InterviewPrepareRepository()
    persona = interview_prepare_repo.create_interview(
        user_id=user_id, interview_info=interview_info
    )
    return persona


# 인터뷰 페르소나 생성
@interview_prepare_router.post(path="/{interview_id}/persona")
async def create_persona(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    persona = interview_prepare_repo.create_persona(
        user_id=user_id, interview_id=interview_id
    )
    return persona


# 인터뷰 질문지 생성
@interview_prepare_router.post(path="/{interview_id}/question-list")
async def create_question_list(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    question_list = interview_prepare_repo.create_question_list(
        user_id=user_id, interview_id=interview_id
    )
    return question_list


# 가상 인터뷰 시뮬레이션 생성
@interview_prepare_router.post(path="/{interview_id}/virtual-interview")
async def create_virtual_interview(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    question_list = interview_prepare_repo.create_virtual_interview(
        user_id=user_id, interview_id=interview_id
    )
    return question_list
