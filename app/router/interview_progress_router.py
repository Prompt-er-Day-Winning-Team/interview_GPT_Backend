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


# 단일 인터뷰 결과 확인
@interview_progress_router.get(
    path="/{interview_result_id}",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewResultId": 1,
                        "interviewSummary": [
                            {
                                "title": "사용자의 기능 발견 경로",
                                "text": "사용자는 친구의 추천을 통해 I.GPT 인터뷰 질문 생성 기능을 알게 되었으며, 친구는 이 기능을 잘 사용하였다고 말했다. 또한, 회사 동료가 이 기능을 사용하는 것을 보고 편리함을 느꼈다.",
                            },
                            {
                                "title": "사용자의 만족도",
                                "text": "사용자는 I.GPT 인터뷰 질문 생성 기능이 편리하다고 느꼈다. 특히, 팀 미팅 후 주요 논의 사항을 바로 텍스트로 확인하는 것이 매우 편리하다고 느꼈다.",
                            },
                        ],
                        "interviewContents": [
                            {
                                "question": "I.GPT 인터뷰 질문 생성 기능을 처음 사용하게 된 계기는 무엇인가요?",
                                "answer": "친구가 추천해줬어요.",
                            },
                            {
                                "question": "'친구가 추천해줬다고 하셨는데, 그 친구가 왜 이 기능을 추천하게 되었는지 알 수 있을까요?'",
                                "answer": "본인이 정말 잘썼대요.",
                            },
                        ],
                    }
                }
            }
        }
    },
)
async def read_interview_result(
    user_id: int,
    interview_id: int,
    interview_result_id: int,
):
    interview_progress_repo = InterviewProgressRepository()
    interview_contents = interview_progress_repo.read_interview_result(
        user_id=user_id,
        interview_id=interview_id,
        interview_result_id=interview_result_id,
    )

    return interview_contents
