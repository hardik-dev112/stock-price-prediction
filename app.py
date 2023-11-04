from enum import auto
from re import search
import streamlit as st
from PIL import Image
import hydralit_components as hc
import pymysql
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf
from keras.models import load_model
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
from datetime import datetime 
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
from sklearn.preprocessing import MinMaxScaler
from alpha_vantage.fundamentaldata import FundamentalData


if 'is_user_logged_in' not in st.session_state:
    st.session_state.is_user_logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = None 

def home_page():
    st.header("What is stock market scanner?")
    st.write(
        "Welcome to our Stock Market Scanner! Easily search for any stock by its name, and instantly access comprehensive pricing data. Get a deep dive into each stock's detailed information, including key financial metrics and historical performance. Take your trading to the next level with our built-in trading strategies, powered by machine learning algorithms, which utilize indicators and moving averages to provide valuable insights"
        "for your investment decisions. Make smarter, data-driven choices with our all-in-one stock market companion"
    )

    # Online image URLs
    image1_url = "https://img.freepik.com/free-vector/hand-drawn-stock-market-concept-with-analysts_23-2149163670.jpg?size=626&ext=jpg&ga=GA1.2.1270880435.1696601840&semt=ais"
    image2_url = "https://img.freepik.com/premium-photo/stock-market-forex-trading-graph-graphic-concept_73426-96.jpg?size=626&ext=jpg&ga=GA1.1.1270880435.1696601840&semt=ais"
    image3_url = "https://img.freepik.com/free-vector/buy-sell-concept-design-showing-bull-bear_1017-13716.jpg?size=626&ext=jpg&ga=GA1.1.1270880435.1696601840&semt=ais"
    image4_url = "https://picsum.photos/200/300?random=4"



    st.image(image1_url, use_column_width="auto")


    st.header("How Scanner Works")
    st.write("1. Scanner take the name of stock and random date where user what to see .")
    st.write("2. The stock is then processed to extract relevant features.")
    st.write("3. A machine learning model, often a deep neural network, is used to predict the  stock price and nature of the stock.")
    st.write("4. The model's prediction is the Scanner result.")

    st.image(image2_url, use_column_width="auto")

    st.header("Getting Started with Stock price Scanner")
    st.write(
        "To get started with stock name, you need a symbol of stock name and starting date and ending date of period . "
    )


    stockname = {'Name': ['ICICI Bank' , 'SBI Bank', 'Axis Bank', 'HDFC Bank', 'ITC' , 'Tesla','Apple','Amazon'],
                'Symbol': [ 'ICICIBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'HDFCBANK.NS', 'ITC.NS','TSLA','AAPL','AMZN']}






    df = pd.DataFrame(stockname)
    df.index = df.index + 1
    st.table(df)

    st.image(image3_url, use_column_width="auto")



    # Image classification applications
    st.header("Stock Scanner Applications")
    st.write("-Search any type of stock .")
    st.write("-The ability to customize screening criteria is crucial..")




    # Conclusion
    st.header("Conclusion")
    st.write(
        "Stock price scanner is a fundamental task in Stock price, with a wide range of stock  and ongoing research. ")
    
#HOME PAGE FINISH-----------------------------------------------------------------------------------------------------------------------
    
def temp():
    st.title("If Your Want To Access...")
    st.header("For India...")
    st.write("First...")
    st.header("SignUp 🔝↗️")
    st.write("or")
    st.header("Login  🔝↗️")

def temp():
    st.title("If Your Want To Access...")
    st.header("For foreign...")
    st.write("First...")
    st.header("SignUp 🔝↗️")
    st.write("or")
    st.header("Login  🔝↗️")

def india():
        st.title("Indian Stock Prediction")
        ticker= st.text_input('Enter stock ticker','SBIN.NS')
        start_date =st.date_input('Start date')
        end_date = st.date_input('End date')

        df = yf.download(ticker, start=start_date, end= end_date)
        fig = px.line(df, x=df.index, y= df['Close'], title = ticker )
        st.plotly_chart(fig)
        st.write(df.describe())
        princing_data, chart_analysis= st.tabs(["Princing Data","Chart Analysis"])

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



        
        
       



    #spliting data into training and testing 

        data_training =pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
        data_testing  =pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])

        print(data_training.shape)
        print(data_testing.shape)



        
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



def foreign():
    st.title('Foreign stock Prediction')

    ticker= st.text_input('Enter stock ticker','AAPL')
    start_date =st.date_input('Start date')
    end_date = st.date_input('End date')

    df = yf.download(ticker, start=start_date, end= end_date)
    fig = px.line(df, x=df.index, y= df['Close'], title = ticker )
    st.plotly_chart(fig)


    #Describing Data
    st.write(df.describe())


    princing_data,fundamental_data, news, chart_analysis= st.tabs(['Princing Data',"fundamental_data", "Top 10 news", "Chart Analysis"])

    with princing_data:
        st.header("Price Movement")
        st.write(df)

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









# MySQL database
def connect_to_database():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stock_price"
    )
    return conn

def check_credentials(username, password):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, password FROM authentication WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data and user_data[2] == password:
        return True
    else:
        return False
    
def insert_user_data(first_name, last_name, username, password):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM authentication WHERE username = %s", (username))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Username is already in use. Please choose a different one.")
    else:
        cursor.execute("INSERT INTO authentication (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, username, password))
        conn.commit()

    cursor.close()
    conn.close()

    
def get_user_data(username):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, first_name, last_name FROM authentication WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user_data:
        user_data = {
            'username': user_data[0],
            'first_name': user_data[1],
            'last_name': user_data[2],
            
        }
        return user_data
    else:
        return None


def forgot_password():
    st.title("Forgot Password")

    reset_option = st.radio("Select Reset Option", ["Username"])

    if reset_option == "Username":
        username = st.text_input("Username", key="forgot_password_username")
    else:
        username = None

    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

    def reset_password():
        if reset_option == "Username":
            if username:
                user_data = get_user_data(username)
                if user_data:
                    if new_password == confirm_password:
                        conn = connect_to_database()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE authentication SET password = %s WHERE username = %s", (new_password, username))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Password reset successful. You can now login with your new password.")
                        st.session_state.next_page = "loginPage"
                    else:
                        st.error("New passwords do not match.")
                else:
                    st.error("Username not found. Please enter a valid username.")
    st.button("Reset Password", on_click=reset_password)

def logout():
    st.session_state.is_user_logged_in = False
    st.session_state.next_page = "login"
    st.session_state.username = None
    
# Login page
def login_page():
    st.title("Login Your Account")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    def on_login_button_click():
        if check_credentials(username, password):
            st.session_state.is_user_logged_in = True
            st.session_state.next_page = "logged_in"
            st.session_state.username = username
        else:
            st.error("Login failed. Please check your username and password.")

    st.button("Login", on_click=on_login_button_click)
    
    if st.button("Forgot Password"):
        st.session_state.next_page = "forgot_password"


# Signup page
def is_valid_string(input_str):
    return input_str.isalpha()

def signup_page():
    st.title("Sign-Up Page")

    # Display a string input field for the first name
    first_name = st.text_input("First Name", key="signup_first_name")

    # Display a string input field for the last name
    last_name = st.text_input("Last Name", key="signup_last_name")
    new_username = st.text_input("Username", key="signup_username")
    new_password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
    captcha = st.checkbox("I am not a robot", key="signup_captcha")

    def on_signup_button_click():
        if (
            first_name
            and last_name
            and new_username
            and new_password
        ):
            if is_valid_string(first_name) and is_valid_string(last_name):
                insert_user_data(first_name, last_name, new_username, new_password,)
                st.session_state.is_user_logged_in = True
                st.session_state.next_page = "logged_in"
                st.session_state.username = new_username
            else:
                st.error("Please enter valid first and last names with only characters.")
        else:
            st.error("Please fill in all required fields.")

    st.button("Sign Up", on_click=on_signup_button_click)



    def logout():
        st.session_state.is_user_logged_in = False
        st.session_state.next_page = "login"
        st.session_state.username = None
    
def user_page():
    if st.session_state.is_user_logged_in:
        username = st.session_state.username
        user_data = get_user_data(username)


        display_user_info(user_data)


        st.button("Logout", on_click=logout)
    
    else:
        st.write("You are not logged in. Please log in first.")
    
def display_user_info(user_data):
    conn = connect_to_database()
    cursor = conn.cursor()

    if user_data and 'first_name' in user_data and 'last_name' in user_data:
        st.title(f"Welcome, {user_data['first_name']} {user_data['last_name']}")
        
        st.header("Edit Profile")
        
        first_name = st.text_input("First Name:", user_data['first_name'])
        last_name = st.text_input("Last Name:", user_data['last_name'])
        if st.button("Update Profile"):
            success = True
            cursor.execute(
                "UPDATE authentication SET first_name = %s, last_name = %s WHERE username = %s",
                (first_name, last_name, user_data['username'])
            )
            conn.commit()
            cursor.close()
            conn.close()
            if success:
                st.success("Profile updated successfully")
    else:
        st.write("User information not available")


def logged_in_content():
    modify_css()
    username = st.session_state.username 
    user_data = get_user_data(username)
    
    if user_data:
        user_name = f"{user_data['first_name']} {user_data['last_name']}"
    else:
        user_name = ""

    menu_data = [
        {'id': 'Home', 'label': "Home"},
        {'id': 'India', 'label': "India"},
        {'id': 'Foreign','label': "Foreign"},
        {'id': 'user_page','icon': "🟢",'label': user_name},
    ]

    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False,
        sticky_nav=True,
        sticky_mode='pinned',
    )

    if menu_id == 'Home':
        home_page()
    elif menu_id == 'India':
        india()
    elif menu_id == 'Foreign':
        foreign()    
    elif menu_id == 'user_page':
        user_page()
      

def logged_out_content():
    modify_css()
    menu_data = [
        {'id': 'home','label': "Home"},
        {'id': 'india', 'label': "india"},
        {'id': 'Foreign','label': "Foreign"},
        {'id': 'signup','label': "Sign Up"},
        {'id': 'login','label': "Login"},
        
    ]
    over_theme = {'txc_inactive': '#FFFFFF'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        hide_streamlit_markers=False,
        sticky_nav=True,
        sticky_mode='pinned',
    )
    
    if menu_id == 'home':
        home_page()
    elif menu_id == 'india':
        temp()
    elif menu_id == 'Foreign':
        temp()        
    elif menu_id == 'signup':
        signup_page()
    elif menu_id == 'login':
        login_page()

#Main Program.......................................................................................................................
st.set_page_config(
    layout="wide",              
    initial_sidebar_state="auto", 
    page_title="Stock Prediction",
)
def modify_css():
    custom_css = """
        <style>
        .st-emotion-cache-z5fcl4 {
        width: 100%;
        padding: 2.5rem 1rem 10rem;
        min-width: auto;
        max-width: initial;
        padding:29px 27px;
        }

        img {
        border-radius: 8px;
        }
        img:hover {
        box-shadow: 0 0 5px 5px rgba(0, 140, 186, 0.5);
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


if "next_page" in st.session_state:
    if st.session_state.next_page == "logged_in":
        logged_in_content()
    elif st.session_state.next_page == "login":
        logged_out_content()
    elif st.session_state.next_page == "forgot_password":
        forgot_password()
    elif st.session_state.next_page == "loginPage":
        login_page()
else:
    logged_out_content()
