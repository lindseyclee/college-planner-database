import streamlit as st
import db 

# Method for deleting/deactivatin/reactivating account 
def activate(conn, cur_obj):
    st.title("Activate/Deactivate account")

    account_type = st.radio("Choose account type:", ["Student", "Professor"]) # choose between student or professor 

    if account_type == "Student":
        
        user = st.text_input("Please enter your name: ") # Makes user enter their name in order to retrieve their id

        query = '''
        SELECT studentID
        FROM student
        WHERE Name = %s
        '''



        if st.button("Enter"): # Button for entering query to search if the user exists 

            cur_obj.execute(query, (user,))
            results = cur_obj.fetchone()

            user_id = results[0]

            cur_obj.execute(query, (user,))
            results = cur_obj.fetchone()

            if results == None:
                st.error("There is no existing user.")
                return
            else: 
                user_id = results[0]
                display_options = ["Activate", "Deactivate"]
                active = st.selectbox("Do you want to activate or deactivate the account?", ["-- Select option --"] + display_options) # Option to activte or deactivate

                if  active != "-- Select option --":

                    if active == "Activate": # Activate
                        
                        query = '''
                        UPDATE student
                        SET active = 1
                        WHERE studentID = %s
                        '''
                        cur_obj.execute(query, (user_id,))
                        conn.commit()
                        st.success("Your account is active!")
                    elif active == "Deactivate":
                        # Deactivate
                        query = '''
                        UPDATE student
                        SET active = 0
                        WHERE studentID = %s
                        '''
                        cur_obj.execute(query, (user_id,))
                        conn.commit()
                        st.success("Your account is inactive!")

    else: # Professor is similar to student except it retrieves the professor id instead of student

        user = st.text_input("Please enter your name: ")

        if st.button("Enter"): # Button for entering query to search if the user exists :
            

            query = '''
            SELECT professorID
            FROM professor
            WHERE Name = %s
            '''

            cur_obj.execute(query, (user,))
            results = cur_obj.fetchone()

            if results == None:
                st.error("There is no existing user.")
                return
            else:
                user_id = results[0]
                display_options = ["Activate", "Deactivate"]
                active = st.selectbox("Do you want to activate or deactivate the account?", ["-- Select option --"] + display_options) # Option to activte or deactivate

                if  active != "-- Select option --":
                    if active == "Activate":
                        query = '''
                        UPDATE professor
                        SET active = 1
                        WHERE professorID = %s  
                        '''
                        cur_obj.execute(query, (user_id,))
                        conn.commit()

                        st.success("Your account is active!")   
                    elif active == "Deactivate":
                        query = '''
                        UPDATE professor
                        SET active = 0
                        WHERE professorID = %s
                        '''
                        cur_obj.execute(query, (user_id,))
                        conn.commit()
                        st.success("Your account is inactive!")
                        
