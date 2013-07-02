import sqlite3

DB = None
CONN = None


def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def get_project_by_title(title):
    query = """SELECT * FROM Projects WHERE title=?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Title: %s
    Description: %s
    Max Score: %s""" % (row[0], row[1], row[2])

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
    print """\
    Github: %s""" % github
    for r in rows:
        print """Project: %s  Grade: %s""" % (r[0], r[1])

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
    if tokens:
        command = tokens[0]
    args = []
    temp = None


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()



        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(" ".join(args))
        elif command == "give_grade":
            give_grade_to_student(*args)
        elif command == "get_grades_for_project":
            get_all_grades_for_project(" ".join(args))
        elif command == "get_grades_by_github":
            get_grades_by_github(*args)
        elif command == "get_grades_by_name":
            get_grades_by_name(*args)
        elif command == "new_project":
            make_new_project(args[0], " ".join(args[1:-1]),int(args[-1]))

    CONN.close()

if __name__ == "__main__":
    main()
