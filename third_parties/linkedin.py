import os
import requests
from dotenv import load_dotenv

load_dotenv()

# The function will take de LinkedIn profile URL, use a third-party API called Poxyculr,
# which is going to help scrape LinkedIn information with just making an HTTP call
# the mock equals false cause we want to put for mocking and for local development
# no site GIST abaixo há uma cópia do perfil do instrutor para avaliarmos
# para o curso vamos usar o site https://nubela.co/proxycurl/linkedin
# ele trará um perfil do linkedin em formato JSON. É pago mas podemos usar uma conta grátis
# por um tempo
def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock: # mock deve ser True
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else: # mock deve ser False
        #print("ERRO")
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/thiago-seiki-kato-93a12b/", 
            mock=False #alterado para true para pegar as informações do GIST
        )
    )
