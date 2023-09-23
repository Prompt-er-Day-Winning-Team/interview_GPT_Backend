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


def persona(status, product_name, product_detail, interview_goal, target_user):
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
        "이름": "",
        "나이": "",
        "성별": "",
    },
    "성격 및 취향" : {
        "성격": "",
        "취미": ""
    },
    "직업 및 배경" : {
        "직업": "",
        "학력": "",
        "근무지": "",
    },
    "가족 및 개인 상황" : {
        "가족 구성": "",
        "거주": "",
    },
    "라이프스타일" : {
        "라이프스타일": "",
    },
    }
    """

    persona_prompt = persona_prompt.format_prompt(
        status=status,
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        example=example,
    )
    persona_prompt = persona_prompt.to_messages()

    msg = LLM(persona_prompt)
    return msg.content
