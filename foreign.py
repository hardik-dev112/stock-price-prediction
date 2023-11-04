import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf
from keras.models import load_model
import streamlit as st
import plotly.express as px
from stocknews import StockNews 
import requests
import nltk
import mysql.connector
import mplfinance as mpf
import plotly.graph_objects as go
from datetime import datetime 

st.title('Foreign stock Prediction')

ticker= st.text_input('Enter stock ticker','AAPL')
start_date =st.date_input('Start date')
end_date = st.date_input('End date')

df = yf.download(ticker, start=start_date, end= end_date)
fig = px.line(df, x=df.index, y= df['Close'], title = ticker )
st.plotly_chart(fig)


#Describing Data
st.write(df.describe())


princing_data,fundamental_data, news, chart_analysis, openai1 = st.tabs(['Princing Data',"fundamental_data", "Top 10 news", "Chart Analysis", "chatgpt"])

with princing_data:
    st.header("Price Movement")
    st.write(df)




from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    
    key= 'CR0NM5AZ00OG5TFD'
    fd =FundamentalData(key,output_format ='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0] #ticker are change with the selected_stocks
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)

    st.subheader('Income Statment')
    income_statement = fd.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns =list(income_statement.T.iloc[0])
    st.write(is1)

    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)


from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker , save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')


with chart_analysis:
    st.header("Charts")
    st.subheader('Candle chart')
   
    # Create the candlestick chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))


    # Display the candlestick chart in Streamlit
    st.plotly_chart(fig)
    
    
    
    
    st.subheader('Closing price vs Time Chart')
    fig =plt.figure(figsize=(12,6))
    plt.plot(df.Close)
    st.pyplot(fig)



    st.subheader('Closing prive Vs Time chart with 100 MA')
    ma100 = df.Close.rolling(100).mean()
    fig =plt.figure(figsize=(12,6))
    plt.plot(ma100)
    plt.plot(df.Close)
    st.pyplot(fig)


    st.subheader('Closing prive Vs Time chart with 100 MA & 200 MA')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig =plt.figure(figsize=(12,6))
    plt.plot(ma100, 'r')
    plt.plot(ma200,'g')
    plt.plot(df.Close, 'b')
    st.pyplot(fig)


#spliting data into training and testing 

    data_training =pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing  =pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

    print(data_training.shape)
    print(data_testing.shape)



    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0,1))

    data_training_array =scaler.fit_transform(data_training)



    #load my model
    model = load_model('keras_model.h5')

    #testing part
    past_100_days = data_training.tail(100)
    final_df = past_100_days.append(data_testing , ignore_index = True)
    input_data = scaler.fit_transform(final_df)

    x_test =[]
    y_test = []
    for i in range (100, input_data.shape[0]):
        x_test.append(input_data[i-100: i])
        y_test.append(input_data[i, 0])

    x_test , y_test = np.array(x_test), np.array(y_test)
    y_predicted = model.predict(x_test)
    scaler = scaler.scale_

    scale_factor =1/scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor 


    st.subheader('Prediction Vs actual')
    fig2 = plt.figure(figsize=(12,6))
    plt.plot(y_test, 'b', label = 'Orginal price')
    plt.plot(y_predicted, 'r', label =' predicated price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)

from pyChatGPT import ChatGPT
session_token ='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..wt5hVikYwMehGD5Z.qOXGOI6OhJSflhM79I0Pm8qcEMHKrd--QrZUP5pWSdP3aQiIke__FlNXab97_wU4c9tn-lFFPl8M3pmHDThbtq6tyuN9K4vA2fz3jsNo1NeDc6U8XG7nBy0p25qTT26EHpW1yRQhPuLGC7kfkPXnrWh4655Tf9emSIXquH73YZnKJwwC8_qQWGMEfzJLkCtq1NoAR7zAq_WGSCOak2kX8sciP4l_PRMAl-o3ExplNM_2-To3zn2KKEFuWxXuV0OeMzMYMoZ0v2_fnwPYwVUQX80S_9bEnPa9M4Y5Wj2JXVWnHWx3OXTck4fFPwV-y2ZbADWEs2mAMcbQ3Ixsy6CNvJBC5IxazNbjAnrHtYjLEi-Wu3-yyHfC-OCe5Ys8A0eOeCgLSO0BLZXc5t6wh7oJZoa_IEpo2QgpxH2Uq5xQpcaaVgesBcw0SQ54uu3sopogfTxMX23tC3ZGtmzw8h_c5904hsnveiRUlqXbaXz_SZu2gPdl4N40g0WEWGOtTWyK0JKuFO3oq_guQg4gAgEWF0A7NJQHOv2WCtBs_6zVHCZaIipZrI_EUZWHj0WapF8SgN-faDnbisTfdug3H5OkUdomDq3SucGyQOHjA4L1MGqdVusQ1lM30kPUYivCRem1PXWpF4rs0zUO_QwTNAl3CHziDM4qLSCUxdNpKOmmtlaIAoSdwYAWkhOb0pFLHn0oJ3BFI5MDC5GK7IUBhj97LZWbYHuPiwmJZ0eXoytC6ExIutNyZvqlBmGkoW69uWV9Do89uyO0VTxpW21ioHIOtEFjgBXzUjmX4AdSzv6oLVOq8H7_zarT9O2Ss1cUFkpTFhHLTahrQhY8rvl-jFFql9cHxD18ecmZ7oL00qNMPjuLQqbhXvL1EnpmVKg9o9DHm4z-8q_JWCQ2_tYoS6AQGT2nK5tR9vz-TOg20aybBTwE4PZz_T8gElAYLpc4SXO2it6IS54Jlu6-ka6aRK627oSnZ73PPUVLL_apXLGiAXFrrkvSWagZNdOxF-VS5iXx02EDO6760on_NNl2Ekx3ZlLPrNeauGUdbSAdlv4wova16om4f62TOJ24iQtnb_svp8DmU4blCivkHJnrpH8ApN-oFcVC4MF-O86-4TeU__nm0jr_8yE2o4HRo3tiRePY9iXFSr7nrIAWmqfBSntSateMrNwrvdUUi1MmK8O3JZoKF9P4z8pYVhjRZMLngk1FEUIcG6Ln7tZTkF9EUfNHunWVnw7xsQ3rOL5ypmgBHt2XgsyShCoEn-sYsTowg7X65_CvSbLOO_zsY6Y5gmM-eF9tyQEWdxZeyShZJsE8xQy7Rj1Lb7NxwSzVBfCReoYWHF0XUa9dmO7tf20mciq5l5O1HrCcVdAW1238mOyyK5qz4RU6VPsYOV2rBg0qhVd3gF2Ec7log_jNbUHK5nAtzDySsdUyzrNDf2wM1DE9C3lj0gSFeqF8h9F145rgV_jyyQNj7zOwC8VJ36vcmy6Ju3vs76t-Mg7heP2YvODofAYn7pCm9LlQN82bnIqshGy6Ec3xKGHVNfNpO_a7Ac7elgWukpQBzM7IP7hIWuscmtnjbidXxEmwcW4il8FDpBL8QMn37z3fSOeBabGfGBI2xH_XqVQqpkugGaEUZP6vGcvS71E0Hls5snZzdzOS0MxOUbywvoKRHx5-0W35bAXfkHSqAKXj526lSduPFXotqI2yzjosNbiVk4m0zOvOWgCeTTIPwSf1WLd8SyYKBXeizH5D5XIF_IJ5aueQr8x2aVSk4GB0CkME5yijZu0iWqOLV1kA5snUK5H7OwmcYSle1uOLhNfu4ey6_3FuSwiUMs6xEE1TJP0smPcBDDBUUngbQyQWtKT5PpRlktVH9AV6UKlNtoA4MW4XpLT-WFjvLvm6S_d8wlZuhMCgg8afs2iUKe7xfz1It17IFNUYyf59YsKsyFo7dVgtlgMQJtCA-GPAqJvq8dUbkIV0k49iuUxdKL9sqc7aoShqFwcpztXVsMpFAXDuNHzGUn6iCxeB-SXcoXA0d7uema291Wy70ZNVXqWv6k-2_soA1CctE45Jn1N7D0-RMhvC7W-vqdXTYfr5UJBWmb1J35fcAgayKuJwGs17uHsHBp2exayINj0QxBi6-2mYLTu2NjhMMPCPRSGHNClCllHpTf65cs39re8C2PlEQEjdRzu3PNN7N9RyR01yttg-8ojNFBiKPgd6GVsDOKiId5FVETT1_1vbesKj042b0l4dVTvKWspx509X1G0QzBPW73nJgIQ0ZCBdqRuhhmvDq05KIz5eOf6p24VfyDUaHdcxFiufwT1PHOeGq80ha8Uarwn99EJ4DKmDH9ZZrnEo4fZC1-cLHg9rkynyR-nsG9TUEuxdPxSfdRAC7AMNg718c-eFtdftJyIzc6X1_aagCvQ9ptidm0ySbxxtS8wsjJECWeeGeoj2cndFIZ16IRdrpcFSsotYG_p8EcQqMn_FzG3OSZPia9itfFD7fOiP0d3vTRWMiXFJ7LxQ6Pb77q4vX7ABkWPngXhvuuI0QdlQ27qy9nPEdkSjtt8MuMsWPpcRhybu0X0YAbKROiZGkemiB7JMAYxtb3T52akmCrBBfaKXeqcDvpWhX4D1ZXjXjmj9Zny6_SqOwBHcb3InjgnsBt_ZncD9tHHjZgR-MOgAXFMPRcyxB_Sr9tr0_LxMcXAfS4f0rdQDgiPkGdYGxjAc5cwigk0Xbf7vuyMnheSh7zJGqdZkFLbYKzs8nUYztY_hcwTap5ueOs6LBtLBHO7Y.EPtD4o2agIxMVF8Dsip7kA'
api2 = ChatGPT(session_token)
buy = api2.send_message(f'3 Reasons to buy {ticker} stock')
sell = api2.send_message(f'3 Reasons to sell {ticker} stock')
swot = api2.send_message(f'SWOT analysis of {ticker} stock')


with openai1:
    buy_reason, sell_reason, swot_analysis = st.tabs (['3 Reasons to buy ', '3 Reasons to sell', 'SWOT analysis' ])

    with buy_reason:
        st.subheader(f'3 reasons on why to buy {ticker} Stock')
        st.write(buy ['message'])

    with sell_reason:
        st.subheader(f'3 reasons on why to sell {ticker} Stock')
        st.write(sell ['message'])

    with swot_analysis:
        st.subheader(f'SWOT Analysis of  {ticker} Stock')
        st.write(swot ['message'])

