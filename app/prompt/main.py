from question import question
from interview import interview
from persona import persona
from summarize import summarize

from app.core.config import config


def main():
    product_name = "SKT에이닷"
    interview_goal = "에이닷 서비스 사용 방해요소"
    target_user = "20대 남자 대학생"

    question_res = question(product_name, interview_goal, target_user)
    persona_res = persona(product_name, interview_goal, target_user)
    interview_res = interview(product_name, target_user, persona_res, question_res)
    summarize_res = summarize()

    print(question_res)
    print(persona_res)
    print(interview_res)
    print(summarize_res)


if __name__ == "__main__":
    main()
