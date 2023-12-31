#### 생성된 질문지의 적절성을 확인해서 기준에 적절하지 않은 부분은 수정하는 프롬프트

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


def question_validation(status, product_name, product_detail, interview_goal, target_user, question_list):
    conf = OmegaConf.load("app/prompt/config.yaml")
    # interview_question = conf.interview_question

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    validation_sys_template = prompt.question_validation.system_prompt
    validation_user_template = prompt.question_validation.user_prompt

    validation_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        validation_sys_template
    )
    validation_human_message_prompt = HumanMessagePromptTemplate.from_template(
        validation_user_template
    )
    question_prompt = ChatPromptTemplate.from_messages(
        [validation_sys_message_prompt, validation_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.question.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    example = """
    {
    "서비스 편리성 및 기능성에 관한 질문" : [
        {
        question: "",
        answer: ""
        }
    ]
    }
    """

    question_tot_prompt = question_prompt.format_prompt(
        status=status,
        product_name=product_name,
        product_detail=product_detail,
        target_user=target_user,
        interview_goal=interview_goal,
        example=example,
        question_list = question_list
    )
    question_tot_prompt = question_tot_prompt.to_messages()

    msg = LLM(question_tot_prompt)
    return msg.content
