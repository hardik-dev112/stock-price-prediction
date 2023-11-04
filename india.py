
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
import datetime as dt
import mplfinance as mpf
import plotly.graph_objects as go
from bokeh.plotting import figure,column
import talib as ta

#@st.cache_data

st.set_page_config(layout="wide" , page_title='Indian Stock Prediction')

# ticker= st.sidebar.text_input('Enter stock ticker','SBIN.NS')
# start_date =st.sidebar.date_input('Start date')
# end_date = st.sidebar.date_input('End date')

ticker= st.text_input('Enter stock ticker','SBIN.NS')
start_date =st.date_input('Start date')
end_date = st.date_input('End date')

df = yf.download(ticker, start=start_date, end= end_date)
fig = px.line(df, x=df.index, y= df['Close'], title = ticker )
st.plotly_chart(fig)


#Describing Data
st.write(df.describe())

#ticker= ('') #new line
#dropdown = st.multiselect('pick your stock', ticker) #new line
#selected_stocks = st.sidebar.multiselect('Pick your stock', ticker)


# if len(selected_stocks)>0: #new line
#     df = yf.download(selected_stocks, start=start, end=end) ['Close']
#     st.line_chart(df)
    
# #if len(selected_stocks)>0: #new line two times because i want to show all the high low open etc
# df = yf.download(selected_stocks, start=start, end=end) 
# print(df)


    

princing_data, chart_analysis, openai1 = st.tabs(['Princing Data',"Chart Analysis", "chatgpt"])




with princing_data:
    st.header("Price Movement")
    st.write(df)

  


with chart_analysis:
    st.header("Charts")
    st.subheader('Candle chart')
   





# Calculate support and resistance levels
    df['Support'] = df['Close'].rolling(window=30).min()
    df['Resistance'] = df['Close'].rolling(window=30).max()

    # Plot using mplfinance
    fig, axes = mpf.plot(df, addplot=[mpf.make_addplot(df['Support'], panel=0, color='green', linestyle='dashed'),
                                   mpf.make_addplot(df['Resistance'], panel=0, color='red', linestyle='dashed')],
                   type='candle', style='yahoo', returnfig=True)
    
    st.write(fig)

    
    
    # Create the candlestick chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))

    # Display the candlestick chart in Streamlit
    st.plotly_chart(fig)


     # st.subheader('Closing price vs Time Chart')
    # fig =plt.figure(figsize=(12,6))
    # plt.plot(df.Close)
    # st.pyplot(fig)



    # Add 44-day moving average
    st.subheader('Closing Price vs  44-day MA')
    ma44 = df['Close'].rolling(44).mean()

    # Create a new figure for the chart with the moving average
    fig_ma = plt.figure(figsize=(12, 6))
    plt.plot(ma44, label='44-day MA', color='red')
    plt.plot(df['Close'], label='Closing Price', color='blue')
    plt.legend()

    # Display the figure in Streamlit
    st.pyplot(fig_ma)




    # Add 8-day moving average
    st.subheader('Closing Price vs Time chart with 8-day MA')
    ma8 = df['Close'].rolling(8).mean()

    # Create a new figure for the chart with the moving average
    fig_ma = plt.figure(figsize=(12, 6))
    plt.plot(ma8, label='8-day MA', color='red')
    plt.plot(df['Close'], label='Closing Price', color='blue')
    plt.legend()

    # Display the figure in Streamlit
    st.pyplot(fig_ma)




    # Add 44-day and 8-day moving averages
    st.subheader('Closing Price vs Time chart with Moving Averages')
    ma44 = df['Close'].rolling(44).mean()
    ma8 = df['Close'].rolling(8).mean()

    # Create a new figure for the chart with the moving averages
    fig_ma = plt.figure(figsize=(18, 9))
    plt.plot(ma44, label='44-day MA', color='red')
    plt.plot(ma8, label='8-day MA', color='orange')
    plt.plot(df['Close'], label='Closing Price', color='green')
    plt.legend()

    # Display the figure in Streamlit
    st.pyplot(fig_ma)






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


    
    st.subheader('Closing prive Vs Time chart with 44 MA & 8 MA')
    ma44 = df.Close.rolling(44).mean()
    ma8= df.Close.rolling(8).mean()
    fig =plt.figure(figsize=(12,6))
    plt.plot(ma44, 'r')
    plt.plot(ma8,'g')
    plt.plot(df.Close, 'b')
    st.pyplot(fig)



    
    
    # Define a function to calculate RSI
    def calculate_rsi(data, window=14):
        delta = data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi


    # Calculate RSI with default window of 14 days
    df['RSI'] = calculate_rsi(df)

    # Print the DataFrame with RSI values
    print(df[['Close', 'RSI']])




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



from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

driver = webdriver.Chrome(ChromeDriverManager().install())


from pyChatGPT import ChatGPT
#session_token ='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..wt5hVikYwMehGD5Z.qOXGOI6OhJSflhM79I0Pm8qcEMHKrd--QrZUP5pWSdP3aQiIke__FlNXab97_wU4c9tn-lFFPl8M3pmHDThbtq6tyuN9K4vA2fz3jsNo1NeDc6U8XG7nBy0p25qTT26EHpW1yRQhPuLGC7kfkPXnrWh4655Tf9emSIXquH73YZnKJwwC8_qQWGMEfzJLkCtq1NoAR7zAq_WGSCOak2kX8sciP4l_PRMAl-o3ExplNM_2-To3zn2KKEFuWxXuV0OeMzMYMoZ0v2_fnwPYwVUQX80S_9bEnPa9M4Y5Wj2JXVWnHWx3OXTck4fFPwV-y2ZbADWEs2mAMcbQ3Ixsy6CNvJBC5IxazNbjAnrHtYjLEi-Wu3-yyHfC-OCe5Ys8A0eOeCgLSO0BLZXc5t6wh7oJZoa_IEpo2QgpxH2Uq5xQpcaaVgesBcw0SQ54uu3sopogfTxMX23tC3ZGtmzw8h_c5904hsnveiRUlqXbaXz_SZu2gPdl4N40g0WEWGOtTWyK0JKuFO3oq_guQg4gAgEWF0A7NJQHOv2WCtBs_6zVHCZaIipZrI_EUZWHj0WapF8SgN-faDnbisTfdug3H5OkUdomDq3SucGyQOHjA4L1MGqdVusQ1lM30kPUYivCRem1PXWpF4rs0zUO_QwTNAl3CHziDM4qLSCUxdNpKOmmtlaIAoSdwYAWkhOb0pFLHn0oJ3BFI5MDC5GK7IUBhj97LZWbYHuPiwmJZ0eXoytC6ExIutNyZvqlBmGkoW69uWV9Do89uyO0VTxpW21ioHIOtEFjgBXzUjmX4AdSzv6oLVOq8H7_zarT9O2Ss1cUFkpTFhHLTahrQhY8rvl-jFFql9cHxD18ecmZ7oL00qNMPjuLQqbhXvL1EnpmVKg9o9DHm4z-8q_JWCQ2_tYoS6AQGT2nK5tR9vz-TOg20aybBTwE4PZz_T8gElAYLpc4SXO2it6IS54Jlu6-ka6aRK627oSnZ73PPUVLL_apXLGiAXFrrkvSWagZNdOxF-VS5iXx02EDO6760on_NNl2Ekx3ZlLPrNeauGUdbSAdlv4wova16om4f62TOJ24iQtnb_svp8DmU4blCivkHJnrpH8ApN-oFcVC4MF-O86-4TeU__nm0jr_8yE2o4HRo3tiRePY9iXFSr7nrIAWmqfBSntSateMrNwrvdUUi1MmK8O3JZoKF9P4z8pYVhjRZMLngk1FEUIcG6Ln7tZTkF9EUfNHunWVnw7xsQ3rOL5ypmgBHt2XgsyShCoEn-sYsTowg7X65_CvSbLOO_zsY6Y5gmM-eF9tyQEWdxZeyShZJsE8xQy7Rj1Lb7NxwSzVBfCReoYWHF0XUa9dmO7tf20mciq5l5O1HrCcVdAW1238mOyyK5qz4RU6VPsYOV2rBg0qhVd3gF2Ec7log_jNbUHK5nAtzDySsdUyzrNDf2wM1DE9C3lj0gSFeqF8h9F145rgV_jyyQNj7zOwC8VJ36vcmy6Ju3vs76t-Mg7heP2YvODofAYn7pCm9LlQN82bnIqshGy6Ec3xKGHVNfNpO_a7Ac7elgWukpQBzM7IP7hIWuscmtnjbidXxEmwcW4il8FDpBL8QMn37z3fSOeBabGfGBI2xH_XqVQqpkugGaEUZP6vGcvS71E0Hls5snZzdzOS0MxOUbywvoKRHx5-0W35bAXfkHSqAKXj526lSduPFXotqI2yzjosNbiVk4m0zOvOWgCeTTIPwSf1WLd8SyYKBXeizH5D5XIF_IJ5aueQr8x2aVSk4GB0CkME5yijZu0iWqOLV1kA5snUK5H7OwmcYSle1uOLhNfu4ey6_3FuSwiUMs6xEE1TJP0smPcBDDBUUngbQyQWtKT5PpRlktVH9AV6UKlNtoA4MW4XpLT-WFjvLvm6S_d8wlZuhMCgg8afs2iUKe7xfz1It17IFNUYyf59YsKsyFo7dVgtlgMQJtCA-GPAqJvq8dUbkIV0k49iuUxdKL9sqc7aoShqFwcpztXVsMpFAXDuNHzGUn6iCxeB-SXcoXA0d7uema291Wy70ZNVXqWv6k-2_soA1CctE45Jn1N7D0-RMhvC7W-vqdXTYfr5UJBWmb1J35fcAgayKuJwGs17uHsHBp2exayINj0QxBi6-2mYLTu2NjhMMPCPRSGHNClCllHpTf65cs39re8C2PlEQEjdRzu3PNN7N9RyR01yttg-8ojNFBiKPgd6GVsDOKiId5FVETT1_1vbesKj042b0l4dVTvKWspx509X1G0QzBPW73nJgIQ0ZCBdqRuhhmvDq05KIz5eOf6p24VfyDUaHdcxFiufwT1PHOeGq80ha8Uarwn99EJ4DKmDH9ZZrnEo4fZC1-cLHg9rkynyR-nsG9TUEuxdPxSfdRAC7AMNg718c-eFtdftJyIzc6X1_aagCvQ9ptidm0ySbxxtS8wsjJECWeeGeoj2cndFIZ16IRdrpcFSsotYG_p8EcQqMn_FzG3OSZPia9itfFD7fOiP0d3vTRWMiXFJ7LxQ6Pb77q4vX7ABkWPngXhvuuI0QdlQ27qy9nPEdkSjtt8MuMsWPpcRhybu0X0YAbKROiZGkemiB7JMAYxtb3T52akmCrBBfaKXeqcDvpWhX4D1ZXjXjmj9Zny6_SqOwBHcb3InjgnsBt_ZncD9tHHjZgR-MOgAXFMPRcyxB_Sr9tr0_LxMcXAfS4f0rdQDgiPkGdYGxjAc5cwigk0Xbf7vuyMnheSh7zJGqdZkFLbYKzs8nUYztY_hcwTap5ueOs6LBtLBHO7Y.EPtD4o2agIxMVF8Dsip7kA'
#session_token ="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..r0a30oT3RA5vXrrc.G0ULyYWV2fbW3s-Eqo2ebjOoaTuI7Zv27LIA-4ktXCKRZO1DnUrhMfTvLKzMOMu692yRyr-6RGw9VkjMhL5CMg4iZ7EGyx5KRsWr8TYr7pwF_MFO39zynWSwnifv-nlxHDeT7ljKp7Zk909Bc4YRDSsHMgu3fegHu2VUSUXtrHtdt06e7jvoj7ych_lcv6FCVIi3B40k2aYw8ZvP_iGbuO5VB9zQlaqkvi5q_u3xvHu2aYgY0eN7n_e-mrh3DYtpZI-hC7OSy2ofvBC3vKz1wG0iUoUUabWPQgCZh6C7yQgoWLuKfBZpIF1oG6WRBQkMZ1ULscJ0ApOWxMjSOUlRbLX0OY3vST25qxNWXimOR5mYwcdB3rmjyQ9DTXvHv8FDbiht2chAd2ZFU4ZZA42gZUeBskE5xhETvlaMD_utApAYcrDBLyvEz_fLTUpTPKSekPrJmGNfuCYdJZI8w7HnhaGW_VhaPU0NyyVihdRBopGAdoguCsryAILclh4alNIFb8cV625tkUotL_ICvAhGhGyQDcrbji-oacXF-gu-wIN9Q2MmbJmAY8yCuKR-MpnFDagskWReBdejUG7gER-Bo7-3wGlWXt2tp7kvdP2QQz0z0yoXJtnU8GGEbst4Nu4EOBCnV4lQ6yTPL08rlAnpFkpFtPQ2RQmE0sRY4hXXeECT_4zZ4e8s3JDRxFYomRtKCjDNGPYN0sG1D9VRi_NuNFFvf2FsTEf0umjG-ju0BycSyYZmdDbRu0GQRYPm6iTSnXyKBlt1chYdzyQGONWSgEgcJ9EtwsgI9O89swqPhEeuuzS9Dug7Kz4PyiJpfCUNOgR9T8uE_Pr9nYYvxuxwOVFSirNW86eBnKwtM9Jr_zokXbhzD9tyoem31veteCE5jyaSoDTlkX4xuhqN9GebIHMdW9vpGmOonXAdE0UUh-6qBVkqxs3oG5lIAs_BHQ_ZvQS2oZ2uE2t20mv-L2IaYoGb3VjuPD8OO3QyMMdHG4uXq28Pr48N1LdOoeVx4cvdXKoOMEiWPWdIsuCoAnMAfinVtHW1JRGdALa7S00DpynfIdeqlEZEqcvYpw51Su3UMyNcx9txnXNTJhjmkaZ_oLRh6sqmuI7ipM3vrvcd1lp5BZZ6mBcdONSuJ8OUq38ZCaEYmGYZkxhNicCM-aV-uBmheYGdZd-pMjEZZNo3Wiehtn3cPDa0MdfpICZIfRcI3THZAzxP3GU-OBXRhdYN8mjDXJZMJhSxbWZc-_p7_DTtKIdqWId32n5YVag6FHG3lb_sdDuMWoOya0CEHu-KWCP-03FmQOfR3NVj0s8RucBfI5d7RbdXvIn1LqholbCeVfRZNdUuAQw_vXoJZYhPrEDs1kpngsJVjx1t7zI_8YwYIM-4jDu0pDShm32HP7xW-tdEKfDu1Z5Lgki--U1w6mCCzHRKSTYLWDxGN6YdjErxO7IshpXNVT_9dKipvCO062fUA0Ub2q6BnA8BoG0YpELfK_1BUX-H5RTLYb2-V82q1dT1hafR_MO2g5slxod2b6BNMgd9yrgfLRwm_E1ZfUAsmn-G9ANHDzBK5_B5fG3GuoqeudHGCUycU-x93xn_yL7AXehGWei-l2GRBEVsUd-2BevMyTnOn5Eim0yL3ie6RO1wuEnMXzC7mBw9Ga0XtJOwObE-DbFSe2WfmXHPAcSmCD8UYJoVGk4nqub0ez3Wp9eRVfK-txHECo64KaH9l6is6es9jimITs7rwXN9-38N5AkCHyeeJHekykpXuwglSmcazUditVWlRxf2-tReaCqzMi_mfOfXRrw3wVN6CDY_BpEhsfCfI_zJ0-C0aUlMNGrUHczCM9-fjC7jYCdzXvqM05sRxbs-j3VgwkMwfRmcvtcjfUFUs4ErEApgfmnLdz1bW7vDrLCHpquyhWk-OYUG8KCjXkpU8N72UadvHbYPG8KcZIWRk7zKfbwEDkITYn-ed1Yc8dmG6No6gK9htM-xcAyaAxkrtAjP323qD6Q_4tEcipuLr0ee8xGy4zPsK9crql3qCw8cXwPjpcVMPt526MHz5ICepgMERlrBqdO9wt0V2GpfLsvQvP-zxjRPWHQoOVU5Ea1mT5LTyelY2nZpnytBX_Oti-oSiXMpf5zpinNyjwNA0erPXts_Yu4tS7Ft0pwqa79iIr0jTa4z4EoFGmPL0jjpJZopjfa5SAVuzrjMTsBFRqqa92o6d21l-4r_B7voTLk7puqKEwzkydZZbS0BrKBt2uQWh-g9ObcVPHOji4viPzCeYlgdzN_9ajIUDFqi54Hu2EdYWqmbVQLQHtH3NZA-G35DSyLQK90HAUosBirvSKsgV9bEjs9kCPjJeqC47on_UVMSRCSIJKYzlUGQ8fzzFthwIWjDUfOONJNFfIeW2pdyGYQqeF0OvnxMSLliZQI_Qo2HW6mFtEE9VdGqU749pAr-dUb3-DyG-Ec9h7Xwa6yIlzcLLzyccB_yP41IkJbis-FAOaW40aamgmPxkuga6trmXVbGksE4EDyCLSaUdhH2TeJG7gtQjBz4u8Mfx9ILj6je4Yw6vhpqfSII1xhIICOs-acuZ8gXrKwU87upOu0tCWjiJFIRGfTrh3-IVQhcmkyQQobmUOnqFjTRyY3QMMegi3mVh1njEqM9JL6Lxr7GeVzBPZLYfjEhlkqfkGC-T13WljvA3FHtkROaQSVCIlS7QFj9iA6EiE7fsjLC9_gzTLGmL4him2RlZwP20ZjhrLriKAbVWPhmueaKo7usEwTif1lzhELh22HDetFqvJfdB06P1mM_-0SekJaKoJb_2fllXSV_Wj0ka4LL2Fu2oaqizygltI3gkASLMfrT.FjWLR1zcbRDkRHlgcTdgPg"
session_token ="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..vhAQiR9ecCpf6MXb.-uVJVp8wc9HHSuDtlnbe1r0IJzPGOUlWrTdMkKXv3LQWjcU2jv5YYufCbMiSS6PFjyTuhhEpt7wNh_kmw_NwqrxsPHRYKH5C9DLTwklB8EUSlzpluAF-jpw7XKq2wjY-lH2JldPl-0LLhJPxsxFYnnBILXZFq8A7g_v2V7SxuUpE6nhTEmEriloHqn_oEcP-gov2MEsSH6w9LWpg-cN8PkMN62-hhuQ9AWeBR1_tS32SAsup7HWpdrevis6OTyW1-HC2M69xxiautrv0NEsUl11W9eL_hnvhTn2D5_N3ERHkjN_H8MCUFSM92akjCUPjVk8-7XDvZK0L4yLy55kWPsuFNBNcEfa7hknJEqC8jeG2ttrCS-f7D-JGJdZvQjV-O8Mpas6tX3nEHwrYTOOBM2OLuS3bsI9ub_NyQGrdMYaBSrkT3Dv5-zv_kT6Thi5JYtZHbH67GMjj_JQcfBsyIN1h6u2FK9_RLzHCOHr7illLgWW6UI_gKVExS1wdmt_7cMXiR2Iln8aDp9UEkv94X-xZjJ9JrtPaIDHHjB846ZVWTQ0-YCAwjr062HEmV0uPp0oOqk9_csKyb8bWHwqbndKGWIyVJbHsQ0ororCyUC7TxdA_G45Y-NQ0Yfijqm10VGeMSiv-X_r-D62sPGhhXUkjpQ7xiyYytyD5n23O6aobnOcCyaxJLQ6R9yhiqGOOYp1DrryrT2Vzsy-Co5F3BO2xTHwDPwdLapS4OYbymxlBGbVSUUm3qXid4r8TaJ6Js-00yRZxEk2OHj73WZhrW6LyWZznbMqgHdr4d8HBp51rIJFjblHadfT6p1TEJFo_ZqhV1k4Ee6pyCGNC_ZztXFPbEKHXnsEbmLYzipMonFup0pAirUufOCRtDlwOZ954ODt9JAu7vqShd9Yd4WArzY9KZDOj2TSsLwa4X11Z0d6CMtCEobzgorTCyXu2IhWBuJq97DVDqbhp9KzDu12OBT2lL4F8ylauvFkt8_AX4DBk0f30VKFBfcdhkkv7f7hQtkzTMT8eTX13ZAGyIdwTbGMpY_N2e26nRtVPOUfxJUoSEv-He9Ohp55Cc5WD7dDS-yOjzGZJiIG0OwdCQsmKXa08P0ovr2AE1urWkVPobKw8gtArXiq5YXf9emm95bJGo0kGgccaVzrH1BJsRvNwrj-16_kogXeeexeqSyLrzbbHmke-tHC3RBP12TW3O0_L7k3d6ujuDXtTuRFkxGD7giip0Jo8dcP3uuwPthAcaT9bS4TO6rJBcJr7efpAX-4CF_7aKsvnNRiRgBmNfL8YM32HRlfL7K8FjBU7Ur4IyEXeHYO2qB7j_r1eGcaYfoSTMlKoYEODVgIyFT41ywwnVs2LP5hrAcesqdndY7dyAnF7AahYVFrMuQ0fmbpZbuCPjieAZ-v9yQUllsRYTfrEWSZOmy_5D9vD5MlF6QvouCKTSqOFRVpvHdz861304d0kVbRxO1pFRdHOTOV5Vi-x4jWbwv265EG_Tw3fYiDbJ0r8hgVfqEi0vTe1QkFpne8qKNBvP9VbboXY52aJPsyG-9kngGxGm3vPb0W35Wvp2RpjknkAoPyF1-JckkubmGC4THbl3IKSsfKvrPCgbO20XNxGBkqLnaZjJ4jr-n6QHmYb5yIz626dUjIAybRZ1K8e3tHsx42BpKQzkGcxSauZMsaZsRjUsbzXwEoER6pUGXX5lZbCb1_mjh5WSsZCiLzhJijEEEsMI-1-hIW5Og7nB8vPWwxYM-lyfWmvrm6CyciSAi3jUAOj0br_r7dNL9lREV2sw0FQMXZ1ikmhRyZF47ZrsFkxbJYHGzjW_NjjpXTWtOnQ8n-ri15Pz7lGdT7crQyW7KsZ-Hz9DY0OM9UwkQ-A8WWkQyEPGW5BrJb7bNyjmp9vS-vgHAbbSD_EWLaccntIbnWAESoq_6pKrzEq5WPHTYtjwY10wyMiNXvFMOJzlYHc44B_9yizmKKLbWqeCfRnbpJmpYTtKeuReD0ZIUAMWPqyh4W0SfvdhsjcnKgQAA7Fz_QSiZI5lhGHjfnK6C-BK9m_U3AI3E2XNP42pHAV_VbT9iWPVeEMlhyCy3FJbeIRVrOVoPFY_RnlP-iMnBEmfvLsT1IvGVgmHsmDqfXxAV2DInSJvgR_u1dUTFpcKh8dn6KDW2XgGe6OtDP7ZDXOkxNLlu97dm96jNfJtlrF6IF1MncCVsBb5FNX2HOe3cGO1yqX_i7kJcXLp0w2DOPAS0TZtpEN8xMxytJEzMZY1eD-48KXj_zJgJAWk-1ZQeQFxL4gHeSYCaURrt1y5LtWsBrro0XIodEfUeAs9AH3boK2FtiyKmrYgm5Bv6tno-Ge5tYdx8vqXpGslngcRa0rvFsZyOOzPvKxA27VrmlNXK8DORp0bqw5Qe1ImSAlERUGcyPkjl9WL-qBP_qhmGcK94IS7yOp1CahKR1Sw8rBXlNy4tcdpx3jx-Ya1syNNE3Sbbk-_NrwalxKhrqPJrfrzSGCH_UzkLzQVQYb29VLiJB-2SO1fB86tM2Poqedw74ueZACh696n_vlbOPXachrI9QovuOiPf0S3gALl0HjN4wa0eI1io4yM9XaOdz35uWx1VcIdfollf7QEcBQc1AoOw5voUJ5MqMljvFXFJv1JaV2I-1LpTC-SbwV0pUxna2pJNgmEiJpL_dolqYQuqwiQ6otT1eiIY5A4P7Q0Qlcjav-kpe1x1fwFGfMN5F1sUOv0u0gb6ug3y_EmIH8qogfvoqP4zbwtx4UO-KYuSQhyNGx-W6II76r7FiJPkw7075iywcluOmq6-GLTt_fjOYe5QqfuiZJCKNlvQOVQkN0MNpajbqY.RX171r_9GbEEJpxZOL1Y2g"
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

