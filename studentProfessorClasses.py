import streamlit as st
import db 

# Method to let users search up all the classes a professor teaches 

def studentProfessorClasses(conn, cur_obj): # Inputs are variables for connecting to database 

    st.title("Look the classes a professor teaches")

    prof_name = st.text_input("Please enter the name of the professor: ") # student enters name of the professor 

    query = '''
    SELECT professorID
    FROM professor
    WHERE Name = %s
    '''
    cur_obj.execute(query, (prof_name,))
    result = cur_obj.fetchall()

    if st.button("Enter"):

        if len(result) == 0:
            st.write("There is no professor named ", (prof_name,)) # Shows if name does not exist 
        else: 
            
            # query that gets professor id and shows the classes associated by that id 
            professor_id = result[0]
            query = '''
            SELECT Name
            FROM course
            WHERE professorID = %s
            '''
            cur_obj.execute(query, professor_id)
            result = cur_obj.fetchall()
            st.write("Class results: ")
            for i in range(len(result)):
                st.write(f"{result[i][0]}")
