import json
from fastapi import HTTPException
from typing import Dict

from app import Session
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.repository.model.interview_result import InterviewResult
from app.prompt.persona import persona
from app.prompt.question import question
from app.prompt.virtual_interview import virtual_interview


class InterviewProgressRepository:
    def __init__(self, session=None):
        self.session = Session()

    def read_interview_result_all(self, user_id: int, interview_id: int):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")
            interview_results = (
                self.session.query(InterviewResult)
                .filter(InterviewResult.interview_id == interview_id)
                .all()
            )

            return interview_results
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_interview_result(self, user_id: int, interview_id: int):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")
            interview_result_count = (
                self.session.query(InterviewResult)
                .filter(InterviewResult.interview_id == interview_id)
                .count()
            )

            interview_result = InterviewResult(
                interview_id=interview_id, name=f"인터뷰 {interview_result_count + 1}"
            )
            self.session.add(interview_result)
            self.session.commit()

            interview_url = f"https://i-dot-gpt.com/interview-helper/users/{user_id}/interviews/{interview_id}/interview-results/{interview_result.interview_result_id}"
            interview_result.interview_url = interview_url
            self.session.add(interview_result)
            self.session.commit()

            result = {
                "interviewId": interview_id,
                "interviewResultId": interview_result.interview_result_id,
                "name": f"인터뷰 {interview_result_count + 1}",
                "interviewUrl": interview_url,
            }

            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def create_interview_contents(
        self, user_id: int, interview_id: int, interview_result_id: int
    ):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = self.session.query(Interview).get(interview_id)
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")
            interview_result = self.session.query(InterviewResult).get(
                interview_result_id
            )

            question_list = json.loads(interview.question_list)
            # if not interview_result.interview_contents:
            #     interview_result.interview_contents[question_list.keys()[0]] = {
            #         "question":
            #     }

            only_question_list = []
            for category in question_list:
                for question_set in question_list[category]:
                    only_question_list.append(question_set["question"])

            print(only_question_list)

            # # 인터뷰 질문 생성
            # persona_result = persona(
            #     product_name=interview.product_name,
            #     product_detail=interview.product_detail,
            #     interview_goal=interview.interview_goal,
            #     target_user=interview.target_user,
            # )

            # interview.persona = persona_result
            # self.session.add(interview)
            # self.session.commit()

            # result = {
            #     "interviewId": interview.interview_id,
            #     "persona": json.loads(persona_result),
            # }
            # return result
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
