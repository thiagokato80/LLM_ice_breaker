# Exemplo de pegar os dados somente 1x, ele salva os dados já procurados 1x na pasta
# Caso procure novamente, e o arquivo já está no diretório, ele apenas pega as informações,
# não busca novamente, nem entra no site do GIST pois os dados estarão no diretório

import os, os.path, json, requests


# nome está definido para o eden-marco, para o meu deveria ser "thiago-seiki-kato-93a12b"
# https://www.linkedin.com/in/thiago-seiki-kato-93a12b/
def scrapeLinkedIn(name):
    
    # avalia se o arquivo json já está gravado, se sim, retorna os dados do arquivo
	diretorio = 'G:/Meu Drive/Estudo/Cursos/LangChain/ice_breaker/third_parties/'
	fname = f"{diretorio}{name}.json"
	
	if os.path.isfile(fname):
		with open(fname, 'r') as fh:
			str = fh.read()
			data = json.loads(str)
			#return json.loads(str)
	else:
		proxyCurlUrl = 'https://nubela.co/proxycurl/api/v2/linkedin'
		linkedInUrl = f"https://www.linkedin.com/in/{name}/"
		hHeaders = {
			'Authorization': f"Bearer {os.environ['PROXYCURL_API_KEY']}"
			}
		hParams = {
			'url': linkedInUrl,  # will work with just this
	
			'fallback_to_cache': 'on-error',
			'use_cache': 'if-present',
			'skills': 'include',
			'inferred_salary': 'include',
			'personal_email': 'include',
			'personal_contact_number': 'include',
			'twitter_profile_id': 'include',
			'facebook_profile_id': 'include',
			'github_profile_id': 'include',
			'extra': 'include',
			}
		# --- resp has these fields:
		#        status_code - should be 200, otherwise an error occurred
		#        headers - a hash of header name/header value
		#        encoding - should be 'utf-8'
		#        text - the text of the response, should be a JSON string
		#        json() - interprets text as JSON, returns a data structure
		resp = requests.get(proxyCurlUrl,
				params=hParams,
				headers=hHeaders)
		assert resp.status_code == 200, "Bad status"
		with open(fname, 'w') as fh:
			#json.dump(resp, fh) #ajustei com um teste que fiz
			fh.write(resp.text)
		data = resp.json()

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
        scrapeLinkedIn(
            name="thiago-seiki-kato-93a12b", 
        )
    )