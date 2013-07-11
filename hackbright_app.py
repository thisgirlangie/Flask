import sqlite3
import re

DB = None
CONN = None

#TODO: handle when no data is returned for the below get_ functions

#given a github acct, print corresponding student name
def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title=?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row:
        print """\tTitle: %s
        Description: %s
        Max Score: %s""" % (row[0], row[1], row[2])
    else:
        print "There isn't a project with that title."

def make_new_student(first, last, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first, last, github))

    CONN.commit()
    print "Successfully added student: %s %s" % (first, last)

def make_new_project(title, descrip, max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, descrip, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % title

def give_grade_to_student(github, project, grade):
    query = """INSERT into Grades values (?,?,?)"""
    DB.execute(query, (github, project, grade))
    CONN.commit()
    print "Successfully gave %s a grade of %s for project %s" % (github, grade, project)

def get_all_grades_for_project(title):
    query = """SELECT first_name, last_name, grade from GradesView WHERE project_title=?"""
    DB.execute(query, (title,))
    rows = DB.fetchall()
    print """Project: %s""" % title
    for r in rows:
        print """Name: %s %s   Grade: %s""" % (r[0], r[1], r[2])

def get_grades_by_github(github):
    query = """SELECT project_title, grade from Grades WHERE student_github=?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    #for r in rows:
    #    print """Project: %s  Grade: %s""" % (r[0], r[1])
    return rows

def get_grades_by_name(first, last):
    query = """SELECT title, grade, max_grade 
                from ReportCardView WHERE first_name=? and last_name=?"""
    DB.execute(query, (first,last))
    rows = DB.fetchall()
    print """\
    Github: %s %s""" % (first,last)
    for r in rows:
        print """Project: %s  Grade: %s/%s""" % (r[0], r[1], r[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def split_into_command_and_args(text):
    tokens = text.split()
    command = None
    args = []
    if tokens:
        command = tokens[0]
    if len(tokens) > 1:
        args = tokens[1:]

    # deal with splitting on quote marks if used
    # TODO: the below code is gross...there must be a more elegant way? look for a library to handle?

    if re.search("[\"]", text):
        s = " ".join(args)
        args = s.split("\"")

        i=0
        while i < len(args):

            if args[i] == "":
                args.pop(i)
            else:
                if args[i][0] == " ":
                    args[i] = args[i][1:]
                if args[i][-1] == " ":
                    args[i] = args[i][0:-1]
            i += 1

    return (command, args)

def print_help_info():
    print "Available commands are:"
    print "Get a student's info: student <github name>"
    print "Add a new student: new_student <first> <last> <github>"
    print "Get project info: project <project name>"
    print "Add a new project: new_project <name> <description> <maxscore>"
    print "Give a new grade: give_grade <github> <project name> <grade>"
    print "Get grades by name: get_grades_by_name <first> <last>"
    print "Get grades by github: get_grades_by_github <github>"
    print "Get all grades for a project: get_grades_for_project <project name>"

def check_args_len(args,n):
    if len(args) == n:
        return True
    print "Ooops! You gave %s arguments, but needed %s arguments." % (len(args),n)
    return False

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        
        command, args = split_into_command_and_args(input_string)


        if command == "student" and check_args_len(args,1):
                get_student_by_github(*args) 
        elif command == "new_student" and check_args_len(args,3):
                make_new_student(*args)
        elif command == "project" and check_args_len(args,1):
                get_project_by_title(*args)
        elif command == "give_grade" and check_args_len(args,3):
            give_grade_to_student(*args)
        elif command == "get_grades_for_project" and check_args_len(args,1):
            get_all_grades_for_project(*args)
        elif command == "get_grades_by_github" and check_args_len(args,1):
            get_grades_by_github(*args)
        elif command == "get_grades_by_name" and check_args_len(args,2):
            get_grades_by_name(*args)
        elif command == "new_project" and check_args_len(args,3):
            make_new_project(*args)
        elif command == "help":
            print_help_info()
        else:
            print "Oops, you did it wrong. Try again! Type help to see your options."

    CONN.close()

if __name__ == "__main__":
    main()
