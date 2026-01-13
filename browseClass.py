#imports
import streamlit as st
import db 

# Method for professor to browse the classes they teach
def browseClass(conn, cur_obj, id): # inputs are connection to the database and professor id

    st.title("Browse your classes")

    if st.button("Browse"):

        # query gets the name of courses based on the professor id student gives
        query = '''
        SELECT Name
        FROM course
        WHERE professorID = '%s'
        '''
        cur_obj.execute(query, (id,))
        result = cur_obj.fetchall()
        for i in range(len(result)):
            st.write(f"{result[i][0]}")