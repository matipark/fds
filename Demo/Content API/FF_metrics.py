#%%

# Content API - FactSet Fundamentals - fundamentals end point python code snippet

# 1. Import the required packages
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize


import os
from dotenv import load_dotenv
load_dotenv()


#%%

fundamentals_endpoint = 'https://api.factset.com/content/factset-fundamentals/v1/metrics?category=RATIOS&subcategory=VALUATION'


# %%

# auth
authorization = (os.getenv('username_universal'),os.getenv('pass_home'))
#headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# Create a POST Request
# fundamentals_post = json.dumps(fundamentals_request)
fundamentals_response = requests.get(url = fundamentals_endpoint, auth = authorization)


fundamentals_data = json.loads(fundamentals_response.text)
fundamentals_df = json_normalize(fundamentals_data['data'])
print(fundamentals_df)

# %%
