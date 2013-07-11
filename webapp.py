from flask import Flask, render_template, request

import hackbright_app

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)