#%%

from re import sub
from docutils import DataError
import pandas as pd
import pyodbc
import time
import warnings

from scipy.fftpack import dstn
import loadsql #functions to load sql queries


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

bdx_board_char_type = 'Overall Board Characteristics'

start_time = time.time()

## excluded nationality 0, gender ratio 100, current date
## only included 'Overall Board Characteristics'

sql_query_1 = loadsql.get_sql_q('1.bdx_sf.sql',show=0,connection=dsn, skipSubsCheck=1).format(bdx_board_char_type=bdx_board_char_type)
with warnings.catch_warnings():
    warnings.simplefilter('ignore', UserWarning)
    df_1 = pd.read_sql(sql_query_1,connection_to_sql)
#df_1['p_date'] = pd.to_datetime(df_1['p_date']).dt.date #, format='%Y-%m-%d')

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# %%


df_1.head(3)


# %%

df_1.info(verbose=True)
print(df_1.shape)


# %%

print(df_1.isnull().any())

# %%

#feature engineering

df_1['DATETIME'] = pd.to_datetime(df_1['DATETIME']) #datetime
data = df_1.set_index('BDX_COMPANY_ID') #company ID as index

data = data.dropna() #subset='FF_ROE'

#%%

#Normalization
#data['FF_ROE']  = [float(i)/sum(data['FF_ROE']) for i in data['FF_ROE']]

# data = data.loc[:, ~data.columns.isin(['DATETIME', 'BDX_ANNUAL_REPORT_DATE', "BDX_BOARD_CHAR_TYPE"])]

# data1 = preprocessing.normalize(data)
# scaled_df = pd.DataFrame(data1, columns = data.columns)
# scaled_df.head()



#%%


rho = data.corr()
pval = data.corr(method=lambda x, y: pearsonr(x, y)[1]) - np.eye(*rho.shape)
p = pval.applymap(lambda x: ''.join(['*' for t in [0.01,0.05,0.1] if x<=t]))
rho.round(2).astype(str) + p



#%%

# Try to show only relevant columns

# data1 = data.loc[:, data.columns.isin(['FF_ROA', 'FF_ROTC', 'FF_DEBT_COM_EQ', 'FF_DEBT_ENTRPR_VAL', 'FF_DEBT_EQ'])]

# rho = data.corrwith(data1)
# pval = data.corrwith(data['FF_ROA'], method=lambda x, y: pearsonr(x, y)[1]) - np.eye(*rho.shape)
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
