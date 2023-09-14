import json
from fastapi import HTTPException
from typing import Dict

from app import Session
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.domain.request_domain import InterviewCreateInfo
from app.prompt.persona import persona
from app.prompt.question import question
from app.prompt.virtual_interview import virtual_interview


class InterviewPrepareRepository:
    def __init__(self, session=None):
        self.session = Session()

    def create_interview(self, user_id: int, interview_info: InterviewCreateInfo):
        try:
            if interview_info.status not in [1, 2, 3, 4]:
                raise HTTPException(status_code=406, detail="제품 개발 상태가 올바르지 않습니다.")
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = Interview(user_id=user_id, **dict(interview_info))
            self.session.add(interview)
            self.session.commit()
            return {
                "interviewId": interview.interview_id,
            }
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_persona(self, user_id: int, interview_id: int):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")

            # 페르소나 생성
            persona_result = persona(
                product_name=interview.product_name,
                product_detail=interview.product_detail,
                interview_goal=interview.interview_goal,
                target_user=interview.target_user,
            )

            interview.persona = persona_result
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "persona": json.loads(persona_result),
            }
            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_question_list(self, user_id: int, interview_id: int):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")

            # 질문리스트 생성
            question_list_result = question(
                product_name=interview.product_name,
                product_detail=interview.product_detail,
                interview_goal=interview.interview_goal,
                target_user=interview.target_user,
            )

            interview.question_list = question_list_result
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "productName": interview.product_name,
                "interviewGoal": interview.interview_goal,
                "status": interview.status,
                "questionList": json.loads(question_list_result),
            }
            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_virtual_interview(self, user_id: int, interview_id: int):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")

            # 가상인터뷰 생성
            virtual_interview_result = virtual_interview(
                product_name=interview.product_name,
                product_detail=interview.product_detail,
                interview_goal=interview.interview_goal,
                target_user=interview.target_user,
                persona=interview.persona,
                question_list=interview.question_list,
            )

            interview.virtual_interview = virtual_interview_result
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "virtualInterview": json.loads(virtual_interview_result),
            }
            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
