import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection function
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="0.0.0.0",         # Replace with your host (e.g., "127.0.0.1")
            user="app",               # Your username
            password="qwEr!@#$09",    # Your password
            database="test_db"        # Your database name
        )
        return conn
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Fetch all users from the database
def fetch_users():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Add a new user to the database
def add_user(name, age, email):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, age, email) VALUES (%s, %s, %s)", (name, age, email))
            conn.commit()
            st.success("User added successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        conn.close()

# Streamlit App UI
st.title("Streamlit + MySQL Testing App")

# Fetch and display users
st.header("Existing Users")
users = fetch_users()
if users:
    for user in users:
        st.write(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}, Email: {user[3]}")
else:
    st.warning("No users found in the database.")

# Add a new user
st.header("Add a New User")
with st.form("add_user_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    email = st.text_input("Email")
    submitted = st.form_submit_button("Add User")

    if submitted:
        if name and email and age > 0:
            add_user(name, age, email)
        else:
            st.error("Please fill out all fields correctly!")
