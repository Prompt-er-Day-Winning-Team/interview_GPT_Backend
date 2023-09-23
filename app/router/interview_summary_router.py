from fastapi import APIRouter

# from app.core.helper import check_jwt
from app.repository.interview_summary_repo import InterviewSummaryRepository


interview_summary_router = APIRouter(
    prefix="/v1/users/{user_id}/summary/interviews/{interview_id}/interview_results",
    tags=["interview_summary"],
    # dependencies=[Depends(check_jwt)],
    responses={404: {"description": "Not Found!!!"}},
)


# 전체 인터뷰 결과 확인
@interview_summary_router.post(
    path="",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "interviewId": 1,
                        "totalInterviewSummary": [
                            {
                                "title": "",
                                "text": "",
                            },
                        ],
                        "totalInterviewInsight": [
                            {
                                "title": "",
                                "text": "",
                            },
                        ],
                        "totalInterviewKeyword": [
                            {"text ": "", "value": 100},
                            {"text": "", "value": 94},
                        ],
                    }
                }
            }
        }
    },
)
async def create_interview_result_statistics(user_id: int, interview_id: int):
    interview_summary_repo = InterviewSummaryRepository()
    interview_results_statistics = (
        interview_summary_repo.create_interview_result_statistics(
            user_id=user_id, interview_id=interview_id
        )
    )
    return interview_results_statistics
