import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
#from langchain_ollama import ChatOllama
#from langchain.chains import LLMChain
#from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary
from typing import Tuple

def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = "https://www.linkedin.com/in/frank-affatigato-9a705a172/" #linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

    summary_template = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them

    \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
    input_variables=["information"], 
    template=summary_template,
    partial_variables={"format_instructions": summary_parser.get_format_instructions()
                       },
            )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    #linked_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/frank-affatigato-9a705a172/")
    
    #llm = ChatOllama(model="mistral")
    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    chain = summary_prompt_template | llm | summary_parser


    res:Summary = chain.invoke(input={"information": linkedin_data})
    print(res)
    print(linkedin_data.get("profile_pic_url"))
    return res, linkedin_data.get("profile_pic_url")




if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="Frank Affatigato ALDI US")
