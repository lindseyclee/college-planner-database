import streamlit as st
import db 

# Method for student to register for a class 
def registerClass(conn, cur_obj, id): # inputs are 
    
    st.title("Register for class")

    # One query that joins course_reuirements and course and subtracting that from one query Joining course_requirements, course and classes_take given the student id
    query = '''
    SELECT course.Name, course.courseID
    FROM course_requirements
    INNER JOIN course
    ON course_requirements.courseID = course.courseID
    EXCEPT
    SELECT course.Name, course.courseID
    FROM course_requirements
    INNER JOIN course
    ON course_requirements.courseID = course.courseID
    INNER JOIN classes_take
    ON course.courseID = classes_take.courseID
    WHERE classes_Take.studentID = %s;
    '''
    input_values = (id,)
    cur_obj.execute(query, input_values)

    st.write("This is a list of classes you have yet to take. ") # Returns a list of classes student has yet to register that they can register
    st.write("Please input which class you want to register for. ")

    choices = {}
    display_options = []
    result = cur_obj.fetchall()
    for i in range(len(result)):
        display = f"{i}: {result[i][0]}"
        display_options.append(display)
        choices[i] = result[i]

    selected_display = st.selectbox("Select college:", ["-- Select Class --"] + display_options)

    if selected_display != "-- Select Class --": # once student selects an option code below runs 

        index = int(selected_display.split(":")[0])
        courseID = choices[index][1]

        input_values = (id, courseID, None)

        cur_obj.callproc("register_class", input_values)

        # Query to get results from stored procedure and transaction
        query = '''
        SELECT @ouput AS result;
        '''

        cur_obj.execute(query)
        result = cur_obj.fetchall()

        if result[0][0] == 'success':
            st.success("You have successfully registered the class!") # Sucess message 
        elif result[0][0] == 'fail':
            st.error("You do not meet the prerequisite year of the class.")  # if student does not meet prerequisite year then this shows  
