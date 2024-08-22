import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,                                     #Create react agent implements the framework based on the LLM you choose
    AgentExecutor,                                          #Agent executor takes in the prompt and feeds it to the agent/LLM
)                                                           
from langchain import hub                                   #this is a package that contains templates promtps created by the community

load_dotenv()

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the function from the tools module
from tools.tools import get_profile_url_tavily


def lookup(name: str) ->str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo"
    )
    template = """Given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page. Your answer should contain only a URL"""

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linked profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent,verbose=True)

    result = agent_executor.invoke(
        input = {"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_url = lookup(name="Frank Affatigato")
    print(linkedin_url)
    
    
    #return "https://www.linkedin.com/in/frank-affatigato-9a705a172/"