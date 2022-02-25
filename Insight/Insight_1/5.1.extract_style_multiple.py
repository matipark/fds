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

# update manager name
manager_list = ['fidelity','blackrock','state_st']
sql_query= {}
df = {}

start_time = time.time()

for i,manager in enumerate(manager_list):
    sql_query[i] = loadsql.get_sql_q('3.1.extract_style_data.sql',show=0,connection=dsn).format(manager=manager)
    df[i] = pd.read_sql(sql_query[i],connection_to_sql)
    df[i]['as_of_date'] = pd.to_datetime(df[i]['as_of_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))


#%%

dates = '2019 - 2021'
start_date = datetime.date(2019, 5, 1)
end_date = datetime.date(2021, 4, 1)

# dates = '2008 - 2010'
# start_date = datetime.date(2008, 5, 1)
# end_date = datetime.date(2010, 4, 1)
interval = 3


#%%

final_df={}

for i in range(len(df)):
    final_df[i] = df[i][df[i].style_agg.isin(['Value', 'Growth'])].groupby(['as_of_date','style_agg']).sum()['net_chg'].unstack()

rows = range(1)

fig, ax = plt.subplots(1,len(final_df),squeeze=False,figsize = (15,4.5))
fig.suptitle(dates)

# set font and rotation for date tick labels
plt.gcf().autofmt_xdate()


for x in rows:
    for i in range(len(final_df)):
        if i == 0:
            manager = 'Manager D'
        elif i == 1:
            manager = 'Manager G'
        else:
            manager = 'Manager Z'
        
        ax[x,i].plot(final_df[i], marker='o', linewidth=1, alpha=1)
        ax[x,i].set_title(manager)
        ax[x,i].axhline(linewidth=2, color='r')
        ax[x,i].set_xlim([start_date, end_date])
        ax[x,i].grid()
        if start_date > datetime.date(2015, 1, 1):

            ax[x,i].axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 5, 1), facecolor ='gray', alpha = 0.5) # gray area for March/2020

        else:
            
            ax[x,i].axvspan(datetime.date(2008, 10, 1), datetime.date(2009, 1, 1), facecolor ='gray', alpha = 0.5) # gray area for Sep/2008
        # set monthly locator
        ax[x,i].xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
        # set formatter
        ax[x,i].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax[x,i].legend(final_df[i], loc ="lower right", title = 'Fund type')

plt.tight_layout()
#plt.savefig('{}.png'.format(dates), dpi=100) # store image
plt.show()


#%%

# https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html