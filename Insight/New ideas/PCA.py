# https://blog.quantinsti.com/principal-component-analysis-trading/

#%%

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale


# %%

data = pd.read_csv('MarketData.csv')
x = pd.DataFrame(data)
df = x.drop(axis=1,columns=['Date'])
X = df.values
#Normalization of the data
X = scale(X)




# %%


pca = PCA(n_components=9)
pca.fit(X)
factor_loading = pca.components_
df_factor_loading = pd.DataFrame(factor_loading)



# %%



#variance percent of each PC
variance_percent_df = pd.DataFrame(data=pca.explained_variance_)
variance_ratio_df = pd.DataFrame(data=pca.explained_variance_ratio_)
variance_ratio_df = variance_ratio_df * 100


# %%

variance_ratio_df






# %%
