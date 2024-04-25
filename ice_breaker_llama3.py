from dotenv import load_dotenv

import langchain

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

from agents.linkedin_lookup_agent_Llama3 import lookup as linkedin_lookup_agent

#from third_parties.linkedin import scrape_linkedin_profile
# este está melhor pois pega as informações contidas em um arquivo json na máquina
from third_parties.LinkedIn_Scrap2 import scrapeLinkedIn

# Prompt Tamplate recebe inputs chamados de prompts
# Prompt é simplesmente um input de texto que damos ao LLM e ele retorna um output
# Chat models contem as LLMs, como interagimos com a LLM
# Helps organize our message history

# LLM chain, chains allow us to combine multiple components together 
# and create one single coherent application
# Chains allow us to combine things together

from langchain.chains import LLMChain
from output_parsers import summary_parser, Summary, ice_breaker_parser, topics_of_interest_parser

# USANDO LLAMA ONLINE
#import transformers
#import torch

# USANDO AI21
from langchain_ai21 import AI21LLM


def ice_breaker_with(name: str) -> Summary:
#def ice_breaker_with(name: str) -> str:
    # não estou utilizando para buscar o id do linkedin pois não tenho crédito
    #linkedin_username = linkedin_lookup_agent(name=name)
    #linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    linkedin_data = scrapeLinkedIn(name="thiago-seiki-kato-93a12b")

    summary_template = """
    Given the information about a person: \n{informacao}
    
    I want you to create:
    1) A short summary
    2) 2 interesting facts about this person
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        template = summary_template,
        input_variables = ['informacao'],
        partial_variables = {
            "format_instructions": summary_parser.get_format_instructions()
            }
        )
    #summary_prompt_template = PromptTemplate.from_template(summary_template)
    
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # other open source LLM: Llamma.cppp, Athropic law, AI21, GCP Pump2
    llm = AI21LLM(model="j2-ultra", temperature=0, max_tokens=1000)

    #llm = Ollama(temperature=0, model="llama2")
    #llm = Ollama(temperature=0, model="llama3")
    
    # USANDO LLAMA ONLINE - falta o HF_TOKEN, aguardar e-mail
    """llm = transformers.pipeline(
        "text-generation",
         model="meta-llama/Meta-Llama-3-8B",
         model_kwargs={"torch_dtype": torch.bfloat16},
         device="cuda",
         )"""

    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    #chain = LLMChain(llm=llm, prompt=summary_prompt_template, output_parser=summary_parser, return_final_only=True)
    chain = summary_prompt_template | llm | summary_parser
    #linkedin_data = scrapeLinkedIn(
        #name='thiago-seiki-kato-93a12b') # este é para o Scrap2
        #linkedin_profile_url="https://www.linkedin.com/in/thiago-seiki-kato-93a12b/",
        #mock=False) #alterado para true para pegar as informações do GIST
    
    summary_and_facts: Summary = chain.invoke(input={"informacao":linkedin_data},)
    #summary_and_facts = chain.invoke(input={"informacao":linkedin_data},)

    #print(summary_and_facts, linkedin_data.get("profile_pic_url"))
    return summary_and_facts, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_breaker_with(name='thiago seiki kato')
    