#imports
import streamlit as st
import db 
from browseCollege import browseCollege
from updateyear import updateYear
from studentProfessorClasses import studentProfessorClasses
from registerClass import registerClass
from viewClassesTaken import viewClassesTaken

def studentLogin(conn, cur_obj): # For professor log in 

    st.title("Student Log in")

    if 'student_id' not in st.session_state:
        st.session_state['student_id'] = None # Ensures that during the start that there is no initital student selectionn 

    if st.session_state['student_id'] is None: # Student logs in by typing their name which will be used for a query to store the student id
        user = st.text_input("Please enter your name: ") 
        if st.button("Log In"):
            query = '''
            SELECT studentID
            FROM student
            WHERE Name = %s
            '''
            cur_obj.execute(query, (user,))
            results = cur_obj.fetchone()

            if results == None:
                st.error("There is no existing user.") # returns error if ther is no existing user 
            else: 
                user_id = results[0] # checks if studenrt account is active or not
                query = '''
                SELECT active
                FROM student
                WHERE studentID = %s
                '''
                cur_obj.execute(query, (user_id,))
                results = cur_obj.fetchone()
                status = results[0]

                if status == 0:
                    st.error("Your account has been deactivated, please reactivate to use. ")
                else: 
                    st.session_state['student_id'] = user_id
                    st.success(f"You have successfully logged in as {user}")
                    st.rerun()
    else:
        st.write(f"Welcome!") # Once logged in, student will be givcen options 

        student_options = ["Browse Colleges & their degree programs", "Update year", "Look up professor and their classes","Register for your class", "View classes taken", "Log out"]
        option = st.radio("Select an option", student_options)

        if option == "Browse Colleges & their degree programs":
            browseCollege(conn, cur_obj)
        elif option == "Update year":
            updateYear(conn, cur_obj, st.session_state['student_id'])
        elif option == "Look up professor and their classes":
            studentProfessorClasses(conn, cur_obj)
        elif option == "Register for your class":
            registerClass(conn, cur_obj, st.session_state['student_id'])
        elif option == "View classes taken":
            viewClassesTaken(conn, cur_obj, st.session_state['student_id'])
        elif st.button("6. Log Out"):
            st.session_state['student_id'] = None
            st.rerun()