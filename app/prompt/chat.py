import gradio as gr
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


def respond(user_msg, chat_hist):
    conf = OmegaConf.load("app/prompt/config.yaml")
    scenario = conf.scenario

    prompt_path = "app/prompt/prompt.yaml"
    prompt = OmegaConf.load(prompt_path)
    chat_sys_template = prompt.chat.system_prompt
    chat_user_template = prompt.chat.user_prompt

    chat_sys_message_prompt = SystemMessagePromptTemplate.from_template(
        chat_sys_template
    )
    chat_human_message_prompt = HumanMessagePromptTemplate.from_template(
        chat_user_template
    )
    chat_messages = ChatPromptTemplate.from_messages(
        [chat_sys_message_prompt, chat_human_message_prompt]
    )

    LLM = ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        temperature=prompt.chat.temperature,
        model="gpt-4"
        # max_tokens=prompt.chat.max_tokens,
        # model_kwargs={'top_p':conf.chat.top_p}
    )

    chat_history = ""
    if chat_hist is not None:
        for chat in reversed(chat_hist):
            chat_history += f"Customer: {chat[0]}, "
            chat_history += f"Interviewer: {chat[1]}, "

    chat_prompt = chat_messages.format_prompt(
        scenario=scenario, chat_history=chat_history, user_answer=user_msg
    )
    chat_prompt = chat_prompt.to_messages()
    chat_promp_str = chat_prompt.to_string()

    question = LLM(chat_prompt).content
    chat_hist += [(user_msg, question)]

    return question, "", chat_hist, chat_promp_str


def main():
    with gr.Blocks() as demo:
        chat_history = gr.State([])

        with gr.Tab("하루챗 서비스"):
            with gr.Row():
                with gr.Column():
                    chatbot = gr.Chatbot(height=600)
                    user_msg = gr.Textbox(label="채팅창", placeholder="답변해주세요")
            with gr.Column(scale=2):
                with gr.Accordion("프롬프트를 위한 정보"):
                    with gr.Row():
                        chat_prompt = gr.Textbox(label="프롬프트")
                    with gr.Row():
                        question = gr.Textbox(label="질문")

        user_msg.submit(
            respond,
            [user_msg, chat_history],
            [question, user_msg, chatbot, chat_prompt],
        )

        demo.queue()
        demo.launch()


if __name__ == "__main__":
    main()
