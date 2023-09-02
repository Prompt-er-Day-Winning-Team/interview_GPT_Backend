import os
from lda import TopicAnalyzer
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

os.environ["OPENAI_API_KEY"] = "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"
davinci = OpenAI(model_name='text-davinci-003')

analyzer = TopicAnalyzer()

conversation_history = []

interview_purpose = "본 인터뷰는 SKTelecom의 에이닷 통화요약 기능에 대한 사용자 경험을 파악하기 위한 것입니다."

while True:
    user_input = input("텍스트를 입력하세요 (나가려면 '나가기'를 입력하세요): ")

    if user_input == '나가기':
        break
    
    conversation_history.append(f'사용자: {user_input}')
    result = analyzer.analyze_text(conversation_history)
    questions = ['단어를 포함해 인터뷰 형식의 정형적인 질문을 1개만 만들어줘.']
    for idx, topic in enumerate(result, 1):
        template = f"""질문 (토픽: {topic}):
                    {interview_purpose}
                    {conversation_history[-1]}  # 이전 대화 내용을 여기에 추가
                    {{question}}

                    답변: """

        prompt = PromptTemplate(template=template, input_variables=["question"])

        llm_chain = LLMChain(
            prompt=prompt,
            llm=davinci
        )

        for question in questions:
            response = llm_chain.run(question)
            print(f"답변: {response}\n")

            conversation_history.append(f'AI: {response}')
