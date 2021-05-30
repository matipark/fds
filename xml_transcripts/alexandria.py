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
dsn = 'FDSLoader'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

sql_path = 'C:\\Github_repo\\Notes\\FDS\\xml_transcripts\\'

#%%

start_time = time.time()

# classify calls by type
sql_query_1 = loadsql.get_sql_q(os.path.join(sql_path,'4.1.1 Call Types and Counts.sql'),show=0,connection=dsn)

ct = pd.read_sql(sql_query_1,connection_to_sql, index_col ='actr_call_type')

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# %%

ct.head(15)

#%%

# start_time = time.time()

# # Input a start and end date call event range.
# start_date = '2020-01-01'
# end_date = '2020-12-31'

# # average sentiment by country 
# sql_query_2 = loadsql.get_sql_q(os.path.join(sql_path,'4.1.2 Average Sentiment by Country.sql'),show=0,connection=dsn).format(start_date = start_date, end_date = end_date)

# acc = pd.read_sql(sql_query_2,connection_to_sql, index_col ='actr_country_name')

# print("Process finished --- %s seconds ---" % (time.time() - start_time))


# # %%

# acc.head(10)

#%%

# list of topics discussed in the calls

sql_query_3 = loadsql.get_sql_q(os.path.join(sql_path,'4.1.3 Topic Map.sql'),show=0,connection=dsn)

tm = pd.read_sql(sql_query_3,connection_to_sql, index_col ='actr_topic')
tm.head(25)

# %%

start_time = time.time()
 
ticker = 'FDS-US'
call_type = 'Earnings Call'
start_date = '2020-01-01'
end_date = '2020-12-31'

# tagging events in the call
sql_query_4 = loadsql.get_sql_q(os.path.join(sql_path,'4.1.4 Ticker Event Selection.sql'),show=0,connection=dsn).format(ticker=ticker,call_type=call_type, start_date = start_date, end_date = end_date)

tcc = pd.read_sql(sql_query_4,connection_to_sql, index_col ='actr_call_time')


print("Process finished --- %s seconds ---" % (time.time() - start_time))


# %%

# pull the list of conversations with tag
tcc[['ticker_region','actr_name','actr_affiliation','actr_section','actr_topic',
     'actr_topic_desc','actr_prob_pos','actr_prob_ntr','actr_prob_neg']].head(5)

#%%

# topic_count = tcc.groupby(by=['actr_topic_desc', 'actr_topic']).agg({'actr_topic_count':'sum', 'actr_prob_pos':'mean', 'actr_prob_neg':'mean', 'actr_prob_ntr':'mean'}).sort_values(by='actr_topic_count',ascending=False)

# topic_count.head(10)


# %%

# Select two topics from the actr_topic hierarchical categories in the table above
topic1 = 'ERN/REV' #Earnings
topic2 ='COV' #COVID

#Create a new column to flag topics that role up to the topics selected above
tcc['topic_category'] = pd.np.where(tcc.actr_topic.str.startswith(topic1),topic1,pd.np.where(tcc.actr_topic.str.startswith(topic2),topic2,'NA'))

#Filter to only transcript sections about the selected topics
topic_sent = tcc[tcc['topic_category']!='NA']

#Aggegate statistics for each topic category and earnings call
topic_sent = topic_sent.groupby(by=['actr_call_time','topic_category']).agg({'actr_topic_count':'sum','actr_prob_pos':'mean','actr_prob_neg':'mean','actr_prob_ntr':'mean'})

#calculate net sentiment for each earnings call and topic
topic_sent['net_sentiment'] = (1-topic_sent['actr_prob_ntr'])*(np.log10((topic_sent['actr_prob_pos']+.01)/(topic_sent['actr_prob_neg']+.01)))

topic_sent

# %%

ax = topic_sent.actr_topic_count.unstack().plot(kind='bar',figsize=(10,7))
#ax.set_facecolor("black")
ax.set_title('Number of Times Topics was Mentioned')
ax.set_ylabel('Topic Count')
ax.set_xlabel('Date of Earnings Call')

ax = topic_sent.net_sentiment.unstack().plot(kind='bar',figsize=(10,7))
ax.set_title('Net Sentiment of Topic')
ax.set_ylabel('Net Sentiment')
ax.set_xlabel('Date of Earnings Call')

plt.show()

# %%
