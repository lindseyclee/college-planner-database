import streamlit as st
import db 


# Method that lets student change their year 
def updateYear(conn, cur_obj, id): # inputs are variables related to connecting to database and student id
    st.title("Update year")

  
    # four options students can pick from: Freshman, Sopphomroe and Senior 
    year_options_dict = {"Freshman": 1, "Sophomore": 2, "Junior": 3, "Senior": 4} # Useing dictionary in order to get id value based on choice 
    year_options_list = list(year_options_dict.keys())

    new_year_choice = st.selectbox("Please choose your year: ", year_options_list) 
    new_year_input = year_options_dict[new_year_choice]

    if st.button("Enter"): # Button to enter in the new year 

        query = '''
        UPDATE student
        SET year = %s
        WHERE studentID = %s
        '''
        input_values = (new_year_input, id)
        cur_obj.execute(query, input_values)
        conn.commit()
        st.success("You have changed your year!") # success message once it worked

        