#%%

# Formula API - Batch Requests Sample Python Code Snippet

# This snippet demonstrates how to make Batch Requests using the FactSet Formula API by walking through the following steps:
#        1. Import Python packages
#        2. Enter your Username and API Key for authorization
#        3. Initiate the Batch Request
#        4. Check the status of the Batch Request
#        5. Retrieve the results of the completed Batch Request        

# 1. Import the required packages

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import os
from dotenv import load_dotenv
load_dotenv()
#%%

# 2. Create a connection object

# Enter your credentials for 'Username' and 'API Key' below.
# To generate an API key, visit (https://developer.factset.com/authentication) for more details on Authentication.

authorization = (os.getenv('username_universal'),os.getenv('pass_home'))


# Set Required Headers
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# 3. Initiate the Batch Request

# 3.1 Create the Batch Request Object
# Using the `time-series` endpoint, return one year of daily prices and the company name for the top 250 U.S. common stocks by market cap that are currently trading.
# To make a Batch Request, construct the standard request for the endpoint and add the parameter "batch": "Y"

time_series_endpoint = 'https://api.factset.com/formula-api/v1/time-series'
batch_request ={
  "data":{
      "batch": "Y",
      "universe": "URANKX((F_COUNTRY=\"UNITED STATES\" AND ISON_INACTIVE=0 AND ISON_SECONDARY=0 AND P_SEC_TYPE(CODE,GEN)=0)=1,FG_MKT_VALUE)<=250S",
      "formulas": [
        "P_PRICE(0,-1AD,D)",
        "PROPER_NAME"
      ],
      "flatten": "Y"
  }
}


#%%


# 3.2 Make the Batch Request

batch_request_json = json.dumps(batch_request)
response = requests.post(url = time_series_endpoint, data = batch_request_json, auth = authorization, headers = headers, verify= False)
print('HTTP Status: {}'.format(response.status_code))


#%%

# 3.3 View the output
batch_request_data = json.loads(response.text)
batch_request_data_formatted = json.dumps(batch_request_data, indent=2)
print(batch_request_data_formatted)

# Save the batch id to check the status and pick up the results
batch_id = batch_request_data['data']['id']


#%%

# 4. Check the Status of the Batch Request

# 4.1 Create the `/batch-status` Request Object
# All that is required to check the status is the batchId from the initial Batch Request

status_endpoint = 'https://api.factset.com/formula-api/v1/batch-status'
batch_id_request ={
  "data":{
      "id": batch_id
  }
}


#%%



# 4.2 Make the `/batch-status` Request

batch_id_request_json = json.dumps(batch_id_request)
batch_status_response = requests.post(url = status_endpoint, data = batch_id_request_json, auth = authorization, headers = headers, verify= False)
print('HTTP Status: {}'.format(batch_status_response.status_code))

# 4.3 View the Status in the output
batch_status_data = json.loads(batch_status_response.text)
batch_status_data_formatted = json.dumps(batch_status_data, indent=2)
print(batch_status_data_formatted)


#%%

# 5. Pick up the Results of the Batch Request

# 5.1 Create the `/batch-result` Request Object
# Once the status is "DONE", the results are ready for pick up.
# The request object for the `/batch-status` and `/batch-result` endpoints are the same. We will re-use the batch_id_request object.

result_endpoint = 'https://api.factset.com/formula-api/v1/batch-result'

# 5.2 Make the `/batch-result` Request

batch_result_response = requests.post(url = result_endpoint, data = batch_id_request_json, auth = authorization, headers = headers, verify= False)
print('HTTP Status: {}'.format(batch_result_response.status_code))

# 5.3 View the Results
batch_result_data = json.loads(batch_result_response.text)
batch_result_data_formatted = json.dumps(batch_result_data, indent=2)
print(batch_result_data_formatted)

                
# %%
