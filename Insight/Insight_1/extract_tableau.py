#%%

# Importing libraries

import pandas as pd
from pandas.io.json import json_normalize
import pantab
from tableauhyperapi import TableName

import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# %%

# AUTH

authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')


#%%

# Pulling data from API
 
tickers = ["IBM-US","FDS-US"]
metrics_ff = ["FF_EPS","FF_NET_INC"]
startdate = "2000-01-01"
enddate = "2020-01-01"



prices_endpoint = 'https://api.factset.com/content/factset-prices/v1/prices'
fundamentals_endpoint = 'https://api.factset.com/content/factset-fundamentals/v1/fundamentals'

prices_request ={
  "ids": tickers,
  "startDate": startdate,
  "endDate": enddate,
  "frequency": "D",
  "calendar": "FIVEDAY",
  "currency": "LOCAL",
  "adjust": "SPLIT"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

fundamentals_request={
  "ids": tickers,
  "periodicity": "QTR",
  "fiscalPeriodStart": startdate,
  "fiscalPeriodEnd": enddate,
  "metrics": metrics_ff,
  "currency": "USD",
  "restated": "RP"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# %%

# Building df

prices_post = json.dumps(prices_request)
prices_response = requests.post(url = prices_endpoint, data=prices_post, auth = authorization, headers = headers, verify= False )

fundamentals_post = json.dumps(fundamentals_request)
fundamentals_response = requests.post(url = fundamentals_endpoint, data=fundamentals_post, auth = authorization, headers = headers, verify= False )


prices_data = json.loads(prices_response.text)
prices_df = json_normalize(prices_data['data'])

fundamentals_data = json.loads(fundamentals_response.text)
fundamentals_df = json_normalize(fundamentals_data['data'])

#%%

# Save One df output to .hyper file

# pantab.frame_to_hyper(prices_df, r"C:\Users\mpark\OneDrive - FactSet\Desktop\Tableau\content_api_test.hyper", table = "prices")


# %%

# writing multiple df

dict_df = {"prices": prices_df, "ff": fundamentals_df}

pantab.frames_to_hyper(dict_df, r"C:\Users\mpark\OneDrive - FactSet\Desktop\Tableau\content_api_test.hyper")

#%%

# Reference

# https://towardsdatascience.com/a-primer-on-pantab-81a9dae81b2c
# https://github.com/c-l-nguyen/pantab-pokemon/blob/master/pantab_tutorial.ipynb
# https://help.tableau.com/current/api/hyper_api/en-us/docs/hyper_api_create_update.html