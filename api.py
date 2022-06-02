from flask import Flask, request, render_template, flash
import json
import sqlite3
import sys
import re

from config import config

app = Flask(__name__)

# Database Connection
conn = sqlite3.connect('./database/database.db', check_same_thread=False)
cur = conn.cursor()

# State of the API
state = "Teacher"

# API Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login/login.html')
    else:
        flag = False

        try:
            username = request.form.get('user_name')
            password = request.form.get('pwd')

            sql_query = f"SELECT * FROM user WHERE user_email = '{username}' AND user_pwd = '{password}';"
            cur.execute(sql_query)
            result = cur.fetchall()

            if len(result) == 1:
                flag = True

            if flag:
                global state
                state = result[0][4]
                if state == "Student":
                    return render_template('dashboard/dashboard_student.html')
                elif state == "Teacher":
                    return render_template('dashboard/dashboard_teacher.html')
                elif state == "Admin":
                    return render_template('dashboard/dashboard_admin.html')
            else:
                return render_template('login/login.html')            
        except Exception as e:
            print(e)
            return render_template('login/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('login/signup.html')
    else:
        try:
            fullname = request.form.get('full_name')
            email = request.form.get('email')
            id_ = int(request.form.get('id'))
            pwd = request.form.get('pwd')
            pwd_confirm = request.form.get('confirm_pwd')
            account = request.form.get('account_type')
            a1 = request.form.get('security_question_1')
            a2 = request.form.get('security_question_2')
            a3 = request.form.get('security_question_3')

            correct_entry_flag = False
            unique_flag = False

            # Verify password
            # Verify confirmed password
            # Verify email
            # Verify id
            correct_entry_flag = verify_email(email) and verify_id(id_) and verify_confirmed_password(pwd, pwd_confirm) and verify_password(pwd)

            # Check if entries is unique
            unique_flag = verify_unqiue_entries(email, id_)

            if correct_entry_flag and unique_flag:
                sql_query = f"INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES ('{id_}', '{fullname}', '{email}', '{pwd}', '{account}', '{a1}', '{a2}', '{a3}');"
                cur.execute(sql_query)
                conn.commit()

                return render_template('login/login.html')
            else:
                return render_template('login/signup.html')
        except Exception as e:
            print(e)
            return render_template('login/signup.html')

def verify_email(email):
    pattern = re.compile("[a-z0-9]+@[a-z]+\.edu")
    return bool(pattern.match(email))

def verify_id(id_):
    return type(id_) == int

def verify_password(pwd):
    pattern = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{5,}$")
    return bool(pattern.match(pwd)) 

def verify_confirmed_password(pwd, pwd_confirm):
    return pwd == pwd_confirm

def verify_unqiue_entries(email, id_):
    sql_query = f"SELECT * FROM user WHERE user_email = '{email}';"
    cur.execute(sql_query)
    r1 = cur.fetchall()

    sql_query = f"SELECT * FROM user WHERE u_id = '{id_}';"
    cur.execute(sql_query)
    r2 = cur.fetchall()

    return len(r1) == 0 and len(r2) == 0

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
