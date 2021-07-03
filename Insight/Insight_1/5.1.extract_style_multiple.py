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
manager_list = ['fidelity','blackrock']
sql_query= {}
df = {}

start_time = time.time()

for i,manager in enumerate(manager_list):
    sql_query[i] = loadsql.get_sql_q('3.1.extract_style_data.sql',show=0,connection=dsn).format(manager=manager)
    df[i] = pd.read_sql(sql_query[i],connection_to_sql)
    df[i]['as_of_date'] = pd.to_datetime(df[i]['as_of_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))


#%%

start_date = datetime.date(2019, 5, 1)
end_date = datetime.date(2021, 4, 1)

# start_date = datetime.date(2008, 5, 1)
# end_date = datetime.date(2010, 4, 1)
interval = 1
position_pos = 40
position_neg = 40

#%%

a={}


for i in range(len(df)):
    a[i] = df[i][df[i].style_agg.isin(['Value', 'Growth'])].groupby(['as_of_date','style_agg']).sum()['net_chg'].unstack()

rows = range(2)
dics = range(2)

def set_cycler(ax):
    ax.set_prop_cycle(plt.cycler('color', ['limegreen', '#bc15b0', 'indigo'])+
                      plt.cycler('linestyle', ["-","--","-."]))

fig, ax = plt.subplots(2,2,squeeze=False,figsize = (8,5))
fig.suptitle('Manager A')

# set font and rotation for date tick labels
plt.gcf().autofmt_xdate()


#plt.legend(loc ="lower right", title = 'Fund type') # place legend

for x in rows:
    for i in range(len(a)):
        set_cycler(ax[x,i])
        
        ax[x,i].plot(a[i], marker='o', linewidth=1, alpha=1)
        ax[x,i].set_title(manager)
        ax[x,i].set_xlim([start_date, end_date])
        ax[x,i].grid()
        ax[x,i].axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 5, 1), facecolor ='gray', alpha = 0.5)
        # set monthly locator
        ax[x,i].xaxis.set_major_locator(mdates.MonthLocator(interval=5))
        # set formatter
        ax[x,i].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

plt.show()


#%%

df_2 = df_1[df_1.style_agg.isin(['Value', 'Growth']) & (end_date >= df_1['as_of_date']) & (df_1['as_of_date'] >= start_date)]

df_2



# %%

# shorter version

fig, ax = plt.subplots(figsize=(15,7))

ax.set_title(manager_hidden, fontsize=18, fontweight='bold') # title of the plot
ax.axhline(linewidth=3, color='r') # red color line on y=0

if start_date > datetime.date(2015, 1, 1):

    ax.axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 5, 1), facecolor ='gray', alpha = 0.5) # gray area for March/2020

else:
    
    ax.axvspan(datetime.date(2008, 10, 1), datetime.date(2009, 1, 1), facecolor ='gray', alpha = 0.5) # gray area for Sep/2008


ax.set_xlim([start_date, end_date]) # adjust the x axis to fit the dates available

df_1[df_1.style_agg.isin(['Value', 'Growth'])].groupby(['as_of_date','style_agg']).sum()['net_chg'].unstack().plot(ax=ax, marker='o') # only plot value and growth from dataframe

ax.set_xlabel('')
ax.set_ylabel('net change', fontsize=12)

# set monthly locator
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
# set font and rotation for date tick labels

plt.tight_layout()
plt.gcf().autofmt_xdate()
plt.grid(which='major') # add background grid
plt.legend(loc ="lower right", title = 'Fund type') # place legend

if start_date > datetime.date(2015, 1, 1):
    plt.text(datetime.date(2019, 7, 1), position_pos, 'Positive Change', fontsize=14, color='blue', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)) # adding text box
    plt.text(datetime.date(2019, 7, 1), -position_neg, 'Negative Change', fontsize=14, color='red', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

else:
    plt.text(datetime.date(2008, 7, 1), position_pos, 'Positive Change', fontsize=14, color='blue', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)) # adding text box
    plt.text(datetime.date(2008, 7, 1), -position_neg, 'Negative Change', fontsize=14, color='red', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


#plt.savefig('{}.png'.format(manager), dpi=100) # store image
plt.show()

#%%

# https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
# https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html
