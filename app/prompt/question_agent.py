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
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from omegaconf import OmegaConf
import pandas as pd
import os

from app.core.config import config


def question(status, product_name, product_detail, interview_goal, target_user):
    os.environ["SERPAPI_API_KEY"] = config.SERPAPI_API_KEY

    conf = OmegaConf.load("app/prompt/config.yaml")
    # interview_question = conf.interview_question

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    question_sys_template = prompt.question.system_prompt
    question_user_template = prompt.question.user_prompt

    question_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        question_sys_template
    )
    question_human_message_prompt = HumanMessagePromptTemplate.from_template(
        question_user_template
    )
    question_prompt = ChatPromptTemplate.from_messages(
        [question_sys_message_prompt, question_human_message_prompt]
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
    )
    question_tot_prompt = question_tot_prompt.to_messages()

    tools = load_tools(['wikipedia', 'serpapi'], llm=LLM)
    agent = initialize_agent(tools, llm=LLM, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    msg = agent.run(question_tot_prompt)
    return msg