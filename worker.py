import os, json
from celery import Celery
from fastapi import HTTPException
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.repository.model.interview_result import InterviewResult
from app.prompt.persona import persona
from app.prompt.question import question
from app.prompt.virtual_interview import virtual_interview
from app.prompt.summarize import summarize
from app.prompt.total_statistics import total_statistics

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

app = Celery("tasks", backend=redis_url, broker=redis_url)


from app import Session

session = Session()


@app.task
def create_persona_ai(user_id, interview_id):
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
    interview = session.query(Interview).get(interview_id)
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
    session.add(interview)
    session.commit()

    return "Create persona success!"


@app.task
def create_question_list_ai(user_id, interview_id):
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
    interview = session.query(Interview).get(interview_id)
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
    session.add(interview)
    session.commit()

    return "Create question list success!"


@app.task
def create_virtual_interview_ai(user_id, interview_id):
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
    interview = session.query(Interview).get(interview_id)
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
    session.add(interview)
    session.commit()

    return "Create virtual interview success!"


@app.task
def create_summary_ai(user_id, interview_id, interview_result_id):
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=403, detail="회원 id가 틀립니다.")
    interview = session.query(Interview).get(interview_id)
    if not interview:
        raise HTTPException(status_code=403, detail="인터뷰 id가 틀립니다.")
    interview_result = session.query(InterviewResult).get(interview_result_id)
    if not interview_result:
        raise HTTPException(status_code=403, detail="인터뷰 결과 id가 틀립니다.")

    # 단일 인터뷰 요약 생성
    summary_result = summarize(
        product_name=interview.product_name,
        product_detail=interview.product_detail,
        interview_goal=interview.interview_goal,
        target_user=interview.target_user,
        interview_contents=interview_result.interview_contents,
    )

    interview_result.interview_summary = summary_result
    session.add(interview_result)
    session.commit()

    return "Create summary success!"


@app.task
def create_total_statistics_ai(user_id, interview_id):
    interview = (
        session.query(Interview)
        .filter(Interview.interview_id == interview_id, Interview.user_id == user_id)
        .first()
    )
    if not interview:
        raise HTTPException(status_code=403, detail="인터뷰 id 또는 회원 id가 틀립니다.")
    interview_results = (
        session.query(InterviewResult)
        .filter(InterviewResult.interview_id == interview_id)
        .all()
    )

    interview_summaries = []

    for interview_result in interview_results:
        if (
            interview_result.interview_summary
            and interview_result.interview_summary != "Waiting"
        ):
            interview_summaries += json.loads(interview_result.interview_summary)

    # 전체 인터뷰 통계 생성
    total_statistics_result = total_statistics(
        product_name=interview.product_name,
        product_detail=interview.product_detail,
        interview_goal=interview.interview_goal,
        target_user=interview.target_user,
        interview_summaries=interview_summaries,
    )

    total_statistics_result = json.loads(total_statistics_result)

    interview.total_interview_summary = json.dumps(
        total_statistics_result["total_interview_summary"]
    )
    interview.total_interview_insight = json.dumps(
        total_statistics_result["total_interview_insight"]
    )
    interview.total_interview_keyword = json.dumps(
        total_statistics_result["total_interview_keyword"]
    )
    session.add(interview_result)
    session.commit()

    return "Create total statistics success!"
