#%%

# Formula API Sample Python Code Snippet

# This snippet demonstrates basic features of the FactSet Formula API by walking through the following steps:
#        1. Import Python packages
#        2. Enter your Username and API Key for authorization
#        3. For each endpoint, create the request object and display the results
#           3.1 Time-Series
#           3.2 Cross-Sectional

# 1. Import the required packages

import requests
import json
import pandas as pd
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import os
from dotenv import load_dotenv
load_dotenv()

# 2. Create a connection object

# Enter your credentials for 'Username' and 'API Key' variables below.
# To generate an API key, visit (https://developer.factset.com/authentication) for more details on Authentication.

authorization = (os.getenv('username_universal'),os.getenv('pass_home'))

#%%

# 3.2 Cross-Sectional Endpoint
# For a list of ids, return the previous day's price and the company name.
# 3.2a `/formula-api/v1/cross-sectional` - Create a request object and set the parameters

cross_sectional_endpoint = 'https://api.factset.com/formula-api/v1/cross-sectional'
request ={
  "data":{
      "universe": 
        "(FG_CONSTITUENTS(113648,0,CLOSE))=1",
      "formulas": [
        "PROPER_NAME",
        "FG_CONST_WEIGHT(113648,0)",
        "P_CURRENCY(ISO)",
        "FREF_ENTITY_COUNTRY(INCORP,NAME)"
      ]
  }
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# 3.2b `/formula-api/v1/cross-sectional` - Pull data and view results

post = json.dumps(request)
response = requests.post(url = cross_sectional_endpoint, data = post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(response.status_code))

# View results

json_output = json.loads(response.text)
json_formatted = json.dumps(json_output, indent=2)
print(json_formatted)
                
# %%


json_output['data'][2]
# %%
