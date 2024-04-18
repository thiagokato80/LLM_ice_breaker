from dotenv import load_dotenv
#from langchain.prompts.prompt import PromptTemplate
#from langchain_openai import ChatOpenAI
#from langchain.chains import LLMChain

from langchain_ai21 import AI21LLM
from langchain_core.prompts import PromptTemplate

# Prompt Tamplate recebe inputs chamados de prompts
# Prompt é simplesmente um input de texto que damos ao LLM e ele retorna um output

# Chat moddels contem as LLMs, como interagimos com a LLM
# Helps organize our message history

# LLM chain, chains allow us to combine multiple components together 
# and create one single coherent application
# Chains allow us to combine things together

if __name__ == "__main__":
    load_dotenv()

    information = """
Elon Reeve Musk (born June 28, 1971) is a businessman and investor. He is the founder, chairman, CEO, and CTO of SpaceX; angel investor, CEO, product architect, and former chairman of Tesla, Inc.; owner, executive chairman, and CTO of X Corp.; founder of the Boring Company and xAI; co-founder of Neuralink and OpenAI; and president of the Musk Foundation. He is one of the wealthiest people in the world; as of April 2024, Forbes estimates his net worth to be $193 billion.[6]

A member of the wealthy South African Musk family, Musk was born in Pretoria and briefly attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University, but dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999. That same year, Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In October 2002, eBay acquired PayPal for $1.5 billion. Using $100 million of the money he made from the sale of PayPal, Musk founded SpaceX, a spaceflight services company, in 2002.

In 2004, Musk became an early investor in electric vehicle manufacturer Tesla Motors, Inc. (later Tesla, Inc.). He became the company's chairman and product architect, assuming the position of CEO in 2008. In 2006, Musk helped create SolarCity, a solar-energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year, Musk co-founded Neuralink—a neurotechnology company developing brain–computer interfaces—and the Boring Company, a tunnel construction company. In 2018, the U.S. Securities and Exchange Commission (SEC) sued Musk, alleging that he had falsely announced that he had secured funding for a private takeover of Tesla. To settle the case, Musk stepped down as the chairman of Tesla and paid a $20 million fine. In 2022, he acquired Twitter for $44 billion. He subsequently merged the company into newly created X Corp. and rebranded the service as X the following year. In March 2023, Musk founded xAI, an artificial intelligence company.

Musk has expressed views that have made him a polarizing. He has been criticized for making unscientific and misleading statements, including COVID-19 misinformation and antisemitic conspiracy theories.His ownership of Twitter has been similarly controversial, being marked by layoffs of large numbers of employees, an increase in hate speech and misinformation and disinformation on the website, and changes to Twitter Blue verification.
    """
    

    summary_template = """
    Given the information {information} about a person, I want you to answer:
    What is SolarCity?
    """
    #summarry_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)
    summarry_prompt_template = PromptTemplate.from_template(summary_template)
    
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # other open source LLM: Llamma.cppp, Athropic law, AI21, GCP Pump2
    llm = AI21LLM(model="j2-ultra")

    #chain = LLMChain(llm=llm, prompt=summarry_prompt_template)
    chain = summarry_prompt_template | llm
    res = chain.invoke(input={"information": information})

    print(res)
