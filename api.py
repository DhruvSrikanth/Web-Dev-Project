from flask import Flask, request, render_template
import json
import sqlite3
import sys

from config import config

app = Flask(__name__)

# Database Connection
# conn = sqlite3.connect('')
# cur = conn.cursor()

state = "Teacher"

@app.route('/', methods=['GET'])
def login():
    return render_template('login/login.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('login/signup.html')

@app.route('/forgot', methods=['GET'])
def forgot():
    return render_template('login/forget_pwd.html')

@app.route('/newpwd', methods=['GET'])
def new_pwd():
    return render_template('login/new_pwd.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    global state
    if state == "Student":
        return render_template('dashboard/dashboard_student.html')
    elif state == "Teacher":
        return render_template('dashboard/dashboard_teacher.html')
    elif state == "Admin":
        return render_template('dashboard/dashboard_admin.html')

@app.route('/courses', methods=['GET'])
def courses():
    if state == "Teacher" or state == "Student":
        return render_template('courses/courses.html')
    elif state == "Admin":
        return render_template('courses/courses_admin.html')

@app.route('/course', methods=['GET'])
def course():
    if state == "Student":
        return render_template('courses/course_student.html')
    elif state == "Teacher":
        return render_template('courses/course_teacher.html')

@app.route('/course/announcement', methods=['GET'])
def announcements():
    global state
    if state == "Student":
        return render_template('announcements/announcements_student.html')
    elif state == "Teacher":
        return render_template('announcements/announcements_teacher.html')

@app.route('/course/assignments', methods=['GET'])
def assignments():
    global state
    if state == "Student":
        return render_template('assignments/assignments_student.html')
    elif state == "Teacher":
        return render_template('assignments/assignments_teacher.html')

@app.route('/course/assignment', methods=['GET'])
def assignment():
    global state
    if state == "Student":
        return render_template('assignments/assignment_student.html')

@app.route('/course/grades', methods=['GET'])
def grades():
    global state
    if state == "Student":
        return render_template('grades/grades_students.html')
    elif state == "Teacher":
        return render_template('grades/grades_teacher.html')

@app.route('/course/grade', methods=['GET'])
def grade():
    global state
    if state == "Teacher":
        return render_template('grades/grade_teacher.html')

@app.route('/myaccount', methods=['GET'])
def myaccount():
    global state
    if state == "Student" or state == "Teacher":
        return render_template('myaccount/myaccount.html')
    else:
        return render_template('myaccount/myaccount_admin.html')

@app.route('/myaccount/edit_profile', methods=['GET'])
def edit_profile():
    global state
    if state == "Student" or state == "Teacher":
        return render_template('myaccount/myaccount_edit_profile.html')
    else:
        return render_template('myaccount/myaccount_edit_profile_admin.html')

@app.route('/myaccount/change_password', methods=['GET'])
def change_password():
    global state
    if state == "Student" or state == "Teacher":
        return render_template('myaccount/myaccount_change_password.html')
    else:
        return render_template('myaccount/myaccount_change_password_admin.html')

@app.route('/myaccount/change_sec_questions', methods=['GET'])
def change_sec_questions():
    global state
    if state == "Student" or state == "Teacher":
        return render_template('myaccount/myaccount_change_sec_questions.html')
    else:
        return render_template('myaccount/myaccount_change_sec_questions_admin.html')

@app.route('/settings', methods=['GET'])
def settings():
    global state
    if state == "Admin":
        return render_template('settings/settings.html')


if __name__ == '__main__':
    app.run(host=config['host'], 
            port=config['port'], 
            debug=config['debug'])
