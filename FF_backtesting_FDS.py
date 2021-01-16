


#%%
#Settings
new_money_in = 10000
#Set our rebalance threshold
rebal_threshold = .30 #allowable allocation drift
rebal_timeframe = -30 #in days


#%%

#Define target and current allocations
#create our target allocation
columns_t = ['ticker','allocation_target','assetclass']
positions_t = [['CBA-AU',0.15,'EQ'],
               ['BHP-AU',0.15,'EQ'],
               ['CSL-AU',0.15,'EQ'],
               ['NAB-AU',0.15,'EQ'],
               ['FMG-AU',0.15,'EQ'],
               ['WBC-AU',0.15,'EQ'],
               ['ANZ-AU',0.10,'EQ']]



#set our current portfolio
columns_c = ['lastrebaldate','ticker','assetclass','basisdate','costbasis','shares']
positions_c = [['2020-11-16','CBA-AU','EQ','2020-11-16',1,913.483],
             ['2020-11-16','BHP-AU','EQ','2020-11-16',1,514.298],
             ['2020-11-16','CSL-AU','EQ','2020-11-16',10,151.121],
             ['2021-01-05','NAB-AU','EQ','2020-11-16',1,772.407],
             ['2021-01-05','GMG-AU','EQ','2020-11-16',20,151.578],
             ['2021-01-05','COL-AU','EQ','2020-11-16',1,3.14],
             ['2021-01-05','REA-AU','EQ','2020-11-16',10,549.871]]



#%%

# Content API

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize


authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')
prices_endpoint = 'https://api.factset.com/content/factset-prices/v1/prices'


#Lets import the necessary packages
import pandas as pd
from IPython.display import display
pd.set_option('display.max_columns', None)
import numpy as np
import datetime
import decimal
from pandas_datareader import data as pdr
#define todays datetime
now = datetime.datetime.now()


#%%



#initialize target portfolio
targetalloc = pd.DataFrame(columns = columns_t, data = positions_t)
total=decimal.Decimal(targetalloc.allocation_target.sum())
#check that our target allocation indeed adds to 100%
assert round(total,4) == 1,'Target Allocation not 100% : {}'.format(int(total))

#initialize current portfolio
start_port = pd.DataFrame(columns = columns_c, data = positions_c)
start_port.lastrebaldate = pd.to_datetime(start_port.lastrebaldate)
start_port.basisdate = pd.to_datetime(start_port.basisdate)

#custom apply function
def f(x):
    d = {}
    d['lastrebaldate'] = x['lastrebaldate'].max()
    d['assetclass'] = x['assetclass'].max()
    d['basisdate'] = x['basisdate'].min()
    d['costbasis'] = (x['costbasis'] * x['shares']).sum()/(x['shares'].sum() or 1) #weighted avg
    d['shares'] = x['shares'].sum()
    return pd.Series(d, index=['lastrebaldate', 'assetclass', 'basisdate', 'costbasis', 'shares'])

#aggregate by ticker to account for duplicate securities held in different accounts
agg_port = start_port.groupby(['ticker']).apply(f)

#Define list of distinct tickers - duplicates removed
tickers = list(dict.fromkeys(targetalloc.ticker.unique().tolist()+start_port.ticker.unique().tolist()))


#%%

def get_prices():

  prices_request ={
    "ids": tickers, #grab list from target portfolio
    "startDate": "2021-01-10",
    "endDate": "2021-01-10",
    "frequency": "D",
    "calendar": "FIVEDAY",
    "currency": "LOCAL",
    "adjust": "SPLIT"
  }
  headers = {'Accept': 'application/json','Content-Type': 'application/json'}


  prices_post = json.dumps(prices_request)
  prices_response = requests.post(url = prices_endpoint, data=prices_post, auth = authorization, headers = headers, verify= False )

  prices_data = json.loads(prices_response.text)
  prices_df = json_normalize(prices_data['data'])

  # show the last 5 records for select columns
  return prices_df[["fsymId","date","adjDate","currency","price","priceOpen","priceHigh","priceLow","volume","requestId"]]



ohlc2 = get_prices()[["requestId","price"]]
ohlc2 = ohlc2.rename(columns={'requestId': 'ticker', 'price': 'close'}) # renaming ticker column name


# start_port_c.dtypes
# # ohlc2.dtypes
# type(ohlc2)
# type(start_port_c)

#ohlc2['price']=ohlc2['price'].astype(float)

# %%



#concatenate target allocation and latest prices with our portfolio
start_port_c = pd.merge(agg_port, targetalloc, on ='ticker', how ='outer')
final_port = pd.concat([start_port_c.set_index('ticker'), ohlc2.set_index('ticker')], axis=1, join='outer').reset_index() #reset index will convert the index back to column "ticker"

final_port = final_port.rename(columns={'index': 'ticker'})

#set target to zero for tickers held but not present in our target allocation, set initial basisdate and costbasis for new securities entering the portfolio
final_port.fillna(value = {'allocation_target':0.0,'shares':0.0,'basisdate':pd.to_datetime(now.strftime("%Y-%m-%d")),'costbasis':final_port.close,'assetclass_x':final_port.assetclass_y},inplace = True)
final_port.drop(['assetclass_y'],axis=1,inplace=True)
final_port.rename(columns={'assetclass_x':'assetclass'},inplace=True)

#calculate holding values and current allocation
final_port['value'] = final_port.close * final_port.shares #calculate value as price x shares
final_port.loc[final_port.value.isna() & final_port.shares.isna(),['value']]=0.0 #for securities not currently held but in our target (and close price failed to return), establish zero value




final_port['allocation'] = final_port.value / final_port.value.sum()
final_port['correction'] = final_port.allocation_target - final_port.allocation
final_port['new_money_in'] = new_money_in * final_port.allocation_target #Account for new money in



# %%



# Create timedelta int column. days from the last rebalance date
final_port['timedelta'] = (final_port.lastrebaldate - pd.to_datetime(now.strftime("%Y-%m-%d"))).dt.days
final_port.timedelta.fillna(0,inplace=True)

#define rebalance flags to determine if we must rebalance

# Determine if need to rebalance by threshold
final_port['rebal_flag_thresh'] = np.where((abs(final_port.correction)<=rebal_threshold) & (final_port.allocation > 0),0,1)

# Determine if need to rebalance by time
final_port['rebal_flag_time'] = np.where(final_port.timedelta >= rebal_timeframe,1,0)

# Force rebal securities not present in our target portfolio
final_port['rebal_flag_exit'] = np.where((final_port.allocation > 0) & (final_port.allocation_target==0),1,0) 

# Determine if need to input more money
final_port['rebal_flag_newmoney'] = np.where(final_port.new_money_in > 0,1,0)

# Final decision - needs a fix for time
final_port['rebal_flag'] = np.where(final_port.rebal_flag_thresh + final_port.rebal_flag_time + final_port.rebal_flag_exit + final_port.rebal_flag_newmoney >= 1, 1,0)



#Subset of securities we need to rebalance
rebal_port = final_port[final_port.rebal_flag==1].copy()
#Securities that do not need to rebalance
stable_port = final_port[final_port.rebal_flag==0].copy()



# %%

# Calculate our current allocation, target, and the change we need to hit target
total_val = rebal_port.value.sum()

# Current allocation
rebal_port['allocation'] = rebal_port.value/rebal_port.value.sum()

# Target
rebal_port['allocation_target'] = rebal_port.allocation_target/rebal_port.allocation_target.sum()
# Correction
rebal_port['correction'] = rebal_port.allocation_target - rebal_port.allocation

#Factor in any new money entering the portfolio and determine necessary changes in value and shares
rebal_port['value_chg'] = (total_val * rebal_port.correction) + rebal_port.new_money_in
rebal_port['shares_chg'] = rebal_port.value_chg / rebal_port.close
rebal_port.loc[rebal_port.value_chg.isna() & rebal_port.shares > 0,['shares_chg']]=-rebal_port.shares #sell all shares of securities not in our target portfolio

#Round off shares to whole numbers, except when we are fully exiting a position
rebal_port['shares_chg_round'] = rebal_port.shares_chg
rebal_port = rebal_port.astype({'shares_chg_round': int})
rebal_port['final_shares_chg'] = rebal_port.shares_chg
rebal_port.loc[np.round(rebal_port.shares_chg+rebal_port.shares)!=0,['final_shares_chg']]=rebal_port.shares_chg_round*1.0
rebal_port.drop(['shares_chg_round'],axis=1,inplace=True)

#Calculate initial new shares and values
rebal_port['new_shares'] = np.round(rebal_port.shares + rebal_port.final_shares_chg,3)
rebal_port['new_value'] = rebal_port.new_shares * rebal_port.close #due to share rounding, there will be slight variance vs. portfolio starting value
rebal_port['new_value_chg'] = rebal_port.final_shares_chg * rebal_port.close


# %%


#Double check our work so far
#net of buying and selling should be zero
assert(np.round(rebal_port.value_chg.sum(),3)-new_money_in==0) 
#make sure totals match (with rounding error + new money in) from original portfolio and rebalanced portfolio
assert(np.round(rebal_port.new_value.sum() - rebal_port.value.sum(),3)==np.round((rebal_port.new_value.sum() + stable_port.value.sum()) - final_port.value.sum(),3))



# %%

#Merge our rebalanced portfolio with our stable portfolio for our execution portfolio
stable_port['value_chg'] = 0
stable_port['shares_chg']=0
stable_port['final_shares_chg'] = 0
stable_port['new_value_chg'] = 0
stable_port['new_shares'] = stable_port.shares
stable_port['new_value'] = stable_port.value
exec_port = pd.concat([rebal_port,stable_port],sort=False)
exec_port.drop(columns=['timedelta','rebal_flag_thresh','rebal_flag_time','rebal_flag_exit','rebal_flag_newmoney','value_chg','shares_chg'],inplace=True)

#Reset allocations to be based on all securities
exec_port['allocation'] = exec_port.value/exec_port.value.sum()
exec_port['allocation_target'] = exec_port.allocation_target/exec_port.allocation_target.sum()
exec_port['correction'] = exec_port.allocation_target - exec_port.allocation
exec_port['final_allocation'] = exec_port.new_value / exec_port.new_value.sum()

# %%

#Lets look at all our work to get to our target portfolio
exec_port


#%%

#Lets add a bar chart here to show the new allocation vs. the target allocation and vs. the original portfolio
graph_port = exec_port[['ticker','allocation','allocation_target','final_allocation']].copy()
graph_port.plot.barh(x='ticker',figsize=(20,10))




#%%










# %%

# Reference
# https://medium.com/swlh/how-to-build-a-multi-factor-equity-portfolio-in-python-4560fab3df7b
# https://github.com/StevenDowney86/Public_Research_and_Backtests/blob/master/Multi-Factor/portfolio_multi_factor_models_rebalance_annually_public_medium_OOS.py

# https://evgenypogorelov.com/portfolio-rebalancing-python
# https://github.com/pogoetic/rebalance/blob/master/portfolio_rebalance.ipynb

#%%