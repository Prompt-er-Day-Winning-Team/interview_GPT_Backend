import os
from celery import Celery
from fastapi import HTTPException
from app.repository.model.user import User
from app.repository.model.interview import Interview
from app.prompt.persona import persona
from app.prompt.question import question
from app.prompt.virtual_interview import virtual_interview

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
