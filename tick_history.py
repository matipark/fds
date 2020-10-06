#%%
# Import the required packages
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

# parameters

ticker = 'SI00-USA'
ticker_2 =  'GC00-USA'
ticker_list = ['SI00-USA','GC00-USA']
start_date = '20200915'
end_date = '20200930'
start_time = '000000'
end_time = '235959'
interval = '1H'
authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')


#%%

# create a GET Request

def tick_history_connectivity(ticker, start_date, end_date, start_time, end_time, interval):
  global tick_history_response
  tick_history_endpoint = 'https://api.factset.com/TickHistory/history?id={}&start_date={}&end_date={}&start_time={}&end_time={}&interval={}&format=json'.format(ticker, start_date, end_date, start_time, end_time, interval)
  
  tick_history_response = requests.get(url = tick_history_endpoint, auth = authorization, verify= False)
  print('HTTP Status: {}'.format(tick_history_response.status_code))

# transform json into dataframe

def put_in_df(ticker):
  global final_df
  tick_history_data = json.loads(tick_history_response.text)
  tick_history_df = json_normalize(tick_history_data, 'Field Names')
  tick_history_df2 = json_normalize(tick_history_data, 'Values').transpose()
  final_df = pd.concat([tick_history_df, tick_history_df2], axis=1).transpose()
  final_df = final_df.drop([12,16,17,18], axis=1) # dropping fields that are not needed
  final_df.rename(columns=final_df.iloc[0], inplace = True)
  final_df.drop([0], inplace = True) # transform non-header into headers
  final_df.insert(0, 'TICKER', ticker) # insert ticker column
  final_df = final_df.apply(pd.to_numeric, errors='ignore') # transform obj to numeric

  # transform LAST_TIME column and add a new HOUR column

  final_df.loc[final_df['LAST_TIME'].astype(str).str.len() < 8, 'HOUR'] = 0 # if length is below 8 digits, then 0
  final_df.loc[final_df['LAST_TIME'].astype(str).str.len() == 8, 'HOUR'] = final_df['LAST_TIME'].astype(str).str[:1].astype(int)
  final_df.loc[final_df['LAST_TIME'].astype(str).str.len() == 9, 'HOUR'] = final_df['LAST_TIME'].astype(str).str[:2].astype(int)

  print('COLUMNS:')
  print('')
  print(final_df.dtypes)
  print('')
  print('RECORDS:',len(final_df))
  # Display the Records
  print(final_df)

#%%

d = {}

for ticker in ticker_list:
  tick_history_connectivity(ticker, start_date, end_date, start_time, end_time, interval)
  put_in_df(ticker)
  i = ticker_list.index(ticker)
  d["output_dataframe{}".format(i)] = final_df

d["output_dataframe0"]
d["output_dataframe1"]



#%%



# %%

# Convert data type
# https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
# https://api.factset.com/TickHistory/history?id=GC00-USA&date=20201001&format=json

# json_normalize
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.json_normalize.html




#%%

import pandas as pd

numbers = {'set_of_numbers': [1,2,3,4,5,6,7,8,9,10]}
df = pd.DataFrame(numbers,columns=['set_of_numbers'])

df.loc[df['set_of_numbers'] <= 4, 'equal_or_lower_than_4?'] = 'True' 
df.loc[df['set_of_numbers'] > 4, 'equal_or_lower_than_4?'] = 'False' 

print (df)



# %%
