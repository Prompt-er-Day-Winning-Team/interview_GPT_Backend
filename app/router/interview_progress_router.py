from os import stat
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File

# from app.core.helper import check_jwt
from app.repository.interview_progress_repo import InterviewProgressRepository
from app.domain.request_domain import InterviewContentsInfo


interview_progress_router = APIRouter(
    prefix="/v1/users/{user_id}/progress/interviews/{interview_id}/interview_results",
    tags=["interview_progress"],
    # dependencies=[Depends(check_jwt)],
    responses={404: {"description": "Not Found!!!"}},
)


# 인터뷰 결과 조회
@interview_progress_router.get(path="")
async def read_interview_result_all(user_id: int, interview_id: int):
    interview_progress_repo = InterviewProgressRepository()
    interview_results = interview_progress_repo.read_interview_result_all(
        user_id=user_id, interview_id=interview_id
    )
    return interview_results


# 인터뷰 결과 생성
@interview_progress_router.post(path="")
async def create_interview_result(user_id: int, interview_id: int):
    interview_progress_repo = InterviewProgressRepository()
    persona = interview_progress_repo.create_interview_result(
        user_id=user_id, interview_id=interview_id
    )
    return persona


# 인터뷰 진행
@interview_progress_router.post(path="/{interview_result_id}")
async def create_interview_contents(
    user_id: int,
    interview_id: int,
    interview_result_id: int,
    answer_audio_file: bytes = File(None),
):
    interview_progress_repo = InterviewProgressRepository()
    interview_contents = interview_progress_repo.create_interview_contents(
        user_id=user_id,
        interview_id=interview_id,
        interview_result_id=interview_result_id,
        answer_audio_file=answer_audio_file,
    )

    return interview_contents
