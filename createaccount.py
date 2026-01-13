#imports
import streamlit as st
import db 

# Method for account creation

def createaccount(conn, cur_obj):
    st.title("Account Creation")
    account_type = st.radio("Choose account type:", ["Student", "Professor"]) # Choose between student or professor

    if account_type == "Student": # For student

        name = st.text_input("Please input your name: ") # first gets name from user

        st.write("Input your degree program: ") # Then makes user choose existing degree program
        query = '''
        SELECT degreeProgramID, Name, collegeID
        FROM degreeProgram
        '''
        cur_obj.execute(query)
        choices = {}
        display_options = []
        result = cur_obj.fetchall()
        for i in range(len(result)):
            display = f"{i}: {result[i][1]}"
            display_options.append(display)
            choices[i] = result[i]

        selected_display = st.selectbox("Select your degree program:", display_options)
        index = int(selected_display.split(":")[0])

        degreeProgramID = choices[index][0]
        collegeID = choices[index][2]

        if st.button("Submit Student"): # Button to submit all user 

            query = '''
            SELECT * 
            FROM student
            '''
            cur_obj.execute(query)
            newID = len(cur_obj.fetchall()) + 1

            # creaters new user entity
            query = '''
            INSERT INTO student(studentID, Name, degreeProgramID, collegeID, active, year) 
            VALUES(%s, %s, %s, %s, %s, %s)
            '''
            input_values = (newID, name, degreeProgramID, collegeID, 1, 1)
            cur_obj.execute(query, input_values)
            conn.commit()
            st.success("Your student account has been made!")

    elif account_type == "Professor": # For professor

        name = st.text_input("Please input your name: ") # first gets name from user

        print("Input your College: ") # then makes user select the college they are teaching
        query = '''
        SELECT collegeID, Name
        FROM college
        '''
        cur_obj.execute(query)
        choices = {}
        display_options = []
        result = cur_obj.fetchall()
        for i in range(len(result)):
            display = f"{i}: {result[i][1]}"
            display_options.append(display)
            choices[i] = result[i]

        selected_display = st.selectbox("Select your college: ", display_options)
        index = int(selected_display.split(":")[0])

        collegeID = choices[index][0]

        if st.button("Submit professor"): # Button for submitting all information and creating new professor entity

            query = '''
            SELECT * 
            FROM professor
            '''
            cur_obj.execute(query)
            newID = len(cur_obj.fetchall()) + 1

            query = '''
            INSERT INTO professor(professorID, Name, collegeID, active)
            VALUES(%s, %s, %s, %s)
            '''
            input_values = (newID, name, collegeID, 1)
            cur_obj.execute(query, input_values)
            conn.commit()
            st.success("Your professor account has been made!")