import json
import random
from typing import Dict
from fastapi import HTTPException, UploadFile, File
from worker import (
    create_total_statistics_ai,
)

from app import Session
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.repository.model.interview_result import InterviewResult
from app.domain.request_domain import InterviewContentsInfo
from app.prompt.instant_question import instant_question
from app.prompt.whisper import whisper


class InterviewSummaryRepository:
    def __init__(self, session=None):
        self.session = Session()

    def create_interview_result_statistics(self, user_id: int, interview_id: int):
        try:
            interview = (
                self.session.query(Interview)
                .filter(
                    Interview.interview_id == interview_id, Interview.user_id == user_id
                )
                .first()
            )
            if not interview:
                raise HTTPException(status_code=403, detail="인터뷰 id 또는 회원 id가 틀립니다.")
            if (
                not interview.total_interview_summary
                or not interview.total_interview_insight
                or not interview.total_interview_keyword
            ):
                create_total_statistics_ai.delay(user_id, interview_id)
                interview.total_interview_summary = "Waiting"
                interview.total_interview_insight = "Waiting"
                interview.total_interview_keyword = "Waiting"
                self.session.add(interview)
                self.session.commit()

            result = {
                "interviewId": interview.interview_id,
                "totalInterviewSummary": interview.total_interview_summary
                if interview.total_interview_summary == "Waiting"
                else json.loads(interview.total_interview_summary),
                "totalInterviewInsight": interview.total_interview_insight
                if interview.total_interview_insight == "Waiting"
                else json.loads(interview.total_interview_insight),
                "totalInterviewKeyword": interview.total_interview_keyword
                if interview.total_interview_keyword == "Waiting"
                else json.loads(interview.total_interview_keyword),
            }

            return result
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
