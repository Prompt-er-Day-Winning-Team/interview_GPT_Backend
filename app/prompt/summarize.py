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


def summarize():
    conf = OmegaConf.load("app/prompt/config.yaml")
    interview = conf.interview

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    summarize_sys_template = prompt.summarize.system_prompt
    summarize_user_template = prompt.summarize.user_prompt

    sum_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        summarize_sys_template
    )
    sum_human_message_prompt = HumanMessagePromptTemplate.from_template(
        summarize_user_template
    )
    sum_messages = ChatPromptTemplate.from_messages(
        [sum_sys_message_prompt, sum_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.summarize.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    sum_prompt = sum_messages.format_prompt(interview=interview)
    sum_prompt = sum_prompt.to_messages()

    msg = LLM(sum_prompt)
    return msg.content