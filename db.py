# imports
import mysql.connector
import streamlit as st

# make connection to databse
def start_connection():
    conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="CPSC408!",
                               auth_plugin='mysql_native_password',
                               database="collegeplanner")
    cur_obj = conn.cursor()
    return conn, cur_obj

# close connection to database
def close_connection(conn):
    conn.close()
