#%%

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize


# %%

authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')
fund_holdings_endpoint = 'https://api.factset.com/content/factset-ownership/v1/fund-holdings'


fund_holdings_request = {
  "ids": [
    "FDIVX-US"
  ],
  "date": "2019-09-30",
  "topn": 1000,
  "assetType": "EQ"
}

headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# %%

fund_holdings_post = json.dumps(fund_holdings_request)
fund_holdings_response = requests.post(url = fund_holdings_endpoint, data=fund_holdings_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(fund_holdings_response.status_code))
#create a dataframe from POST request, show dataframe properties
fund_holdings_data = json.loads(fund_holdings_response.text)
fund_holdings_df = json_normalize(fund_holdings_data['data'])
print('COLUMNS:')
print('')
print(fund_holdings_df.dtypes)
print('')
print('RECORDS:',len(fund_holdings_df))
# #### Display the Records
print(fund_holdings_df[['fsymId','requestId','fsymSecurityId','fsymRegionalId','date','securityName','securityTicker','issueType','adjHolding','adjMarketValue']].tail())


# %%
