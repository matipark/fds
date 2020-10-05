#%%
# Import the required packages
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

# Insert

ticker = 'SI00-USA' #'GC00-USA'
date = '20201001'
authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')


#%%

# API Calls

tick_history_endpoint = 'https://api.factset.com/TickHistory/history?id={}&date={}&format=json'.format(ticker, date)

# Create a GET Request
tick_history_response = requests.get(url = tick_history_endpoint, auth = authorization, verify= False)
print('HTTP Status: {}'.format(tick_history_response.status_code))


#%%

# Create a dataframe from GET request, show dataframe properties
tick_history_data = json.loads(tick_history_response.text)
tick_history_df = json_normalize(tick_history_data, 'Field Names')
tick_history_df2 = json_normalize(tick_history_data, 'Values').transpose()
final_df = pd.concat([tick_history_df, tick_history_df2], axis=1).transpose()

final_df = final_df.drop([12,16,17,18], axis=1)


print('COLUMNS:')
print('')
print(final_df.dtypes)
print('')
print('RECORDS:',len(final_df))
# Display the Records
print(final_df)




#%%

print('COLUMNS:')
print('')
print(final_df.dtypes)
print('')
print('RECORDS:',len(final_df))
# Display the Records
print(final_df)


df2 = final_df[1:].apply(pd.to_numeric, errors='ignore')



print(df2.dtypes)
df2

# %%

# Convert data type
# https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
# https://api.factset.com/TickHistory/history?id=GC00-USA&date=20201001&format=json

# json_normalize
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html