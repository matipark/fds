
# https://www.theanalysisfactor.com/the-fundamental-difference-between-principal-component-analysis-and-factor-analysis/
# https://towardsdatascience.com/stock-market-analytics-with-pca-d1c2318e3f0e
# https://github.com/gylx/Financial-Machine-Learning-Articles/blob/master/Stock%20Market%20Analytics%20with%20PCA.ipynb

# https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html#:~:text=Choosing%20the%20number%20of%20components,pca%20%3D%20PCA().


#%%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import bs4 as bs
import requests
from sklearn.decomposition import PCA

# %%
plt.style.use('fivethirtyeight')
# %%
def save_sp500_tickers():

    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'html')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        if not '.' in ticker:
            tickers.append(ticker.replace('\n',''))
        
    return tickers

tickers = save_sp500_tickers()
# %%
prices = yf.download(tickers, start='2020-01-01')['Adj Close']
# %%
rs = prices.apply(np.log).diff(1)
# %%
rs.plot(legend=0, figsize=(10,6), grid=True, title='Daily Returns of the Stocks in the S&P500')
plt.tight_layout()
plt.savefig('tmp.png')
# %%
(rs.cumsum().apply(np.exp)).plot(legend=0, figsize=(10,6), grid=True, title='Cumulative Returns of the Stocks in the S&P500')
plt.tight_layout()
plt.savefig('tmp.png')
# %%

pca = PCA(1).fit(rs.fillna(0))
# we set 1 as a component because that would be the weight

pc1 = pd.Series(index=rs.columns, data=pca.components_[0])

# pc2= pd.Series(index=rs.columns, data=pca.components_[1])



pc1.plot(figsize=(10,6), xticks=[], grid=True, title='First Principal Component of the S&P500')
plt.tight_layout()
plt.savefig('tmp.png')

# %%


weights = abs(pc1)/sum(abs(pc1))
myrs = (weights*rs).sum(1)
myrs.cumsum().apply(np.exp).plot()




