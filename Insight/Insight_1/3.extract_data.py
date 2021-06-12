#%%

import pandas as pd
import pyodbc
import time
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt
import loadsql #functions to load sql queries


# %%

# connecting python with SQL 
dsn = 'FDSServer'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))


#%%

manager = 'fidelity'

start_time = time.time()

sql_query_1 = loadsql.get_sql_q('3.extract_data.sql',show=0,connection=dsn).format(manager=manager)
df_1 = pd.read_sql(sql_query_1,connection_to_sql)

print("Process finished --- %s seconds ---" % (time.time() - start_time))


#%%

df_1.head()
#df_1.info()

# only taking Value and Growth types
#df_1[df_1.style_agg.isin(['Value', 'Growth'])]



# %%


# lines = df_1[df_1.style_agg.isin(['Value', 'Growth'])].groupby('style_agg').plot.line(y='net_chg', x='as_of_date')
# lines = df_1[df_1.style_agg.isin(['Value', 'Growth'])].plot.line(y='net_chg', x='as_of_date')



fig, ax = plt.subplots(figsize=(15,7))

ax.set_title(manager, fontsize=18, fontweight='bold') # title of the plot
ax.axhline(linewidth=3, color='r') # red color line on y=0
ax.axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 5, 1), facecolor ='gray', alpha = 0.5) # gray area for March/2020
ax.set_xlim([datetime.date(2019, 2, 1), datetime.date(2021, 5, 1)]) # adjust the x axis to fit the dates available

df_1[df_1.style_agg.isin(['Value', 'Growth'])].groupby(['as_of_date','style_agg']).sum()['net_chg'].unstack().plot(ax=ax, marker='o') # only plot value and growth from dataframe

ax.set_xlabel('')
ax.set_ylabel('net change', fontsize=12)

# set monthly locator
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
# set font and rotation for date tick labels
plt.gcf().autofmt_xdate()
plt.grid(which='major') # add background grid
plt.legend(loc ="lower right", title = 'Fund type') # place legend
plt.text(datetime.date(2019, 5, 1), 30, 'Positive Change', fontsize=14, color='blue', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.text(datetime.date(2019, 5, 1), -30, 'Negative Change', fontsize=14, color='red', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.savefig('{}.png'.format(manager), dpi=100)
plt.show()


# %%