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

from app.core.config import config


def instant_question(
    status, product_name, product_detail, interview_goal, target_user, chat_history
):
    conf = OmegaConf.load("app/prompt/config.yaml")
    scenario = conf.scenario

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    instant_question_sys_template = prompt.instant_question.system_prompt
    instant_question_user_template = prompt.instant_question.user_prompt

    instant_question_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        instant_question_sys_template
    )
    instant_question_human_message_prompt = HumanMessagePromptTemplate.from_template(
        instant_question_user_template
    )
    instant_question_messages = ChatPromptTemplate.from_messages(
        [instant_question_sys_message_prompt, instant_question_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.instant_question.temperature,
        model="gpt-4"
        # max_tokens=prompt.instant_question.max_tokens,
        # model_kwargs={'top_p':conf.instant_question.top_p}
    )

    instant_question_prompt = instant_question_messages.format_prompt(
        status=status,
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        chat_history=chat_history,
    )
    instant_question_prompt = instant_question_prompt.to_messages()

    msg = LLM(instant_question_prompt)
    return msg.content
