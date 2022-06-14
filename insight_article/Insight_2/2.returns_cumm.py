#%%

import pandas as pd
import pyodbc
import time
import warnings

import loadsql #functions to load sql queries

from datetime import datetime
from IPython.display import display

import numpy as np
import pandas as pd


# connecting python with SQL 
dsn = 'SF'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)

#%%

bdx_board_char_type = "\'Overall Board Characteristics\'"

start_time = time.time()

r3000_query = loadsql.get_sql_q('3.bdx_sf_tr.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_result = pd.read_sql(r3000_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))


r3000_mcv_query = loadsql.get_sql_q('3.bdx_sf_tr_MCV.sql',show=0,connection=dsn, skipSubsCheck=1)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_mcv_result = pd.read_sql(r3000_mcv_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

r3000_pr_query = loadsql.get_sql_q('4.calc_returns_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_pr_result = pd.read_sql(r3000_pr_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))


final_df = pd.merge(r3000_pr_result, r3000_result, on=['FSYM_ID','DATE_YEAR'], how='inner')
final_mcv_df = pd.merge(r3000_pr_result, r3000_mcv_result, on=['FSYM_ID','DATE_YEAR'], how='inner')


# final_df[ final_df['DATE_YEAR'] == 2020]
# boolean = not final_df[final_df['DATE_YEAR'] == 2021]['FSYM_ID'].is_unique  

#%%

final_df['quintile_gender'] = pd.cut(final_df['BDX_GENDER_RATIO'], 5) # around mid is best, 100 means man
final_df['quintile_nationality'] = pd.cut(final_df['BDX_NATIONALITY_MIX'], 5)
r3000_result['quals_ratio'] = r3000_result['BDX_AVG_QUALS'].div(r3000_result['BDX_NUMBER_DIRECTORS'], axis=0) # ratio of qualifications / number of board members
final_df['quintile_quals'] = pd.cut(r3000_result['quals_ratio'], 5)


final_df['BDX_GENDER_RATIO'].head()
final_mcv_df['MCV_CEO_RANK'].head()


#, labels=False
#, duplicates='drop'

#r3000_result[r3000_result['quintile'] == 0]
#r3000_result['ONE_YR_PCT_2'] = r3000_result['ONE_YR_PCT'].apply(lambda x: x/100 + 1)

#%%

# calcultate market cap weights for each security by year

final_df['mcap_sum'] = final_df.groupby('DATE_YEAR')['BDX_MARKET_CAP'].transform('sum')
final_df['annual_mcap_weight'] = final_df['BDX_MARKET_CAP']/final_df['mcap_sum']

final_mcv_df['mcap_sum'] = final_mcv_df.groupby('DATE_YEAR')['FF_MKT_VAL'].transform('sum')
final_mcv_df['annual_mcap_weight'] = final_mcv_df['FF_MKT_VAL']/final_mcv_df['mcap_sum']


#final_df[final_df['DATE_YEAR']==2020]['BDX_MARKET_CAP_WEI'].sum()

# r3000_result['BDX_MARKET_CAP_WEI'].sum()
# r3000_result['BDX_GENDER_RATIO'].count()

# multiply return by market cap weights

final_df['ann_weighted_return'] = final_df['ANN_RETURN'].mul(final_df['annual_mcap_weight']*100, axis=0)

final_mcv_df['ann_weighted_return'] = final_mcv_df['ANN_RETURN'].mul(final_mcv_df['annual_mcap_weight']*100, axis=0)

#%%

# add up to calculate the bottom-up return by factor and year

final_df.groupby(['DATE_YEAR','quintile_gender']).sum()['ann_weighted_return'].tail(15)
final_mcv_df.groupby(['DATE_YEAR','MCV_CEO_RANK']).sum()['ann_weighted_return'].tail(15)


# Calculate cummulative return from year xxxx

factors = ['quintile_gender','quintile_nationality','quintile_quals']

for i in factors:
    print(final_df[final_df['DATE_YEAR']>2017].groupby(i).sum()['ann_weighted_return'])
    print('\n')

factors_mcv = ['MCV_CEO_RANK','MCV_TEAM_RANK']

for i in factors_mcv:
    print(final_mcv_df[final_mcv_df['DATE_YEAR']>2017].groupby(i).sum()['ann_weighted_return'])
    print('\n')

final_df[['DATE_YEAR','quintile_gender','ann_weighted_return']]

# r3000_result.groupby('quintile_nationality').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]
# r3000_result.groupby('quintile_quals').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]


#%%

# count in each one of the factors

final_df.groupby('quintile_gender')['quintile_gender'].count()
final_df.groupby('quintile_nationality')['quintile_nationality'].count()
final_df.groupby('quintile_quals')['quintile_quals'].count()

r3000_mcv_result.groupby('quintile_gender')['quintile_nationality'].count()
r3000_mcv_result.groupby('quintile_nationality')['quintile_nationality'].count()


# ranking by factor then calculate overall

#df['default_rank'] = df['Number_legs'].rank()

# %%
