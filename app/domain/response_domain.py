from typing import Optional, List
from datetime import date

from app.domain import CamelModel


# 인터뷰 기본정보 입력
class InterviewCreateInfo(CamelModel):
    product_name: str
    product_detail: str
    interview_goal: str
    target_user: str
    status: str

    class Config:
        from_attributes = True
