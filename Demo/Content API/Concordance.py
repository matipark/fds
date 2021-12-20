#%%

#Concording 25 Names Synchronously
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize
# First you must Authorize your requests by pulling in your USERNAME-SERIAL and API-Key. Insert those values below - 


#%%

#authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')
# Office key
authorization = ('FDS_DEMO_FE-410734','GItuvdYsPrZl84GJQmjVzl0Krn9SYSjw3jnscEYy')

###
entity_match_endpoint = 'https://api.factset.com/content/factset-concordance/v1/entity-match'

entity_match_request ={
  "input": [
    # {"name":"Apple Inc.","clientId": "abc-123", "country": "US", "url": "https://www.apple.com/"},
    # {"name":"Microsoft Corporation", "clientId": "abc-123"},
    {
      "name": "Amazon.com, Inc.",
      "clientId": "abc-123",
      "country": "US",
      "state": "WA",
      "url": "www.amazon.com"
    },
{"name":"Symantec, Inc", "clientId": "abc-123", "country": "US", "state": "MA"},
{"name":"Tesla Inc", "clientId": "abc-123"},
{"name":"Alphabet Inc. Class A", "clientId": "abc-123"},
{"name":"Berkshire Hathaway Inc. Class B", "clientId": "abc-123"},
{"name":"Johnson & Johnson", "clientId": "abc-123"},
{"name":"JPMorgan Chase & Co.", "clientId": "abc-123"},
{"name":"Visa Inc. Class A", "clientId": "abc-123"},
{"name":"NVIDIA Corporation", "clientId": "abc-123"},
{"name":"UnitedHealth Group Incorporated", "clientId": "abc-123"},
{"name":"Procter & Gamble Company", "clientId": "abc-123"},
{"name":"Walt Disney Company", "clientId": "abc-123"},
{"name":"Home Depot, Inc.", "clientId": "abc-123"},
{"name":"Mastercard Incorporated Class A", "clientId": "abc-123"},
{"name":"PayPal Holdings Inc", "clientId": "abc-123"},
{"name":"Netflix, Inc.", "clientId": "abc-123"},
{"name":"Intel Corporation", "clientId": "abc-123"},
{"name":"Bank of America Corp", "clientId": "abc-123"},
{"name":"Verizon Communications Inc.", "clientId": "abc-123"},
{"name":"Adobe Inc.", "clientId": "abc-123"},
{"name":"Comcast Corporation Class A", "clientId": "abc-123"},
{"name":"AT&T Inc.", "clientId": "abc-123"},
{"name":"Merck & Co., Inc.", "clientId": "abc-123"}],

  "includeParent": False
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}


#%%
# CREATE THE POST

#create a post request and print the Status Code

entity_match_post = json.dumps(entity_match_request)
entity_match_response = requests.post(url = entity_match_endpoint, data=entity_match_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(entity_match_response.status_code))

#create a dataframe from POST request, show dataframe properties

entity_match_data = entity_match_response.json()
entity_match_df = json_normalize(entity_match_data['data'])
print('COLUMNS:')
print('')
print(entity_match_df.dtypes)
print('')
print('RECORDS:',len(entity_match_df))

#%%

# SHOW THE FIRST/LAST FIVE RECORDS

entity_match_df.head(25)
#entity_match_df.tail()


# %%

