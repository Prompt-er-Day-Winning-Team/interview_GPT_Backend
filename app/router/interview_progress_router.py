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
@interview_progress_router.get(
    path="",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "interview_id": 12,
                            "name": "인터뷰 1",
                            "interview_contents": "",
                            "interview_insight": "",
                            "updated_at": "2023-09-15T02:13:21",
                            "interview_result_id": 3,
                            "interview_url": "https://i-dot-gpt.com/interview-helper/users/1/interviews/12/interview-results/3",
                            "interview_summary": "",
                            "created_at": "2023-09-15T02:13:21",
                        }
                    ]
                }
            }
        }
    },
)
async def read_interview_result_all(user_id: int, interview_id: int):
    interview_progress_repo = InterviewProgressRepository()
    interview_results = interview_progress_repo.read_interview_result_all(
        user_id=user_id, interview_id=interview_id
    )
    return interview_results


# 인터뷰 결과 생성
@interview_progress_router.post(
    path="",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewId": 12,
                        "interviewResultId": 3,
                        "name": "인터뷰 1",
                        "interviewUrl": "https://i-dot-gpt.com/interview-helper/users/1/interviews/12/interview-results/3",
                    }
                }
            }
        }
    },
)
async def create_interview_result(user_id: int, interview_id: int):
    interview_progress_repo = InterviewProgressRepository()
    persona = interview_progress_repo.create_interview_result(
        user_id=user_id, interview_id=interview_id
    )
    return persona


# 인터뷰 진행
@interview_progress_router.post(
    path="/{interview_result_id}",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "isFinished": False,
                        "interviewQuestion": "I.GPT 인터뷰 질문 생성 기능에서 개선되었으면 하는 부분은 무엇인가요?",
                    }
                }
            }
        }
    },
)
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
