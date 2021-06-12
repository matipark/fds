#%%

import pandas as pd
import numpy as np
import pyodbc
import os
import lxml
from bs4 import BeautifulSoup
import zipfile
import time
import glob
import datetime
import matplotlib.pyplot as plt
from IPython.display import display, Markdown,HTML
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'FDSServer'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))


#%%

ticker = 'FDS-US'
call_type = 'Earnings Call'
start_date = '2020-01-01'
end_date = '2020-12-31'



start_time = time.time()

# retriving all participants for the last 3 months
sql_query_1 = loadsql.get_sql_q('extract_data.sql',show=0,connection=dsn)

df_1 = pd.read_sql(sql_query_1,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))

#%%

df_1.head()

# %%
