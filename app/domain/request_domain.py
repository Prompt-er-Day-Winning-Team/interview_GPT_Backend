from typing import Optional, List
from datetime import date

from app.domain import CamelModel


# 회원가입 정보 입력
class UserInfo(CamelModel):
    id: str
    password: str

    model_config = {
        "json_schema_extra": {"examples": [{"id": "test", "password": "1234"}]},
        "from_attributes": True,
    }


# 인터뷰 기본정보 입력
class InterviewCreateInfo(CamelModel):
    product_name: str
    product_detail: str
    interview_goal: str
    target_user: str
    status: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "productName": "I.GPT 인터뷰 질문 생성 기능",
                    "productDetail": "기업들의 사용자 인터뷰를 원활히 진행하기 위해 GPT API를 활용하여 인터뷰 질문을 자동생성하는 기능",
                    "interviewGoal": "I.GPT 인터뷰 질문 생성 기능의 부족한 점 파악",
                    "targetUser": "사용자 인터뷰를 진행하는 IT 기업 서비스 기획자",
                    "status": 1,
                }
            ]
        },
        "from_attributes": True,
    }


# 인터뷰 내용 전달
class InterviewContentsInfo(CamelModel):
    is_finished: bool
    interview_contents: list

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "isFinished": False,
                    "interviewContents": [],
                }
            ]
        },
        "from_attributes": True,
    }
