#imports
import streamlit as st
import db 

# Method that 
def viewYearBreakdownInClass(conn, cur_obj, id): # inputs are connection to the database and professor id

    # query selects name and course id from course once given progessor id
    query = '''
    SELECT Name, courseID
    FROM course
    WHERE professorID = %s
    '''

    cur_obj.execute(query, (id,))

    choices = {}
    display_options = []
    result = cur_obj.fetchall()
    for i in range(len(result)):
        display = f"{i}: {result[i][0]}"
        display_options.append(display)
        choices[i] = result[i]

    selected_display = st.selectbox("Select class:", ["-- Select class --"] + display_options) # Shows a list of classes that the professor teach that he/she can choose from

    if selected_display != "-- Select class --": # Once there is a selection code below runs 

        index = int(selected_display.split(":")[0])
        classID = choices[index][1]

        # Query uses subquery to join year, student and classes_take table given the inputted course_id. Gets the name of the year and count of the total number of students grouped by year
        query = '''
        SELECT y.Name, COUNT(*) AS Students_Per_Year 
        FROM year AS y
        WHERE y.yearID IN (
            SELECT s.year
            FROM student AS s
            WHERE s.studentID IN (
                SELECT ct.studentID
                FROM classes_take AS ct
                WHERE ct.courseID IN (
                    SELECT c.courseID
                    FROM course AS c
                    WHERE courseID = %s
                )
            )
        )
        GROUP BY y.Name;
        '''

        cur_obj.execute(query, (classID,))
        result = cur_obj.fetchall()

        st.write("Results: ") # Shows the breakdown per class
        for i in range(len(result)):
            st.write(f"{result[i][0]}: {result[i][1]}")