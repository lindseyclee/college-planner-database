#imports
import streamlit as st
import db 

# Function to browse college and give the list of all programs within that college
def browseCollege(conn, cur_obj):

    st.title("Browse colleges and their degree programs")

    # query selects collegeID and name from college 
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

    selected_display = st.selectbox("Select college:", ["-- Select year --"] + display_options) # Shows the list of existing colleges from the query

    if selected_display != "-- Select year --": # Once user picks an option code below runs 

        index = int(selected_display.split(":")[0])
        collegeID = choices[index][0]

        st.write("Degree Programs Offered:")

        # query selects name from degreeProgram given user inputs college id 
        query = '''
        SELECT Name
        FROM degreeProgram
        WHERE collegeID = %s
        '''
        cur_obj.execute(query, (collegeID,))
        result = cur_obj.fetchall()
        for i in range(len(result)):
            st.write(f"{result[i][0]}") # Shows a list of all the degree programs the college has taken from the query