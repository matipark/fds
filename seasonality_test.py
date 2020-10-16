#%%

# https://towardsdatascience.com/analysis-of-stock-market-cycles-with-fbprophet-package-in-python-7c36db32ecd0
# https://barrypan.github.io/Fbprophet_ANA/Final_Analysis.html


# Import libraries
import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta


# import Content API libraries
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from pandas.io.json import json_normalize

# import ML libraries
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error


# %%

# Data to pull content API

ids = "SP50"

authorization = ('FDS_DEMO_FE-410734','06LE9ERlxk7vS5AIwHFmThwJo0oX6ojGUUDVthEg')
prices_endpoint = 'https://api.factset.com/content/factset-prices/v1/prices'


prices_request ={
  "ids": [ids],
  "startDate": "2018-01-01",
  "endDate": "2019-03-30",
  "frequency": "D",
  "calendar": "FIVEDAY",
  "currency": "LOCAL",
  "adjust": "SPLIT"
}
headers = {'Accept': 'application/json','Content-Type': 'application/json'}

# %%

# Pull Content API data and sort 

prices_post = json.dumps(prices_request)
prices_response = requests.post(url = prices_endpoint, data=prices_post, auth = authorization, headers = headers, verify= False )
print('HTTP Status: {}'.format(prices_response.status_code))
prices_data = json.loads(prices_response.text)
prices_df = json_normalize(prices_data['data'])

# Convert Date format & Index it

prices_df["date"] = pd.to_datetime(prices_df["date"])
prices_df.set_index("date", inplace=True)


# print('COLUMNS:')
# print('')
# print(prices_df.dtypes)
# print('')
print('Total No. of records:',len(prices_df))


#%%

# Test data
prices_df[["price","priceOpen","priceHigh","priceLow","volume"]].tail()


# %%


prices_df[['price']].plot(figsize=(16,8),color='#002699',alpha=0.8)
plt.xlabel("date",fontsize=12,fontweight='bold',color='gray')
plt.ylabel('price',fontsize=12,fontweight='bold',color='gray')
plt.title("Stock price for {}".format(ids),fontsize=18)
plt.show()

#%%

def cycle_analysis(data,split_date,cycle,mode='additive',forecast_plot = False,print_ind=False):
    training = data[:split_date].iloc[:-1,]
    testing = data[split_date:]
    predict_period = len(pd.date_range(split_date,max(data.index)))
    df = training.reset_index()
    df.columns = ['ds','y']
    m = Prophet(weekly_seasonality=False,yearly_seasonality=False,daily_seasonality=False)
    m.add_seasonality('self_define_cycle',period=cycle,fourier_order=8,mode=mode)
    m.fit(df)
    future = m.make_future_dataframe(periods=predict_period)
    forecast = m.predict(future)
    if forecast_plot:
        m.plot(forecast)
        plt.plot(testing.index,testing.values,'.',color='#ff3333',alpha=0.6)
        plt.xlabel('Date',fontsize=12,fontweight='bold',color='gray')
        plt.ylabel('Price',fontsize=12,fontweight='bold',color='gray')
        plt.show()
    ret = max(forecast.self_define_cycle)-min(forecast.self_define_cycle)
    model_tb = forecast['yhat']
    model_tb.index = forecast['ds'].map(lambda x:x.strftime("%Y-%m-%d"))
    out_tb = pd.concat([testing,model_tb],axis=1)
    out_tb = out_tb[~out_tb.iloc[:,0].isnull()]
    out_tb = out_tb[~out_tb.iloc[:,1].isnull()]
    mse = mean_squared_error(out_tb.iloc[:,0],out_tb.iloc[:,1])
    rep = [ret,mse]
    if print_ind:
        print ("Projected return per cycle: {}".format(round(rep[0],2)))
        print ("MSE: {}".format(round(rep[1],4)))
    return rep



# %%

cycle_analysis(prices_df['price'],'2019-01-01',30,forecast_plot=True,print_ind=True)

# %%
