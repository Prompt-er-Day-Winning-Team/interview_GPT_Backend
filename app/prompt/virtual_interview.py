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


def virtual_interview(
    product_name, product_detail, interview_goal, target_user, persona, question_list
):
    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    virtual_interview_sys_template = prompt.virtual_interview.system_prompt
    virtual_interview_user_template = prompt.virtual_interview.user_prompt

    sys_message_prompt = SystemMessagePromptTemplate.from_template(
        virtual_interview_sys_template
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        virtual_interview_user_template
    )
    virtual_interview_prompt = ChatPromptTemplate.from_messages(
        [sys_message_prompt, human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.virtual_interview.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    example = """
    {
        "서비스 사용 배경 및 환경에 관한 질문" : [
            "진행자 : 질문1",
            "참가자 : 답변1",
            "진행자 : 질문2",
            "참가자 : 답변2",
        ]
    }
    """

    virtual_interview_prompt = virtual_interview_prompt.format_prompt(
        product_name=product_name,
        product_detail=product_detail,
        interview_goal=interview_goal,
        target_user=target_user,
        question_list=question_list,
        persona=persona,
        example=example,
    )
    virtual_interview_prompt = virtual_interview_prompt.to_messages()

    msg = LLM(virtual_interview_prompt)
    return msg.content
