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


dsn = 'FDSLoader'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))


#%%


sql_query_1 = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\1.4.1 Retrieve All Participants from Earnings Calls in Past 3 Months.sql',show=0,connection=dsn)

df_1 = pd.read_sql(sql_query_1,connection_to_sql)

df_1.head()


#%%

# excluding people working in the company / finding analysts
analysts = df_1[df_1.person_comp_entity_id!=df_1.factset_entity_id].groupby(['factset_person_id','person_name','person_comp_name','participant_title'])[['event_id','factset_entity_id']].nunique()


analysts.rename(columns={'event_id':'Total Events','factset_entity_id':'Unique Companies'},inplace=True)
analysts.sort_values(['Total Events'],ascending=False).head()


# %%

event_parts = df_1.groupby(['event_id','entity_proper_name','title']).factset_person_id.nunique().sort_values(ascending=False).reset_index().rename(columns={'factset_person_id':'Num Participants'})

event_parts.head()

# %%

event_parts.tail()

#%%

archive_path = 'C:\\Users\\mpark\\OneDrive - FactSet\\Documents\\Loader_app\zips\\tr_history_2020_full_1535'

fund_ticker='SPY-US'
sd = '2018-01-01'
ed = '2018-12-31'

#loadsql is a cover function used to retrieve SQL queries from a directory
sql_query_2 = loadsql.get_sql_q('C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\2.5.1 Retrieving an ETF Universe.sql',show=0,connection=dsn).format(fund = fund_ticker,sd=sd,ed=ed)
univ = pd.read_sql(sql_query_2,connection_to_sql,parse_dates=['startdate','enddate'])

univ.head()


# %%
