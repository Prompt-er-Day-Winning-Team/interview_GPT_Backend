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
@interview_prepare_router.get(
    path="",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "interviewId": 4,
                            "interviewGoal": "I.GPT 인터뷰 질문 생성 기능의 부족한 점 파악",
                            "step": 2,
                        },
                        {
                            "interviewId": 5,
                            "interviewGoal": "I.GPT 인터뷰 질문 생성 기능의 부족한 점 파악",
                            "step": 4,
                        },
                    ]
                }
            }
        }
    },
)
async def read_interview_all(user_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    interviews = interview_prepare_repo.read_interview_all(user_id=user_id)
    return interviews


# 인터뷰 기본정보 입력
@interview_prepare_router.post(
    path="",
    responses={200: {"content": {"application/json": {"example": {"interviewId": 1}}}}},
)
async def create_interview(user_id: int, interview_info: InterviewCreateInfo):
    interview_prepare_repo = InterviewPrepareRepository()
    persona = interview_prepare_repo.create_interview(
        user_id=user_id, interview_info=interview_info
    )
    return persona


# 인터뷰 페르소나 생성
@interview_prepare_router.post(
    path="/{interview_id}/persona",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewId": 12,
                        "persona": {
                            "기본정보": {"이름": "박지훈", "나이": "28세", "성별": "남성"},
                            "성격 및 취향": {
                                "성격": "침착하고 분석적인 성격, 새로운 기술에 대한 호기심이 많음",
                                "취미": "독서, 코딩, 새로운 IT 트렌드 파악",
                            },
                            "직업 및 배경": {
                                "직업": "프론트엔드 개발자",
                                "학력": "대학교 졸업 (컴퓨터공학 전공)",
                                "근무지": "스타트업",
                            },
                            "가족 및 개인 상황": {"가족 구성": "미혼, 혼자 살고 있음", "거주": "서울시 마포구 원룸"},
                            "라이프스타일": {
                                "라이프스타일": "주로 집에서 시간을 보내며, 개발 관련 정보를 찾아보거나 코딩을 하는 것을 즐김"
                            },
                        },
                    }
                }
            }
        }
    },
)
async def create_persona(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    persona = interview_prepare_repo.create_persona(
        user_id=user_id, interview_id=interview_id
    )
    return persona


# 인터뷰 질문지 생성
@interview_prepare_router.post(
    path="/{interview_id}/question-list",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewId": 12,
                        "productName": "I.GPT 인터뷰 질문 생성 기능",
                        "interviewGoal": "I.GPT 인터뷰 질문 생성 기능의 부족한 점 파악",
                        "status": 1,
                        "questionList": {
                            "서비스 편리성 및 기능성에 관한 질문": [
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능을 처음 사용하게 된 계기는 무엇인가요?",
                                    "answer": "인터뷰 질문 작성 어려움, 시간 절약, 효율적인 인터뷰 질문 생성 필요성",
                                },
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 편리하다고 느낀 부분은 무엇인가요?",
                                    "answer": "자동화된 질문 생성, 다양한 주제 abd 범위의 질문 제공, 사용자 맞춤형 질문 생성",
                                },
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능에서 개선되었으면 하는 부분은 무엇인가요?",
                                    "answer": "질문의 품질, 질문의 다양성, 사용자 맞춤형 질문 생성의 정확성",
                                },
                            ],
                            "서비스 사용 경험에 관한 질문": [
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 어려웠던 점은 무엇인가요?",
                                    "answer": "서비스 이해도, 사용 방법, 기능의 접근성",
                                },
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 만족스러웠던 점은 무엇인가요?",
                                    "answer": "질문의 품질, 시간 절약, 인터뷰 질문의 다양성",
                                },
                            ],
                            "서비스 기대치 및 향후 개선사항에 관한 질문": [
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능에 어떤 기능이 추가되었으면 좋겠나요?",
                                    "answer": "사용자 맞춤형 질문 생성, 특정 주제에 대한 질문 생성, 질문의 품질 향상",
                                },
                                {
                                    "question": "I.GPT 인터뷰 질문 생성 기능을 사용하면서 느낀 서비스의 장점과 단점은 무엇인가요?",
                                    "answer": "질문의 품질과 다양성, 사용자 맞춤형 질문 생성의 정확성, 서비스 이해도와 사용 방법의 어려움",
                                },
                            ],
                        },
                    }
                }
            }
        }
    },
)
async def create_question_list(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    question_list = interview_prepare_repo.create_question_list(
        user_id=user_id, interview_id=interview_id
    )
    return question_list


# 가상 인터뷰 시뮬레이션 생성
@interview_prepare_router.post(
    path="/{interview_id}/virtual-interview",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewId": 12,
                        "virtualInterview": {
                            "서비스 편리성 및 기능성에 관한 질문": [
                                "진행자 : 박지훈님, I.GPT 인터뷰 질문 생성 기능을 처음 사용하게 된 계기는 무엇인가요?",
                                "참가자 : 인터뷰 질문 작성이 어려워서 시간을 많이 소비하게 되었고, 그래서 효율적인 인터뷰 질문 생성이 필요하다고 느꼈습니다.",
                                "진행자 : 그럼 I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 편리하다고 느낀 부분은 무엇인가요?",
                                "참가자 : 자동화된 질문 생성과 다양한 주제 및 범위의 질문 제공, 그리고 사용자 맞춤형 질문 생성이 가장 편리했습니다.",
                                "진행자 : 그렇군요. 그럼 반대로 I.GPT 인터뷰 질문 생성 기능에서 개선되었으면 하는 부분은 무엇인가요?",
                                "참가자 : 질문의 품질과 다양성, 그리고 사용자 맞춤형 질문 생성의 정확성이 개선되었으면 좋겠습니다.",
                            ],
                            "서비스 사용 경험에 관한 질문": [
                                "진행자 : I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 어려웠던 점은 무엇인가요?",
                                "참가자 : 서비스 이해도와 사용 방법, 그리고 기능의 접근성이 어려웠습니다.",
                                "진행자 : 그럼 반대로 I.GPT 인터뷰 질문 생성 기능을 사용하면서 가장 만족스러웠던 점은 무엇인가요?",
                                "참가자 : 질문의 품질과 시간 절약, 그리고 인터뷰 질문의 다양성이 만족스러웠습니다.",
                            ],
                            "서비스 기대치 및 향후 개선사항에 관한 질문": [
                                "진행자 : I.GPT 인터뷰 질문 생성 기능에 어떤 기능이 추가되었으면 좋겠나요?",
                                "참가자 : 사용자 맞춤형 질문 생성과 특정 주제에 대한 질문 생성, 그리고 질문의 품질 향상이 필요하다고 생각합니다.",
                                "진행자 : 마지막으로, I.GPT 인터뷰 질문 생성 기능을 사용하면서 느낀 서비스의 장점과 단점은 무엇인가요?",
                                "참가자 : 질문의 품질과 다양성, 그리고 사용자 맞춤형 질문 생성의 정확성이 장점이라고 생각합니다. 반면에, 서비스 이해도와 사용 방법의 어려움이 단점이라고 생각합니다.",
                            ],
                        },
                    }
                }
            }
        }
    },
)
async def create_virtual_interview(user_id: int, interview_id: int):
    interview_prepare_repo = InterviewPrepareRepository()
    question_list = interview_prepare_repo.create_virtual_interview(
        user_id=user_id, interview_id=interview_id
    )
    return question_list
