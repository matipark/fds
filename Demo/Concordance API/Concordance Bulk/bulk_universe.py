#%%

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas import json_normalize

# auth
import os
from dotenv import load_dotenv
load_dotenv()

authorization = (os.getenv('username_universal'),os.getenv('pass_home_kr')) ##pass_office/pass_home

#%%

### No need to run this if you already have a universe ID ###

### CREATE universe

create_universe_endpoint = 'https://api.factset.com/content/factset-concordance/v2/universe'

create_universe_request ={
  "universeName": "Matias_5",
  "universeDescription": "Demyst "
}

headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# Create a post request and print the Status Code

create_universe_post = json.dumps(create_universe_request)
create_universe_response = requests.post(url = create_universe_endpoint, data=create_universe_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(create_universe_response.status_code))
create_universe_response.text

#%%

### CHECK universe

# input your universeId
universeId = 965

check_universe_endpoint = 'https://api.factset.com/content/factset-concordance/v2/universes?universeId={}'.format(universeId)

entity_task_status_response = requests.get(url=check_universe_endpoint,auth=authorization)
print('HTTP Status: {}'.format(entity_task_status_response.status_code))
entity_task_status_response.text


#%%

### Building a concordance request

entity_task_endpoint = 'https://api.factset.com/content/factset-concordance/v2/entity-task'
entity_task_file='Concordance_1.csv' 
entity_task_request = {
    "universeId": universeId,
    "taskName": "testing concordance",
    "clientIdColumn": "Identifier",
    "nameColumn": "Name",
    # "countryColumn": "country",
    # "stateColumn": "state",
    # "urlColumn": "url"
    #"uniqueMatch": True,
    #"excludeEntityType": [ "PVT" ]
}
headers = {'Accept': 'application/json;charset=utf-8'}



#%%

### Making a concordance request

file_data = { "inputFile": (entity_task_file, open(entity_task_file, 'rb'), 'text/csv') }
entity_task_response = requests.post(url=entity_task_endpoint,data=entity_task_request,files=file_data,auth = authorization,headers=headers)
print('HTTP Status: {}'.format(entity_task_response.status_code))
entity_task_data = json.loads(entity_task_response.text)
entity_task_df = json_normalize(entity_task_data['data'])

print('COLUMNS:')
print('')
print(entity_task_df.dtypes)
print('')
print('RECORDS:',len(entity_task_df))

# %%

entity_task_df

#%%

# Get the task ID
eid=entity_task_df['taskId'][0]
type(eid)
eid

# %%

### Check Status

entity_task_status_endpoint = 'https://api.factset.com/content/factset-concordance/v2/entity-task-status'
entity_task_status_parameters={
  "taskId":str(eid),
  "offset": 0,
  "limit": 10,
  #"status": ""
}


entity_task_status_url = entity_task_status_endpoint + "?"
for p,v in entity_task_status_parameters.items():
    if isinstance(v,list):
        entity_task_status_url += p + '=' + ','.join(v) + '&'
    else:
        entity_task_status_url += p + '=' + str(v) + '&'
print(entity_task_status_url)
entity_task_status_response = requests.get(url =entity_task_status_url,auth=authorization, headers=headers, verify=False)

# %%


entity_task_status_data = json.loads(entity_task_status_response.text)
entity_task_status_df = json_normalize(entity_task_status_data['data'])
print('COLUMNS:')
print('')
print(entity_task_status_df.dtypes)
print('')
print('RECORDS:',len(entity_task_status_df))

#%%

entity_task_status_df


#%%

### Pull results

entity_decisions_endpoint = 'https://api.factset.com/content/factset-concordance/v2/entity-decisions'
entity_decisions_parameters={
  "taskId":str(eid),
  "offset": 0,
  "limit": 10000,
  #"mapStatus": ""
}


#%%

entity_decisions_url = entity_decisions_endpoint + "?"
for p,v in entity_decisions_parameters.items():
    if isinstance(v,list):
        entity_decisions_url += p + '=' + ','.join(v) + '&'
    else:
        entity_decisions_url += p + '=' + str(v) + '&'
print(entity_decisions_url)
entity_decisions_response=requests.get(url = entity_decisions_url, auth=authorization, headers=headers, verify=False)

#%%


entity_decisions_data = json.loads(entity_decisions_response.text)
entity_decisions_df = json_normalize(entity_decisions_data['data'])
print('COLUMNS:')
print('')
print(entity_decisions_df.dtypes)
print('')
print('RECORDS:',len(entity_decisions_df))

#%%

### Display the Records
entity_decisions_df

#%%

### Save as Excel

entity_decisions_df.to_excel("output.xlsx", engine='xlsxwriter')






# %%


### Pull previousy run/saved universe

entity_universe_endpoint = 'https://api.factset.com/content/factset-concordance/v2/entity-universe'
entity_universe_request ={
  "universeId": 853,
  #"clientId": "Test_201",
  "offset": 0,
  "limit": 10000
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}


#%%

#create a post request
#manage_mappings_post = json.dumps(manage_mappings_request)
entity_universe_response = requests.get(url = entity_universe_endpoint, params =entity_universe_request, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(entity_universe_response.status_code))


# %%
#create a dataframe from POST request, show dataframe properties
entity_universe_data = entity_universe_response.json()
entity_universe_df = json_normalize(entity_universe_data['data'])
print('COLUMNS:')
print('')
print(entity_universe_df.dtypes)
print('')
print('RECORDS:',len(entity_universe_df))
# %%

#display the universe object
entity_universe_df


#%% 

entity_universe_df.to_excel("output_universe.xlsx", engine='xlsxwriter')

# %%
