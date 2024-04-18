import os
from getpass import getpass
from dotenv import load_dotenv

#os.environ["AI21_API_KEY"] = getpass()


from langchain_ai21 import AI21LLM
from langchain_core.prompts import PromptTemplate

load_dotenv()

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)

model = AI21LLM(model="j2-ultra")

chain = prompt | model

print(chain.invoke({"question": "who is Elon Musk?"}))