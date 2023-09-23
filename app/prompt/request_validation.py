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


def request_validation(product_name, product_detail, interview_goal, target_user):
    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    validation_sys_template = prompt.request_validation.system_prompt
    validation_user_template = prompt.request_validation.user_prompt

    validation_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        validation_sys_template
    )
    validation_human_message_prompt = HumanMessagePromptTemplate.from_template(
        validation_user_template
    )

    request_validation_prompt = ChatPromptTemplate.from_messages(
        [validation_sys_message_prompt, validation_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.request_validation.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    example = """
        {
        "type" : "문제있음|문제없음",
        "answer" : type에 따른 답변
        }
    """

    request_validation_tot_prompt = request_validation_prompt.format_prompt(
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        example=example,
    )
    request_validation_tot_prompt = request_validation_tot_prompt.to_messages()

    msg = LLM(request_validation_tot_prompt)
    return msg.content
