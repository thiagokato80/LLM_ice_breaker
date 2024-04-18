import os

# LangChian hub is simply a way to download pre-made prompts
# by the community and from the LangChain team that we'll be using in this course.
from langchain import hub

# React Agents: Create_react_agent is a built-in function in LangChain,
# which is going to be receiving a LLM that we'll be using to power our agent.
# It's going to receive tools and it's going to receive a prompt,
# a React prompt it's called. And this function is going to return us an agent,
# which is based on the React algorithm, which is using the LLM we provided and has the tools
# we provided it as well.
# The agent executor is the runtime of the agent. So this is actually the object which is going
# to receive our prompts and our instructions what to do, and hopefully to finish our tasks.
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)

# Tools are interfaces that help our LangChain agents, chains, or LLMs use and 
# interact with the external world. So for example, to search online or 
# to search in a database, and you can think about a tool as an object
# that has the following information. It has a function to execute, 
# a Python function, a callable. So for example, it may be a function
# that we'll be using to search online and it has a description which describes
# what does this function do and what is the output, which is actually 
# super important when we write the tools, because the LLM is going to be using that description.
from langchain_core.tools import Tool

#from langchain_openai import ChatOpenAI
from langchain_ai21 import AI21LLM
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv

# importar a tool que fizemos em Tavly
from tools.tools import get_profile_url_tavily

load_dotenv()

#
def lookup(name: str) -> str:
    llm = AI21LLM(model="j2-ultra")
    #llm = ChatOpenAI(
        #temperature=0,
        #model_name="gpt-3.5-turbo",
        #openai_api_key=os.environ["OPENAI_API_KEY"],
    #)

    # Provide the template thsy we're going to supply our ptompt template
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page. Your answer should contain only a URL"""

    # Initialize the prompt template from the template wrote above.
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"])

    # provide all the tools that the agent will be using
    # in this example only one tool
    tools_for_agent = [
        Tool(
            # name argument, name that out agent is going to refer to this tool
            # and is going to be supplied to the reasoning engine
            # and is going to be displayed in the logs
            name="Crawl Google 4 linkedin profile page",
            # Python function that this tool will run
            func=get_profile_url_tavily,
            # description is super important, because that's how the LLM is going to
            # determine whether to use this tool or not.
            # we want the description to be as concise and to have as much information
            # so it won't be ambiguous, and the LLM would always know which tool to use.
            # So if our agent decides that it's time to invoke this tool according to
            # it's reasoning engine, then it'll simply run this function. the search function
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    # Harrison Chase 17 is the username of Harrison Chase in the prompt tab.
    # And Harrison Chase is the co-founder and creator of LangChain.
    # And /react here is a prompt that Harrison Chase world, which is a super 
    # popular prompt used for ReAct prompting and it's actually going to be the 
    # reasoning engine of our agent. And /react here is a prompt that Harrison Chase wrote,
    # which is a super popular prompt used for ReAct prompting and it's actually 
    # going to be the reasoning engine of our agent. And you can see that the 
    # ReAct prompt is a prompt that is sent to the LLM. It will include our tool 
    # names and our tool descriptions and what we want our agent to do. And luckily for us,
    # LangChain is going to be plugging in those values for us after we initialize the agent.
    # So this is the beauty of it, a lot of boilerplate code and a lot of heavy lifting 
    # that we don't really need to do because it's already implemented by the 
    # LangChain framework. And this prompt over here is implementing the ReAct paper,
    # that's why it's called the ReAct Prompt reasoning enacting, and you can check it 
    # in the theory section and it's also using something which is called the chain of thought.
    # So this is also another famous prompting technique.
    react_prompt = hub.pull("hwchase17/react")

    # The function create_react_agent, which is going to accept our ReAct prompt that we just saw.
    # It's going to accept our tools and it's going to accept our LLM.
    # So we have here our agent which basically holds all the way we want to communicate 
    # with the LLM and which tools that we have, and then how to parse the output that we 
    # get from the LLM.
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)

    # Provide it also the runtime, how to run in loops. And this is going to be our final agent.
    # So we will create an AgentExecutor.  It's going to receive that agent. 
    # It's going to receive a list of tools because those are actually the tools 
    # that will be invoked. And supply verbose equals true, so we'll see extensive log-in
    # to understand a bit more how this agent is working. So this AgentExecutor is the final 
    # thing that we're going to be running. This is the runtime of our agent. 
    # So I know this is pretty confusing,why do we need to create a ReAct agent 
    # and then create from it an AgentExecutor. But you can think about it as 
    # the create agent is going to be the recipe, what we're sending to the LLM 
    # and getting back to it and parsing it. But the AgentExecutor is going to be responsible
    # for orchestrating all of these and in to be actually invoking those Python functions.
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)


    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url
