#pip install pycoingecko
from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import datetime
import time
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from tensorflow.keras import layers
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()
cg = CoinGeckoAPI()
cg.ping()

def initial_data_call(coinname):
  t_data = cg.get_coin_market_chart_by_id(coinname , vs_currency = 'USD' , days = '85')
  prices_t = pd.DataFrame(t_data['prices'])
  prices_t.rename(columns={0:'Time', 1 : 'prices'}, inplace =True)
  prices_t['Time'] = prices_t['Time'].floordiv(1000)
  prices_t = prices_t[2:]
  prices_t=prices_t.reset_index()
  prices_t.drop('index',1,inplace=True)
  prices_t = prices_t.iloc[:,1]
  length = prices_t.size
  length=length-1
  prices_t=prices_t[length-2016:-1]
  return prices_t,prices_t


def predict_run(prices_t, newmodel):
  hist2 = np.array(prices_t)
  hist2 = hist2.reshape(-1, 1)
  sc = MinMaxScaler()
  hist_scaled2 = sc.fit_transform(hist2)
  hist_scaled2 = hist_scaled2.reshape(-1, 2016, 1)
  newpred = newmodel.predict(hist_scaled2)
  #newpred+=0.1
  newpred = newpred.reshape(-1)
  hist_scaled2 = hist_scaled2.reshape(-1)
  hist_scaled2 = np.append(hist_scaled2, newpred, axis=0)
  hist_scaled2 = hist_scaled2[1:]
  newpred.reshape(1, 1)
  newpred = [newpred]
  val = sc.inverse_transform(newpred)
  val = val[0][0]

  return val

def append_prediction(store_price,val):
  store_price=store_price.to_frame()
  data = {'prices' : [val]}
  temp_df = pd.DataFrame(data)
  store_price=store_price.append(temp_df)
  store_price.reset_index(inplace=True)
  store_price.drop('index',1,inplace=True)  
  store_price.drop([0],axis=0,inplace=True)
  store_price.reset_index(inplace=True)
  store_price.drop('index',1,inplace=True) 
  return store_price,temp_df

def append_prediction2(store_price,val):
  store_price=store_price
  data = {'prices' : [val]}
  temp_df = pd.DataFrame(data)
  store_price=store_price.append(temp_df)
  store_price.reset_index(inplace=True)
  store_price.drop('index',1,inplace=True)  
  store_price.drop([0],axis=0,inplace=True)
  store_price.reset_index(inplace=True)
  store_price.drop('index',1,inplace=True) 
  return store_price,temp_df

def run(coinname):
    newmodel = tf.keras.models.load_model(f'{coinname}.h5')
    prices_t,store_price=initial_data_call(coinname)
    predicted_df = pd.DataFrame()
    val = predict_run(prices_t,newmodel)
    prices_t,temp_df = append_prediction(prices_t,val)
    predicted_df=predicted_df.append(temp_df)
    for count in range(50): #336
        val = predict_run(prices_t,newmodel)
        prices_t,temp_df = append_prediction2(prices_t,val)
        predicted_df=predicted_df.append(temp_df)
    hist2 = np.array(prices_t)
    hist2 = hist2.reshape(-1, 1)
    sc = MinMaxScaler()
    hist_scaled2 = sc.fit_transform(hist2)
    hist_scaled2 =hist_scaled2[-50:]
    df=pd.DataFrame(hist_scaled2)
    df.to_csv(f'{coinname}.csv')

    







#prices_t
   # predicted_df=predicted_df.reset_index()
    #predicted_df.drop('index',1,inplace=True)
    #hist2 = np.array(prices_t)
    #hist2 = hist2.reshape(-1, 1)
    #sc = MinMaxScaler()
    #hist_scaled2 = sc.fit_transform(hist2)
    #hist_scaled2 =hist_scaled2[-50:]
    #predicted_df.to_csv('bitcoindata.csv') 
    

#prices with historical data and predicted

#can be saved as .csv


#prices predicted as ratio #this is impt