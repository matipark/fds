#%%

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# auth
import os
from dotenv import load_dotenv
load_dotenv()

authorization = (os.getenv('username_universal'),os.getenv('pass_home')) ##pass_office

#%%

###
create_universe_endpoint = 'https://api.factset.com/content/factset-concordance/v2/universe'


create_universe_request ={
  "universeName": "Matias_2",
  "universeDescription": "Aus Super"
}

headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# CREATE THE POST

#create a post request and print the Status Code

create_universe_post = json.dumps(create_universe_request)
create_universe_response = requests.post(url = create_universe_endpoint, data=create_universe_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(create_universe_response.status_code))
create_universe_response.text

#%%

check_universe_endpoint = 'https://api.factset.com/content/factset-concordance/v2/universes?universeId=853'


entity_task_status_response = requests.get(url=check_universe_endpoint,auth=authorization)
print('HTTP Status: {}'.format(entity_task_status_response.status_code))
entity_task_status_response.text


#%%

entity_task_endpoint = 'https://api.factset.com/content/factset-concordance/v2/entity-task'

entity_task_request = {
    "universeId": 853,
    "taskName": "test",
    # "inputFile": "Sample_Concordance.csv",
    # "clientIdColumn": "Identifier",
    # "nameColumn": "Name",
    # "countryColumn": "country",
    # "stateColumn": "state",
    # "urlColumn": "url"
    #"uniqueMatch": True,
    #"excludeEntityType": [ "PVT" ]
}
headers = {'Accept': 'application/json;charset=utf-8','Content-Type': 'multipart/form-data'}

#{'Accept': 'application/json;charset=utf-8','Content-Type': 'multipart/form-data'}
#multipart/form-data
#application/json;charset=utf-8

#%%


entity_task_post = json.dumps(entity_task_request)
#Reading the input file and create a POST request
entity_task_response = requests.post(url=entity_task_endpoint,data=entity_task_post,auth = authorization,headers=headers)
print('HTTP Status: {}'.format(entity_task_response.status_code))


#%%

entity_task_data = json.loads(entity_task_response.text)
entity_task_df = json_normalize(entity_task_data['data'])


entity_task_response.html

# %%
