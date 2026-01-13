#imports
import streamlit as st
import db 

# Method that shows view of how many students there are per class
def studentsPerCollege(conn, cur_obj): # inputs are connection to the database
    
    # query selects results from view
    query = '''
    SELECT * FROM vStudentPerCollege;
    '''

    cur_obj.execute(query)
    result = cur_obj.fetchall()
    for i in range(len(result)):
        st.write(f"{result[i][0]}: {result[i][1]}")