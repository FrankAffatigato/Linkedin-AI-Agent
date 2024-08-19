import os
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    print("Hello LangChain!")

    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
        """
    
    summary_prompt_template = PromptTemplate(
        inputvariables="information", template=summary_template
        )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    linked_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/frank-affatigato-9a705a172/")
    
    #llm = ChatOllama(model="mistral")
    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linked_data})


    print(res)