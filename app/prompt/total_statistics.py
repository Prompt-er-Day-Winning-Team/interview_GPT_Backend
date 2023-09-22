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


def total_statistics(
    product_name, product_detail, interview_goal, target_user, interview_summaries
):
    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    total_statistics_sys_template = prompt.total_statistics.system_prompt
    total_statistics_user_template = prompt.total_statistics.user_prompt

    stat_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        total_statistics_sys_template
    )
    stat_human_message_prompt = HumanMessagePromptTemplate.from_template(
        total_statistics_user_template
    )
    stat_messages = ChatPromptTemplate.from_messages(
        [stat_sys_message_prompt, stat_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.total_statistics.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    example = """
    {
        total_interview_summary: [
            {
                title: "",
                text: "",
            },
        ],
        total_interview_insight: [
            {
                title: "",
                text: "",
            },
        ],
        total_interview_keyword: [
            { text: "", value: 100 },
            { text: "", value: 94 },
        ]
    }
    """

    stat_prompt = stat_messages.format_prompt(
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        interview_summaries=interview_summaries,
        example=example,
    )
    stat_prompt = stat_prompt.to_messages()

    msg = LLM(stat_prompt)
    return msg.content
