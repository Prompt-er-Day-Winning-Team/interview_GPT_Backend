from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessage,
    HumanMessage,
)
from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks import get_openai_callback
from omegaconf import OmegaConf
import pandas as pd

from app.core.config import config


def persona(product_name, product_detail, interview_goal, target_user):
    conf = OmegaConf.load("app/prompt/config.yaml")

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    persona_sys_template = prompt.persona.system_prompt
    persona_user_template = prompt.persona.user_prompt

    persona_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        persona_sys_template
    )
    persona_human_message_prompt = HumanMessagePromptTemplate.from_template(
        persona_user_template
    )
    persona_prompt = ChatPromptTemplate.from_messages(
        [persona_sys_message_prompt, persona_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.persona.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    example = """
    {
    "기본정보" : {
        "이름": "김수진",
        "나이": "32세",
        "성별": "여성",
    },
    "성격 및 취향" : {
        "성격": "액티브한 성격, 상황에 따라 유연하게 대처 가능",
        "취미": "요가, 음악 감상, 주말에는 가족과 함께 나들이"
    },
    "직업 및 배경" : {
        "직업": "마케팅 팀장",
        "학력": "대학교 졸업 (커뮤니케이션 전공)",
        "근무지": "중견 IT 회사",
    },
    "가족 및 개인 상황" : {
        "가족 구성": "기혼, 1명의 아이를 둔 부모",
        "거주": "서울시 강남구 아파트",
    },
    "라이프스타일" : {
        "라이프스타일": "",
    },
    }
    """

    persona_prompt = persona_prompt.format_prompt(
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        example=example,
    )
    persona_prompt = persona_prompt.to_messages()

    msg = LLM(persona_prompt)
    return msg.content
