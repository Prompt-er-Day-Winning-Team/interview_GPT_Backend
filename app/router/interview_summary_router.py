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
async def create_interview_result_statistics(user_id: int, interview_id: int):
    interview_summary_repo = InterviewSummaryRepository()
    interview_results_statistics = (
        interview_summary_repo.create_interview_result_statistics(
            user_id=user_id, interview_id=interview_id
        )
    )
    return interview_results_statistics
