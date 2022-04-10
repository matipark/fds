#%%

import pandas as pd
import pyodbc
import time
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'FDSServer'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
print(how_many)

#%%

p_date = '2022-04-07'
bdx_board_char_type = 'Overall Board Characteristics'

start_time = time.time()

sql_query_1 = loadsql.get_sql_q('0.pull_universe_returns.sql',show=0,connection=dsn).format(p_date=p_date, bdx_board_char_type=bdx_board_char_type)
df_1 = pd.read_sql(sql_query_1,connection_to_sql)
#df_1['p_date'] = pd.to_datetime(df_1['p_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))


# %%
p_date = '2022-04-07'
dsn2 = 'FDSServer2'
connection_to_sql_2 = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn2))
sql_query_2 = loadsql.get_sql_q('1.bdx.sql',show=0,connection=dsn2).format(p_date=p_date)
df_2 = pd.read_sql(sql_query_2,connection_to_sql_2)

# %%
