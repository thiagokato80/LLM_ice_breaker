from dotenv import load_dotenv
from LinkedIn_Scrap2 import scrapeLinkedIn
 
load_dotenv()
 
data = scrapeLinkedIn(name='thiago-seiki-kato-93a12b')
print(data)
#data._content