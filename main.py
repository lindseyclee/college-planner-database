# imports
import streamlit as st
import db
from createaccount import createaccount
from activate import activate
from studentLogIn import studentLogin
from professorLogIn import professorLogin

conn, cur_obj = db.start_connection()

# Starting Screen
st.sidebar.title("CollegePlanner")
st.title("Welcome to your CollegePlanner app!")

# Slider to help navigate to different pages
page = st.sidebar.radio(
    "Navigate to",
    ("Create Account", "Student Login", "Professor Login", "Activate/Deactivate Account", "Exit")
)

if page == "Create Account": # navigate to create account page
    createaccount(conn, cur_obj)
elif page == "Student Login": # navigate to student log in page
    studentLogin(conn,cur_obj)
elif page == "Professor Login": # navigate to professor log in page
    professorLogin(conn,cur_obj)
elif page == "Activate/Deactivate Account": # navigate to activate/deactivate page
    activate(conn, cur_obj)
else:
    conn.close() # closes connection to database

