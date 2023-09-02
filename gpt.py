# import os
# from lda import TopicAnalyzer
# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain

# os.environ["OPENAI_API_KEY"] = "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"
# davinci = OpenAI(model_name='text-davinci-003')

# analyzer = TopicAnalyzer()

# user_input = input("텍스트를 입력하세요: ")

# result = analyzer.analyze_text([user_input])

# # 사용자가 입력한 질문 리스트
# questions = ['단어를 포함해 심층적인 질문을 만들어줘.',
#              '위의 단어를 포함해서 질문을 하고 싶은데 질문을 만들어줘.']

# for idx, topic in enumerate(result, 1):
#     template = f"""Question (Topic: {topic}):
#     {{question}}
    
#     Answer: """

#     prompt = PromptTemplate(template=template, input_variables=["question"])

#     llm_chain = LLMChain(
#         prompt=prompt,
#         llm=davinci
#     )

#     for question in questions:
#         # 각 질문에 대한 답변 생성
#         response = llm_chain.run(question)
#         print(f"답변: {response}\n")



import os
import openai
from lda import TopicAnalyzer
# from langchain.llms import OpenAI
# from langchain import PromptTemplate, LLMChain

os.environ["OPENAI_API_KEY"] = "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"
# davinci = OpenAI(model_name='text-davinci-003')

analyzer = TopicAnalyzer()

user_input = input("텍스트를 입력하세요: ")

result = analyzer.analyze_text([user_input])

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # 모델 출력의 무작위성을 제어합니다.
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # 모델 출력의 무작위성을 제어합니다.
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

messages =  [  
{'role':'system', 'content':'당신은 친근한 챗봇입니다.'},    
{'role':'user', 'content':'안녕, 내 이름은 Isa야'}  ]
response = get_completion_from_messages(messages, temperature=1)
print(response)
