from dotenv import load_dotenv

from langchain_ai21 import AI21LLM
from langchain_core.prompts import PromptTemplate

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.LinkedIn_Scrap2 import scrapeLinkedIn

from agents.linkedin_lookup_agent_A21 import lookup as linkedin_lookup_agent

# Prompt Tamplate recebe inputs chamados de prompts
# Prompt é simplesmente um input de texto que damos ao LLM e ele retorna um output

# Chat moddels contem as LLMs, como interagimos com a LLM
# Helps organize our message history

# LLM chain, chains allow us to combine multiple components together 
# and create one single coherent application
# Chains allow us to combine things together

def ice_breaker_with(name: str) -> str:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    Given the LinkedIn information {information} about a person, I want you to answer:
    A Short Summary
    """
    #summarry_prompt_template = PromptTemplate(input_variables=["information"], template = summary_template)
    summarry_prompt_template = PromptTemplate.from_template(summary_template)
    
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # other open source LLM: Llamma.cppp, Athropic law, AI21, GCP Pump2
    llm = AI21LLM(model="j2-ultra")

    #chain = LLMChain(llm=llm, prompt=summarry_prompt_template)
    chain = summarry_prompt_template | llm
    #linkedin_data = scrapeLinkedIn(
        #name='thiago-seiki-kato-93a12b') # este é para o Scrap2
        #linkedin_profile_url="https://www.linkedin.com/in/thiago-seiki-kato-93a12b/",
        #mock=False) #alterado para true para pegar as informações do GIST
    res = chain.invoke(input={"information": linkedin_data})

    print(res)


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_breaker_with(name='thiago seiki kato')
    