#%%

# Content API - FactSet Estimates - Rolling Consensus - code snippet

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas import json_normalize

# auth
import os
from dotenv import load_dotenv
load_dotenv()


# 2. Create a connection object

# auth
authorization = (os.getenv('username_universal'),os.getenv('pass_home'))



#%%

# 3. FactSet Quant Factor Library API Endpoint Details - Factors : Fetch Quant Factors for large list of ids.
# 3.1a `/factset-quant-factor-library/v1/factors` - Create a request object and set the parameters
factors_endpoint = 'https://api.factset.com/content/factset-quant-factor-library/v1/factors'
factors_request = {
  "ids": [
    "MSFT-US",
    "AAPL-US",
    "IBM-US",
    "TSLA-US",
    "META-US"
  ],
  "factors": [
    "brdFemaleNum",
    "mgmtFemaleCeo",
    "mgmtNum",
    'brdFemaleChair'
  ],
  "factorGroups": [
    "Corporate_Governance"
  ],
  "startDate": "2000-01-01",
  "endDate": "2021-12-31",
  "frequency": "CY"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}
# 3.1b `/factset-quant-factor-library/v1/factors` - Pull data, display datafame properties, show initial records
factors_response = requests.post( url=factors_endpoint, json=factors_request,auth=authorization, headers=headers, verify= False )
print('HTTP Status: {}'.format(factors_response.status_code))
#create a dataframe from POST request, show dataframe properties
factors_data = json.loads(factors_response.text)
factors_df = json_normalize(factors_data['data'])

#factors_df.info(verbose=True)

print('RECORDS:',len(factors_df))
# Show the last 5 records
factors_df#[['date','brdFemaleNum']]


# %%
