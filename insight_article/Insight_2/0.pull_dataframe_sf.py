#%%

import pandas as pd
import pyodbc
import time
import warnings

from scipy.fftpack import dstn
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'SF'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)

#%%

bdx_board_char_type = 'Overall Board Characteristics'

start_time = time.time()

sql_query_1 = loadsql.get_sql_q('1.bdx_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    df_1 = pd.read_sql(sql_query_1,connection_to_sql)
#df_1['p_date'] = pd.to_datetime(df_1['p_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# %%


df_1

# %%
