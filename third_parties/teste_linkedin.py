import os, os.path, json, requests


# nome está definido para o eden-marco, para o meu deveria ser "thiago-seiki-kato-93a12b"
# https://www.linkedin.com/in/thiago-seiki-kato-93a12b/

name='sabrina-frizzo-272b0012'    
# avalia se o arquivo json já está gravado, se sim, retorna os dados do arquivo
fname = f"{name}.json"
if os.path.isfile(fname):
    with open(fname, 'r') as fh:
        str = fh.read()
        json.loads(str)

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