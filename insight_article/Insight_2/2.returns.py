#%%

import pandas as pd
import pyodbc
import time
import warnings

from scipy.fftpack import dstn
import loadsql #functions to load sql queries

from datetime import datetime
from IPython.display import display

import numpy as np
import pandas as pd
from sklearn import datasets
import seaborn as sns
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from sklearn import preprocessing
from scipy.stats import pearsonr

#%%


# connecting python with SQL 
dsn = 'SF'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)



#%%

bdx_board_char_type = "\'Overall Board Characteristics\'"

start_time = time.time()

r3000_query = loadsql.get_sql_q('3.returns_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)

with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    r3000_result = pd.read_sql(r3000_query,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))


#%%

r3000_result['quintile_gender'] = pd.cut(r3000_result['BDX_GENDER_RATIO'], 4) # around mid is best, 100 means man
r3000_result['quintile_nationality'] = pd.cut(r3000_result['BDX_NATIONALITY_MIX'], 4)

r3000_result['quals_ratio'] = r3000_result['BDX_AVG_QUALS'].div(r3000_result['BDX_NUMBER_DIRECTORS'], axis=0) # ratio of qualifications / number of board members
r3000_result['quintile_quals'] = pd.cut(r3000_result['quals_ratio'], 4)

r3000_result['BDX_GENDER_RATIO'].head()

#, labels=False
#, duplicates='drop'

#r3000_result[r3000_result['quintile'] == 0]
#r3000_result['ONE_YR_PCT_2'] = r3000_result['ONE_YR_PCT'].apply(lambda x: x/100 + 1)

#%%

#r3000_result[['BDX_MARKET_CAP', 'ISO_CURRENCY']]

r3000_result['BDX_MARKET_CAP_WEI'] = r3000_result['BDX_MARKET_CAP'].apply(lambda x: x/r3000_result['BDX_MARKET_CAP'].sum()) # Market Cap weighted


# r3000_result['BDX_MARKET_CAP_WEI'].sum()
# r3000_result['BDX_GENDER_RATIO'].count()

r3000_result[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']] = r3000_result[['YTD_PCT','ONE_YR_PCT','TWO_YR_PCT']].mul(r3000_result['BDX_MARKET_CAP_WEI'], axis=0)

#%%

r3000_result.groupby('quintile_gender').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]
r3000_result.groupby('quintile_nationality').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]
r3000_result.groupby('quintile_quals').sum()[['ytd_weighted_return','1yr_weighted_return_2','2yr_weighted_return_3']]


#%%

r3000_result.groupby('quintile_gender')['quintile_nationality'].count()
r3000_result.groupby('quintile_nationality')['quintile_nationality'].count()
r3000_result.groupby('quintile_quals')['quintile_nationality'].count()


# ranking by factor then calculate overall

#df['default_rank'] = df['Number_legs'].rank()

# %%
