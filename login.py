import streamlit as st
import pymysql

def login():
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", key="login_password", type="password")
    login_button = st.sidebar.button("Login", key="login_button")

    if login_button:
        if not username or not password:
            st.sidebar.error("Please fill out all the required fields.")
        else:
            if check_credentials(username, password):
                st.sidebar.success("Login successful.")
            else:
                st.sidebar.error("Login failed. Please check your credentials.")
