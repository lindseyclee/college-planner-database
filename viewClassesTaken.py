#imports
import streamlit as st
import db 
import pandas as pd

# method to get csv file of all the classes a student has taken

def viewClassesTaken(conn, cur_obj, id): # inputs are variables related to connect to a database and student id 

    # query joins the classes that a student has taken and the required classes given student id 
    query = '''
    SELECT c.Name
    FROM classes_take AS ct
    INNER JOIN course AS c
        ON ct.courseID = c.courseID
    WHERE ct.studentID = '%s'
    '''  
    df = pd.read_sql_query(query, conn, params = (id,))

    df.to_csv('classreport.csv',index = False) # converts into a csv file 

    st.success("Your list has been downloaded!") # message once it is done 