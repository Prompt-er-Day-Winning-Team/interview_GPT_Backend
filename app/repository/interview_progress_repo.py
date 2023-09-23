import json
import random
from typing import Dict
from fastapi import HTTPException, UploadFile, File
from worker import (
    create_summary_ai,
)

from app import Session
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.repository.model.interview_result import InterviewResult
from app.domain.request_domain import InterviewContentsInfo
from app.prompt.instant_question import instant_question
from app.prompt.whisper import whisper


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
        self,
        user_id: int,
        interview_id: int,
        interview_result_id: int,
        answer_audio_file: bytes = File(None),
    ):
        try:
            user = self.session.query(User).get(user_id)
            if not user:
                raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
            interview = (
                self.session.query(Interview)
                .filter(
                    Interview.interview_id == interview_id, Interview.user_id == user_id
                )
                .first()
            )
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id 또는 회원 id가 틀립니다.")
            interview_result = (
                self.session.query(InterviewResult)
                .filter(
                    InterviewResult.interview_result_id == interview_result_id,
                    InterviewResult.interview_id == interview_id,
                )
                .first()
            )
            if not interview_result:
                raise HTTPException(
                    status_code=403, detail="인터뷰 결과 id 또는 인터뷰 id가 틀립니다."
                )
            if interview_result.interview_contents:
                interview_contents = json.loads(interview_result.interview_contents)
            else:
                interview_contents = {}

            question_list = json.loads(interview.question_list)
            only_question_list = []
            for category in question_list:
                for question_set in question_list[category]:
                    only_question_list.append(question_set["question"])

            # 음성 인식
            if answer_audio_file:
                interview_contents[-1]["answer"] = whisper(answer_audio_file)

            # 첫 번째 질문인 경우
            if not interview_result.interview_contents or not interview_contents:
                interview_contents = [
                    {
                        "question": only_question_list[0],
                        "answer": "",
                    }
                ]
                interview_result.interview_contents = json.dumps(
                    interview_contents, ensure_ascii=False
                )
                self.session.add(interview_result)
                self.session.commit()
                return {
                    "isFinished": False,
                    "interviewQuestion": interview_contents[-1]["question"],
                }

            # 꼬리질문을 해야 하는 경우
            if interview_contents[-1]["question"] in only_question_list:
                is_follow_on = random.choice([True, False])
                # print(is_follow_on)
                if is_follow_on:
                    # 인터뷰 질문 생성
                    instant_question_result = instant_question(
                        product_name=interview.product_name,
                        product_detail=interview.product_detail,
                        interview_goal=interview.interview_goal,
                        target_user=interview.target_user,
                        chat_history=interview_contents,
                    )
                    interview_contents.append(
                        {
                            "question": instant_question_result,
                            "answer": "",
                        }
                    )
                    interview_result.interview_contents = json.dumps(
                        interview_contents, ensure_ascii=False
                    )
                    self.session.add(interview_result)
                    self.session.commit()
                    return {
                        "isFinished": False,
                        "interviewQuestion": interview_contents[-1]["question"],
                    }

            # 질문리스트의 다음 질문을 해야 하는 경우
            search_idx = -1
            while True:
                if interview_contents[search_idx]["question"] in only_question_list:
                    last_origin_question_idx = only_question_list.index(
                        interview_contents[search_idx]["question"]
                    )
                    break
                search_idx -= 1

            # 더 이상 질문이 없는 경우
            if last_origin_question_idx == len(only_question_list) - 1:
                interview_result.interview_contents = json.dumps(
                    interview_contents, ensure_ascii=False
                )
                interview_result.interview_url = "Done"
                create_summary_ai.delay(user_id, interview_id, interview_result_id)
                interview_result.interview_summary = "Waiting"
                self.session.add(interview_result)
                self.session.commit()
                return {
                    "isFinished": True,
                    "interviewQuestion": interview_contents[-1]["question"],
                }

            interview_contents.append(
                {
                    "question": only_question_list[last_origin_question_idx + 1],
                    "answer": "",
                }
            )
            interview_result.interview_contents = json.dumps(
                interview_contents, ensure_ascii=False
            )
            self.session.add(interview_result)
            self.session.commit()
            return {
                "isFinished": False,
                "interviewQuestion": interview_contents[-1]["question"],
            }
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def read_interview_result(
        self, user_id: int, interview_id: int, interview_result_id: int
    ):
        try:
            interview_result = (
                self.session.query(InterviewResult)
                .filter(
                    InterviewResult.interview_result_id == interview_result_id,
                    InterviewResult.interview_id == interview_id,
                )
                .first()
            )
            if not interview_result:
                raise HTTPException(
                    status_code=403, detail="인터뷰 결과 id 또는 인터뷰 id가 틀립니다."
                )
            if interview_result.interview_url != "Done":
                raise HTTPException(status_code=403, detail="아직 완료되지 않은 인터뷰 결과입니다.")

            result = {
                "interviewResultId": interview_result.interview_result_id,
                "interviewSummary": interview_result.interview_summary
                if interview_result.interview_summary == "Waiting"
                else json.loads(interview_result.interview_summary),
                "interviewContents": json.loads(interview_result.interview_contents),
            }

            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
