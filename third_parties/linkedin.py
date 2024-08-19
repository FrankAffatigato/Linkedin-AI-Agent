import os
import requests
from dotenv import load_dotenv
load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock:bool=True):

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/FrankAffatigato/492c49343f06906f5f5ada0a9a401804/raw"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
            )
        
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROCYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params = {"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10)

   
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in([], "", "", None)
        and k not in ["people_also_viewed"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data





if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/frank-affatigato-9a705a172/",
            )
    )