import json
from fastapi import HTTPException
from worker import (
    create_persona_ai,
    create_question_list_ai,
    create_virtual_interview_ai,
)

from app import Session
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.domain.request_domain import InterviewCreateInfo


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

            if interview.persona:
                if interview.persona == "Waiting":
                    result = {
                        "interviewId": interview.interview_id,
                        "persona": "Waiting",
                    }
                    return result
                result = {
                    "interviewId": interview.interview_id,
                    "persona": json.loads(interview.persona),
                }
                return result

            create_persona_ai.delay(user_id, interview_id)

            interview.persona = "Waiting"
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "persona": "Waiting",
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

            if interview.question_list:
                if interview.question_list == "Waiting":
                    result = {
                        "interviewId": interview.interview_id,
                        "productName": interview.product_name,
                        "interviewGoal": interview.interview_goal,
                        "status": interview.status,
                        "questionList": "Waiting",
                    }
                    return result
                result = {
                    "interviewId": interview.interview_id,
                    "productName": interview.product_name,
                    "interviewGoal": interview.interview_goal,
                    "status": interview.status,
                    "questionList": json.loads(interview.question_list),
                }
                return result

            create_question_list_ai.delay(user_id, interview_id)

            interview.question_list = "Waiting"
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "productName": interview.product_name,
                "interviewGoal": interview.interview_goal,
                "status": interview.status,
                "questionList": "Waiting",
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

            if interview.virtual_interview:
                if interview.virtual_interview == "Waiting":
                    result = {
                        "interviewId": interview.interview_id,
                        "virtualInterview": "Waiting",
                    }
                    return result
                result = {
                    "interviewId": interview.interview_id,
                    "virtualInterview": json.loads(interview.virtual_interview),
                }
                return result

            create_virtual_interview_ai.delay(user_id, interview_id)

            interview.virtual_interview = "Waiting"
            self.session.add(interview)
            self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "virtualInterview": "Waiting",
            }
            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
