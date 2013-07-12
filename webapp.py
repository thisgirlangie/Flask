from flask import Flask, render_template, request

import hackbright_app

app = Flask(__name__)

# FRONTPAGE
@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github") # diff from chriszf example is he has "student" instead of "github" passed as variable
    rows = hackbright_app.get_grades_by_github(student_github)
    html = render_template("student_info.html", github=student_github, project=rows[0], grades=rows)
    return html

@app.route("/students_and_grades")
def get_students_and_grades_for_project():
    hackbright_app.connect_to_db()
    project = request.args.get("project") # goal is to fetch grades for project
    rows = hackbright_app.get_all_grades_for_project(project)
    html = render_template("students_and_grades.html", project=project, grades=rows)
    return html

# ADD STUDENT
@app.route("/student_add")
def display_add_student_form():
    html = render_template("student_add.html")
    return html

@app.route("/student_add_create")
def add_student():
    hackbright_app.connect_to_db()
    first = request.args.get("first")
    last = request.args.get("last")
    github = request.args.get("github")
    row = hackbright_app.make_new_student(first, last, github)
    html = render_template("student_added.html")
    return html

# ADD PROJECT
@app.route("/project_add")
def display_add_project_form():
    html = render_template("project_add.html")
    return html

@app.route("/project_add_create")
def add_project():
    hackbright_app.connect_to_db()
    project = request.args.get("project")
    project_desc = request.args.get("project_desc")
    max_grade = request.args.get("max_grade")
    row = hackbright_app.make_new_project(project, project_desc, max_grade)
    html = render_template("project_added.html")
    return html

# ADD GRADE
@app.route("/grade_add")
def display_add_grade_form():
    html = render_template("grade_add.html")
    return html

@app.route("/grade_add_create")
def add_grade():
    hackbright_app.connect_to_db()
    github = request.args.get("github")
    project = request.args.get("project")
    grade = request.args.get("grade")
    row = hackbright_app.give_grade_to_student(github, project, grade)
    html = render_template("grade_added.html")
    return html

if __name__ == "__main__":
    app.run(debug=True)