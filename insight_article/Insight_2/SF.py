#%%

import pandas as pd
import pyodbc
import time
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'SF'
pw = 'FDSSnowflake_S@1ES'
connection_to_sql = pyodbc.connect('DSN={dsn_name};pwd={password}'.format(dsn_name = dsn, password = pw))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)

#%%

p_date = '2022-04-07'
bdx_board_char_type = 'Overall Board Characteristics'

start_time = time.time()

sql_query_1 = loadsql.get_sql_q('1.bdx_sf.sql',show=0,connection=dsn).format(p_date=p_date, bdx_board_char_type=bdx_board_char_type)
df_1 = pd.read_sql(sql_query_1,connection_to_sql)
#df_1['p_date'] = pd.to_datetime(df_1['p_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# %%
