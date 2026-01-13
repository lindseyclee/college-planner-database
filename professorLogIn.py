#imports
import streamlit as st
import db 

from browseClass import browseClass
from viewYearBreakdowntInClass import viewYearBreakdownInClass
from studentsPerCollege import studentsPerCollege

def professorLogin(conn, cur_obj): # For professor log in 

    st.title("Professor Log in")

    if 'professor_id' not in st.session_state:
        st.session_state['professor_id'] = None # Ensures that during the start that there is no initital professor selectionn 

    if st.session_state['professor_id'] is None: # Professor logs in by typing their name which will be used for a query to store the professors id
        user = st.text_input("Please enter your name: ")
        if st.button("Log In"):
            query = '''
            SELECT professorID
            FROM professor
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
                FROM professor
                WHERE professorID = '%s'
                '''
                cur_obj.execute(query, (user_id,))
                results = cur_obj.fetchone()
                status = results[0]

                if status == 0:
                    st.error("Your account has been deactivated, please reactivate to use. ")
                else: 
                    st.session_state['professor_id'] = user_id
                    st.success(f"You have successfully logged in as {user}")
                    st.rerun()
    else:
        st.write(f"Welcome!") # Once logged in, professor will be givcen options 

        professor_options = ["Browse the classes you are teaching", "Browse student year breakdown in your class", "View total students per college", "Log out"]
        option = st.radio("Select an option", professor_options)

        if option == "Browse the classes you are teaching":
            browseClass(conn, cur_obj, st.session_state['professor_id'])
        elif option == "Browse student year breakdown in your class":
            viewYearBreakdownInClass(conn, cur_obj, st.session_state['professor_id'])
        elif option == "View total students per college":
            studentsPerCollege(conn, cur_obj)
        elif option == "Log out":
            st.session_state['professor_id'] = None # Once logged out user will have to log in again 
            st.rerun()