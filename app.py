# imports
from helper import helper
from db_operations import db_operations

# import MySQL
import mysql.connector

# make connection
conn = mysql.connector.connect(host="localhost",
                               user="root",
                               password="CPSC408!",
                               auth_plugin='mysql_native_password',
                               database="collegeplanner")

# create cursor object
cur_obj = conn.cursor()

def options(): 
    print('''Select from the following menu options: 
    1. Create a new account
    2. Log into student account
    3. Log into professor account
    4. Exit
    ''')
    return helper.get_choice([1,2,3,4])

def student_options():
    print('''Select from the following menu options: 
    1. Browse Colleges & their degree programs
    2. Look up professor and their classes
    3. Exit
    ''')
    return helper.get_choice([1,2,3])

def professor_options():
    print('''Select from the following menu options: 
    1. Browse Classes
    2. Exit
    ''')
    return helper.get_choice([1,2])

def startscreen():
    print("Welcome to your CollegePlanner app!")


def createAccount():
    print('''Do you want a student account or professor account?:
              1. student
              2. professor''')
    account = helper.get_choice([1,2])

    if account == 1:

        name = input("Please input your name: ")

        print("Input your degree program: ")
        query = '''
        SELECT degreeProgramID, Name, collegeID
        FROM degreeProgram
        '''
        cur_obj.execute(query)
        choices = {}
        result = cur_obj.fetchall()
        for i in range(len(result)):
            print(f"{i}, {result[i][1]}")
            choices[i] = result[i]
        index = helper.get_choice(choices.keys())

        degreeProgramID = choices[index][0]
        collegeID = choices[index][2]

        query = '''
        SELECT * 
        FROM student
        '''
        cur_obj.execute(query)
        newID = len(cur_obj.fetchall()) + 1

        query = '''
        INSERT INTO student(studentID, Name, credits, degreeProgramID, collegeID)
        VALUES(%s, %s, %s, %s, %s)
        '''
        input_values = (newID, name, 0, degreeProgramID, collegeID)
        cur_obj.execute(query, input_values)
        conn.commit()
        print("Your student account has been made!")
    else:
        name = input("Please input your name: ")

        print("Input your College: ")
        query = '''
        SELECT collegeID, Name
        FROM college
        '''
        cur_obj.execute(query)
        choices = {}
        result = cur_obj.fetchall()
        for i in range(len(result)):
            print(f"{i}, {result[i][1]}")
            choices[i] = result[i]
        index = helper.get_choice(choices.keys())

        collegeID = choices[index][0]

        query = '''
        SELECT * 
        FROM professor
        '''
        cur_obj.execute(query)
        newID = len(cur_obj.fetchall()) + 1

        query = '''
        INSERT INTO professor(professorID, Name, collegeID)
        VALUES(%s, %s, %s)
        '''
        input_values = (newID, name, collegeID)
        cur_obj.execute(query, input_values)
        conn.commit()
        print("Your professor account has been made!")

def browseCollege():
    print("Choose the college you want to browse: ")
    query = '''
    SELECT collegeID, Name
    FROM college
    '''
    cur_obj.execute(query)
    choices = {}
    result = cur_obj.fetchall()
    for i in range(len(result)):
        print(f"{i}, {result[i][1]}")
        choices[i] = result[i]
    index = helper.get_choice(choices.keys())

    collegeID = choices[index][0]

    query = '''
    SELECT Name
    FROM degreeProgram
    WHERE collegeID = %s
    '''
    cur_obj.execute(query, (collegeID,))
    result = cur_obj.fetchall()
    for i in range(len(result)):
        print(f"{result[i][0]}")

def studentprofessorClasses():
    prof_name = input("Please enter the name of the professor: ")
    query = '''
    SELECT professorID
    FROM professor
    WHERE Name = %s
    '''
    cur_obj.execute(query, (prof_name,))
    result = cur_obj.fetchall()
    if len(result) == 0:
        print("There is no professor named ", (prof_name,))
    else: 
        professor_id = result[0]
        query = '''
        SELECT Name
        FROM course
        WHERE professorID = %s
        '''
        cur_obj.execute(query, professor_id)
        result = cur_obj.fetchall()
        print("Class results: ")
        for i in range(len(result)):
            print(f"{result[i][0]}")


def studentLogIn():
    user = input("Please enter your name: ")

    query = '''
    SELECT studentID
    FROM student
    WHERE Name = %s
    '''

    cur_obj.execute(query, (user,))
    results = cur_obj.fetchone()
    user_id = results[0]

    while True:
        user_choice = student_options()
        if user_choice == 1:
            browseCollege()
        elif user_choice == 2:
            studentprofessorClasses()
        else:
            break
    

def profLogIn():
    user = input("Please enter your name: ")

    query = '''
    SELECT professorID
    FROM professor
    WHERE Name = %s
    '''

    cur_obj.execute(query, (user,))
    results = cur_obj.fetchone()
    user_id = results[0]

    while True:
        user_choice = student_options()
        if user_choice == 1:
            print()
        elif user_choice == 2:
            print()
        elif user_choice == 3:
            print()
        else:
            break




while True:
    user_choice = options()
    if user_choice == 1:
        createAccount()
    elif user_choice == 2:
        studentLogIn()
    elif user_choice == 3:
        profLogIn()
    else:
        break
    


# print out connection to verify and close
print(conn)
conn.close