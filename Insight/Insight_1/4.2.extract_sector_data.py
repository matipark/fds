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
manager = 'JPM'

if manager == 'JPM':
    manager_hidden = 'Manager C'
else:
    manager_hidden = 'Manager A'


start_time = time.time()

sql_query_1 = loadsql.get_sql_q('3.2.extract_sector_data.sql',show=0,connection=dsn).format(manager=manager)
df_1 = pd.read_sql(sql_query_1,connection_to_sql)
df_1['as_of_date'] = pd.to_datetime(df_1['as_of_date'], format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))


#%%

#df_1.head()
#df_1.info()

# pull one sector only
# df_1[df_1.sector.eq('Healthcare')] 

# fig, ax = plt.subplots(figsize=(15,7))
# df_1[df_1.style_agg.isin(['Value', 'Growth'])].groupby(['as_of_date','sector']).sum()['net_chg'].unstack().plot(ax=ax, marker='o') # only plot value and growth from dataframe


#%%


start_date = datetime.date(2008, 5, 1)
end_date = datetime.date(2010, 4, 1)

# start_date = datetime.date(2008, 5, 1)
# end_date = datetime.date(2010, 4, 1)

interval = 1

#%%

# Finance
# Telecommunications
# Healthcare
# Utilities
# Technology
# Non-Energy Materials
# Consumer Non-Cyclicals
# Industrials
# Consumer Services
# Energy
# Consumer Cyclicals
# Business Services


style_list = ['Value','Growth']
sector_list = ['Technology','Energy', 'Utilities', 'Consumer Non-Cyclicals', 'Business Services']


# JPM 2020 ['Finance','Healthcare','Technology','Energy','Consumer Cyclicals', 'Business Services']
# JPM 2008 ['Technology','Energy', 'Utilities', 'Consumer Non-Cyclicals', 'Business Services']

# Fidelity 2020 ['Healthcare','Technology', 'Consumer Non-Cyclicals', 'Industrials', 'Consumer Services', 'Business Services']
# Fidelity 2008 ['Healthcare', 'Utilities', 'Non-Energy Materials', 'Consumer Non-Cyclicals', 'Business Services']

# ALL ['Finance','Healthcare','Technology','Energy', 'Utilities', 'Telecommunications', 'Non-Energy Materials', 'Consumer Non-Cyclicals', 'Industrials', 'Consumer Services', 'Consumer Cyclicals', 'Business Services']


df_value = df_1[df_1.style_agg.eq('Value') & df_1.sector.isin(sector_list) & df_1.as_of_date.eq('2009-01-01')][['sector','net_chg']].set_index('sector').rename(columns = {'net_chg':'net_chg_value'})

df_growth = df_1[df_1.style_agg.eq('Growth') & df_1.sector.isin(sector_list) & df_1.as_of_date.eq('2009-01-01')][['sector','net_chg']].set_index('sector').rename(columns = {'net_chg':'net_chg_growth'})


df_comb = pd.concat([df_value, df_growth], axis=1, join="inner")

df_comb['net_final'] = (df_comb['net_chg_value']-df_comb['net_chg_growth']).abs()

df_comb.sort_values(by='net_final', ascending=False)


#%%

# by Sector

def graph(style,sector_list):

    fig, ax = plt.subplots(figsize=(15,7))

    ax.set_title(manager_hidden + ' - ' + style, fontsize=18, fontweight='bold') # title of the plot
    ax.axhline(linewidth=3, color='r') # red color line on y=0

    if start_date > datetime.date(2015, 1, 1):

        ax.axvspan(datetime.date(2020, 2, 1), datetime.date(2020, 5, 1), facecolor ='gray', alpha = 0.5) # gray area for March/2020

    else:
        
        ax.axvspan(datetime.date(2008, 10, 1), datetime.date(2009, 1, 1), facecolor ='gray', alpha = 0.5) # gray area for Sep/2008


    ax.set_xlim([start_date, end_date]) # adjust the x axis to fit the dates available

    #df_1[df_1.style_agg.eq('Value')].groupby(['as_of_date','sector']).sum()['net_chg'].unstack().plot(ax=ax, marker='o') # only plot value and growth from dataframe

    df_1[df_1.style_agg.eq(style) & df_1.sector.isin(sector_list)].groupby(['as_of_date','sector']).sum()['net_chg'].unstack().plot(ax=ax, marker='o') # only plot value and growth from dataframe


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
    plt.legend(ncol = 4, loc ="upper right", title = 'Sector') # place legend
    # plt.text(datetime.date(2019, 5, 1), 2, 'Positive Change', fontsize=14, color='blue', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)) # adding text box
    # plt.text(datetime.date(2019, 5, 1), -6, 'Negative Change', fontsize=14, color='red', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.savefig('{}.png'.format(manager + '_' + style), dpi=100) # store image
    plt.show()

for style in style_list:
    graph(style,sector_list)






#%%


df_1[df_1.style_agg.eq(style) & df_1.sector.isin(sector_list)].groupby(['as_of_date','sector']).sum()['net_chg']




color = ['limegreen', '#bc15b0', 'indigo']
linestyle = ["-","--","-."]

fig, ax = plt.subplots(3,2,squeeze=False,figsize = (8,5))
for x in rows:
    for i,dic in enumerate(dics):
        dic[x].plot(ax=ax[x,i], style=linestyle, color=color, legend=False)
        



for i in sector_list:
    for x in style_list:
        df_1['style_agg']

















# %%

#https://stackoverflow.com/questions/47341018/plotting-pandas-dataframe-subplots-with-different-linestyles

# REFERENCE

# PLOT
# https://scentellegher.github.io/programming/2017/07/15/pandas-groupby-multiple-columns-plot.html
# https://www.geeksforgeeks.org/matplotlib-axes-axes-axhspan-in-python/
# https://stackoverflow.com/questions/22642511/change-y-range-to-start-from-0-with-matplotlib

# PANDAS
# https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.eq.html