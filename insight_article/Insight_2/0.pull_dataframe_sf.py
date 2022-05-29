#%%

import pandas as pd
import pyodbc
import time
import warnings

from scipy.fftpack import dstn
import loadsql #functions to load sql queries

from datetime import datetime
from IPython.display import display

import numpy as np
import pandas as pd
from sklearn import datasets
import seaborn as sns
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from sklearn import preprocessing
from scipy.stats import pearsonr

# %%

# connecting python with SQL 
dsn = 'SF'
connection_to_sql = pyodbc.connect('DSN={dsn_name}'.format(dsn_name = dsn))

# how_many = connection_to_sql.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)
# print(how_many)

#%%

##### May take long time to run & load #####

start_date = {}
end_date = {}

bdx_board_char_type = "\'Overall Board Characteristics\'"
start_date[0] = "\'2017-01-01\'"
end_date[0] = "\'2021-12-31\'"

start_date[1] = "\'2012-01-01\'"
end_date[1] = "\'2016-12-31\'"

start_date[2] = "\'2007-01-01\'"
end_date[2] = "\'2011-12-31\'"


start_time = time.time()

## excluded nationality 0, gender ratio 100, current date
## only included 'Overall Board Characteristics'

## Loading S&P 500 and Russell 3000 Universes

r3000_query = {}
sp500_query = {}
r3000_result = {}
sp500_result = {}

for x in range(len(end_date)):
    r3000_query[x]  = loadsql.get_sql_q('1.bdx_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type,start_date_x=start_date[x], end_date_x=end_date[x])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        r3000_result[x] = pd.read_sql(r3000_query[x],connection_to_sql)


for x in range(len(end_date)):
    sp500_query[x]  = loadsql.get_sql_q('1.bdx_sp50_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type,start_date_x=start_date[x], end_date_x=end_date[x])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        sp500_result[x] = pd.read_sql(sp500_query[x],connection_to_sql)


print("Process finished --- %s seconds ---" % (time.time() - start_time))



# %%

## Verify DataFrame

r3000_result[0].head(10)

# %%

#df_0.info(verbose=True)
#print(df_0.isnull().any())

## Print Shape

for x in range(len(r3000_result)):
    print('r3000 ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date()) + ': ' +str(r3000_result[x].shape))

print('\n')

for x in range(len(sp500_result)):
    print('sp500 ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date()) + ': ' +str(sp500_result[x].shape))


# %%

# feature engineering


data = {}

for x in range(len(r3000_result)):
    r3000_result[x]['DATETIME'] = pd.to_datetime(r3000_result[x]['DATETIME']) #datetime
    r3000_result[x].set_index('BDX_COMPANY_ID', inplace = True) #company ID as index
    r3000_result[x].dropna(subset=['FF_ROE','FF_ROA','FF_ROTC'], inplace = True) #removing Null fields

for x in range(len(sp500_result)):
    sp500_result[x]['DATETIME'] = pd.to_datetime(sp500_result[x]['DATETIME']) #datetime
    sp500_result[x].set_index('BDX_COMPANY_ID', inplace = True) #company ID as index
    sp500_result[x].dropna(subset=['FF_ROE','FF_ROA','FF_ROTC'], inplace = True) #removing Null fields

# verify shape after dropping NAs

for x in range(len(r3000_result)):
    print('r3000 ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date()) + ': ' +str(r3000_result[x].shape))

print('\n')

for x in range(len(sp500_result)):
    print('sp500 ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date()) + ': ' +str(sp500_result[x].shape))


#%%

#Normalization
#data['FF_ROE']  = [float(i)/sum(data['FF_ROE']) for i in data['FF_ROE']]

# data = data.loc[:, ~data.columns.isin(['DATETIME', 'BDX_ANNUAL_REPORT_DATE', "BDX_BOARD_CHAR_TYPE"])]

# data1 = preprocessing.normalize(data)
# scaled_df = pd.DataFrame(data1, columns = data.columns)
# scaled_df.head()


#data_0 = pd.DataFrame(np.random.randint(0,1000,size=(20, 40)))


#%%

# storing stats

r3000_result_stat = {}
sp500_result_stat = {}

for x in range(len(r3000_result)):
    rho = r3000_result[x].corr()
    pval = r3000_result[x].corr(method=lambda i, y: pearsonr(i, y)[1]) - np.eye(*rho.shape)
    p = pval.applymap(lambda i: ''.join(['*' for t in [0.01,0.05,0.1] if i<=t]))
    r3000_result_stat[x] = rho.round(2).astype(str) + p
    r3000_result_stat[x] = r3000_result_stat[x][['FF_ROA','FF_ROE','FF_ROTC']].loc[~r3000_result_stat[x].index.isin(['FF_ROA','FF_ROE','FF_ROTC'])]

for x in range(len(sp500_result)):
    rho = sp500_result[x].corr()
    pval = sp500_result[x].corr(method=lambda i, y: pearsonr(i, y)[1]) - np.eye(*rho.shape)
    p = pval.applymap(lambda i: ''.join(['*' for t in [0.01,0.05,0.1] if i<=t]))
    sp500_result_stat[x] = rho.round(2).astype(str) + p
    sp500_result_stat[x] = sp500_result_stat[x][['FF_ROA','FF_ROE','FF_ROTC']].loc[~sp500_result_stat[x].index.isin(['FF_ROA','FF_ROE','FF_ROTC'])]


#%%

# printing stats

for x in range(len(r3000_result)):
    display(r3000_result_stat[x].style.set_caption('Russell 3000 Year: ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date())))
    
for x in range(len(sp500_result)):
    display(sp500_result_stat[x].style.set_caption('S&P 500 Year: ' + str(datetime.strptime(start_date[x], "'%Y-%m-%d'").date()) + ' - ' + str(datetime.strptime(end_date[x], "'%Y-%m-%d'").date())))


#%%

# output excel

writer = pd.ExcelWriter('correl_results.xlsx',engine='xlsxwriter')   
col = 0
for x in range(len(r3000_result)):
    r3000_result_stat[x].to_excel(writer,sheet_name='r3000',startrow=0 , startcol=col) 
    sp500_result_stat[x].to_excel(writer,sheet_name='sp500',startrow=0 , startcol=col)     
    col = col + len(r3000_result_stat[x].columns) + 2
writer.save()


#%%

# Try to show only relevant columns

# data1 = data.loc[:, data.columns.isin(['FF_ROE','FF_ROA', 'FF_ROTC'])]
# data1

# #%%

# rho = data.corrwith(data1, axis=0)
# pval = data.corrwith(data['FF_ROE'], method=lambda x, y: pearsonr(x, y)[1]) - np.eye(*rho.shape)
# p = pval.applymap(lambda x: ''.join(['*' for t in [0.01,0.05,0.1] if x<=t]))
# rho.round(2).astype(str) + p



# %%

# Correlation map

# data = data.loc[:, ~data.columns.isin(['FF_ROA', 'FF_ROTC', 'FF_DEBT_COM_EQ', 'FF_DEBT_ENTRPR_VAL', 'FF_DEBT_EQ'])]
# correlation = data.corr(method='pearson')
# columns = correlation.nlargest(10, 'FF_ROE').index
# columns


# correlation_map = np.corrcoef(data[columns].values.T)
# sns.set(font_scale=1.0)
# heatmap = sns.heatmap(correlation_map, cbar=True, annot=True, square=True, fmt='.2f', yticklabels=columns.values, xticklabels=columns.values)

# plt.show()

# %%
