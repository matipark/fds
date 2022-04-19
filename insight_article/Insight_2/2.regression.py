#%%

#%%

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



# %%

data = pd.read_csv('20220416_2_sf.csv')
data.head(3)

#%%


data.info(verbose=True)

print(data.shape)


# %%

print(data.isnull().any())

#%%

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(data.dtypes)

# %%

# Feature engineering

data['DATETIME'] = pd.to_datetime(data['DATETIME'])
data = data.set_index('BDX_COMPANY_ID')

#%%


data.head(5)

#%%

pd.set_option('precision', 2)
print(data.describe())


with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(data.describe())

# %%

correlation = data.corr(method='pearson')
columns = correlation.nlargest(10, 'FF_ROCE').index
columns


# %%

correlation_map = np.corrcoef(data[columns].values.T)
sns.set(font_scale=1.0)
heatmap = sns.heatmap(correlation_map, cbar=True, annot=True, square=True, fmt='.2f', yticklabels=columns.values, xticklabels=columns.values)

plt.show()

# %%
