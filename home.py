
from enum import auto
from re import search
import streamlit as st
from PIL import Image
import pymysql
import pandas as pd
from streamlit_option_menu import option_menu
def experimental_rerun(page):
  st.session_state.next_page = page
  st.experimental_rerun("india")


# selected = option_menu(
#     menu_title ="Main Menu",
#     options =["home","contact","india", "foreign","Signup", "Login"],
#     orientation ="horizontal"
# )

#for login ke liye likha he
#if 'user_login' not in st.session_state:
    #st.session_state.user_login = False


st.title("Stock market scanner")

st.write("Welcome to the stock price scanner!")

st.sidebar.title("User Actions")

user_action = st.radio("", ["Signup", "Login"])
#user_action = st.sidebar.radio("", ["Signup", "Login"])

# username = "111"
# password = "111"



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

    cursor.execute("SELECT username FROM authentication WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.error("Username is already in use. Please choose a different one.")
    else:
        cursor.execute("INSERT INTO authentication (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, username, password))
        conn.commit()

    cursor.close()
    conn.close()
    

if user_action == "Signup":
    st.sidebar.header("Create a new account")
    first_name = st.sidebar.text_input("First Name", key="first_name")
    last_name = st.sidebar.text_input("Last Name", key="last_name")
    #date_of_birth = st.sidebar.date_input("Date of Birth", key="signup_date_of_birth")
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", key="password", type="password")
    confirm_password = st.sidebar.text_input("Confirm Password", key="signup_confirm_password", type="password")
    
    def on_signup_button_click():
        if (
            first_name
            and last_name
            and username
            #and date_of_birth
            and password
        ):
            insert_user_data(first_name, last_name, username, password)
            # st.experimental_rerun()
            #st.experimental_rerun("india")
            # st.experimental_rerun(page="india")
        
        elif(
            st.experimental_rerun(page="india")
        ):

            # else:
            st.error("Please fill in all required fields.")

            st.sidebar.button("Sign Up", on_click=on_signup_button_click)
        elif user_action == "Login":
            st.sidebar.header("Login")
            username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", key="login_password", type="password")
        #st.experimental_rerun()
   

else:
    st.error("Please fill in all required fields.")
    def on_login_button_click():
        if check_credentials(username, password):
            st.session_state.is_user_logged_in = True
            st.session_state.next_page = "logged_in"
            st.session_state.username = username
        else:
            st.error("Login failed. Please check your username and password.")

    st.sidebar.button("Login", on_click=on_login_button_click)





 



# Image classification information
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

def logged_in_content():
    modify_css()
    username = st.session_state.username 
    user_data = get_user_data(username)
    
    if user_data:
        user_name = f"{user_data['first_name']} {user_data['last_name']}"
    else:
        user_name = ""

    menu_data = [
        {'id': 'Home', 'icon': "🏠", 'label': "Home"},
        {'id': 'predict', 'icon': "🐱‍💻", 'label': "Predict"},
        {'id': 'user_page','icon': "🟢",'label': user_name},
        {'id': 'about', 'icon':"🏟️", 'label': "About"},
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
    elif menu_id == 'predict':
        predict_page()
    elif menu_id == 'user_page':
        user_page()
    elif menu_id == 'about':
        about()  

def logged_out_content():
    # #modify_css()
    # menu_data = [
    #     {'id': 'home', 'icon': "🏠", 'label': "Home"},
    #     {'id': 'predict', 'icon': "🐱‍💻", 'label': "Predict"},
    #     {'id': 'signup', 'icon': "🎯", 'label': "Sign Up"},
    #     {'id': 'login', 'icon': "⚡", 'label': "Login"},
    #     {'id': 'about', 'icon':"🏟️", 'label': "About"},
    # ]
    # over_theme = {'txc_inactive': '#FFFFFF'}
    # menu_id = hc.nav_bar(
    #     menu_definition=menu_data,
    #     override_theme=over_theme,
    #     hide_streamlit_markers=False,
    #     sticky_nav=True,
    #     sticky_mode='pinned',
    # )
    
    # if menu_id == 'home':
    #     home_page()
    # elif menu_id == 'predict':
    #     temp()
    # elif menu_id == 'about':
    #     about()        
    # elif menu_id == 'signup':
    #     signup_page()
    # elif menu_id == 'login':
    #     login_page()


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
