import os
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain

os.environ["OPENAI_API_KEY"] = ""
davinci = OpenAI(model_name = 'text-davinci-003')

template = """Question: {question}

Answer:  """

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(
    prompt=prompt,
    llm=davinci
)

question = [] / "" / ()
print(llm_chain.run(question))