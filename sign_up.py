import streamlit as st
import pymysql

def signup():
    st.sidebar.header("Create a new account")
    signup_first_name = st.sidebar.text_input("First Name", key="signup_first_name")
    signup_last_name = st.sidebar.text_input("Last Name", key="signup_last_name")
    signup_username = st.sidebar.text_input("Username", key="signup_username")
    signup_password = st.sidebar.text_input("Password", key="signup_password", type="password")
    signup_confirm_password = st.sidebar.text_input("Confirm Password", key="signup_confirm_password", type="password")
    signup_button = st.sidebar.button("Sign Up", key="signup_button")
    

    if signup_button:
        if not signup_first_name or not signup_last_name or not signup_username or not signup_password or not signup_confirm_password:
            st.sidebar.error("Please fill out all the required fields.")
        elif signup_password == signup_confirm_password:
            st.sidebar.success("Sign-up successful!")
        else:
            st.sidebar.error("Password and Confirm Password do not match.")

def insert_user_data(first_name, last_name, username, password):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM authentication WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        st.sidebar.error("Username is already in use. Please choose a different one.")
    else:
        cursor.execute("INSERT INTO authentication (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, username, password))
        conn.commit()

    cursor.close()
    conn.close()
