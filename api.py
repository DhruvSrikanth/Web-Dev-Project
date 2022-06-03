from flask import Flask, request, render_template, flash
from datetime import datetime
from pytz import timezone
from config import config

import sqlite3
import re



app = Flask(__name__)

# Database Connection
conn = sqlite3.connect('./database/database.db', check_same_thread=False)
cur = conn.cursor()

# State of the API
state = "None"

# ID of user
user_id_ = -1

# Login API
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
                global user_id_
                user_id_ = result[0][0]

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

# Signup API
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('login/signup.html')
    else:
        try:
            fullname = request.form.get('full_name')
            fullname = ' '.join(map(str.capitalize, fullname.split(' ')))
            email = request.form.get('email')
            id_ = int(request.form.get('id'))
            pwd = request.form.get('pwd')
            pwd_confirm = request.form.get('confirm_pwd')
            account = request.form.get('account_type').capitalize()
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

# Signup Helper Functions
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

# Forgot Password API
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'GET':
        return render_template('login/forget_pwd.html')
    else:
        try:
            email = request.form.get('email')
            a1 = request.form.get('security_question_1')
            a2 = request.form.get('security_question_2')
            a3 = request.form.get('security_question_3')

            sql_query = f"SELECT * FROM user WHERE user_email = '{email}' AND user_a1 = '{a1}' AND user_a2 = '{a2}' AND user_a3 = '{a3}';"
            cur.execute(sql_query)
            result = cur.fetchall()


            if len(result) == 1:
                return render_template('login/new_pwd.html')
            else:
                return render_template('login/forget_pwd.html')

        except Exception as e:
            print(e)
            return render_template('login/forget_pwd.html')

# New Password API
@app.route('/newpwd', methods=['GET', 'POST'])
def new_pwd():
    if request.method == 'GET':
        return render_template('login/new_pwd.html')
    else:
        try:
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            pwd_confirm = request.form.get('confirm_pwd')


            sql_query = f"SELECT * FROM user WHERE user_email = '{email}';"
            cur.execute(sql_query)
            result = cur.fetchall()

            unique_flag = len(result) == 1
            correct_email_flag = verify_email(email) and unique_flag
            correct_password_flag = verify_confirmed_password(pwd, pwd_confirm) and verify_password(pwd)

            if correct_password_flag and correct_email_flag:
                sql_query = f"UPDATE user SET user_pwd = '{pwd}' WHERE user_email='{email}';"
                cur.execute(sql_query)
                conn.commit()

                return render_template('login/login.html')
            else:
                return render_template('login/new_pwd.html')
        except Exception as e:
            print(e)
            return render_template('login/new_pwd.html')

# Dashboard API
@app.route('/dashboard', methods=['GET'])
def dashboard():
    global state
    if state == "Student":
        return render_template('dashboard/dashboard_student.html')
    elif state == "Teacher":
        return render_template('dashboard/dashboard_teacher.html')
    elif state == "Admin":
        return render_template('dashboard/dashboard_admin.html')

@app.route('/courses', methods=['GET', 'POST'])
def courses():
    global state
    global user_id_
    if state == "Student":
        sql_query = f"SELECT course_name, course.course_id FROM course JOIN user_course ON course.course_id = user_course.course_id WHERE user_course.u_id = '{user_id_}';"
        cur.execute(sql_query)
        courses = cur.fetchall()

        return render_template('courses/courses.html', courses=courses)

    elif state == "Teacher":
        sql_query = f"SELECT course_name, course_id FROM course WHERE course_teacher = '{user_id_}';"
        cur.execute(sql_query)
        courses = cur.fetchall()

        return render_template('courses/courses.html', courses=courses)

    elif state == "Admin":
        if request.method == 'GET':
            sql_query = f"SELECT course_name, course_id FROM course;"
            cur.execute(sql_query)
            courses = cur.fetchall()
            
            sql_query = f"SELECT user_full_name, u_id FROM user WHERE user_type = 'Teacher';"
            cur.execute(sql_query)
            teachers = cur.fetchall()

            return render_template('courses/courses_admin.html', courses=courses, teachers=teachers)
        else:
            course_name = request.form.get('name')
            course_teacher = request.form.get('teacher')
            course_desc = request.form.get('desc')
            course_capacity = int(request.form.get('capacity'))

            sql_query = "SELECT course_id FROM course;"
            cur.execute(sql_query)
            course_ids = cur.fetchall()
            course_id = len(course_ids) + 1
            
            sql_query = f"INSERT INTO course (course_id, course_name, course_desc, course_capacity, course_teacher) VALUES ('{course_id}', '{course_name}', '{course_desc}', {course_capacity}, {course_teacher});"
            cur.execute(sql_query)
            conn.commit()

            sql_query = f"SELECT course_name, course_id FROM course;"
            cur.execute(sql_query)
            courses = cur.fetchall()
            
            sql_query = f"SELECT user_full_name, u_id FROM user WHERE user_type = 'Teacher';"
            cur.execute(sql_query)
            teachers = cur.fetchall()

            return render_template('courses/courses_admin.html', courses=courses, teachers=teachers)

@app.route('/course/<id>', methods=['GET'])
def course(id):
    global state
    global user_id_

    if state == "Student":
        sql_query = f"SELECT * FROM course WHERE course_id = '{id}';"
        cur.execute(sql_query)
        course = cur.fetchall()

        return render_template('courses/course_student.html', course=course)
    elif state == "Teacher":
        sql_query = f"SELECT * FROM course WHERE course_id = '{id}';"
        cur.execute(sql_query)
        course = cur.fetchall()

        sql_query = f"SELECT * FROM course WHERE course_id = '{id}';"
        return render_template('courses/course_teacher.html', course=course)

@app.route('/course/<id_>/announcement', methods=['GET', 'POST'])
def announcements(id_):
    global state
    global user_id_
    if state == "Student":

        sql_query = f"SELECT * FROM announcement JOIN course_announcement ON announcement.announcement_id = course_announcement.announcement_id WHERE course_announcement.course_id = '{id_}';"
        cur.execute(sql_query)
        announcements = cur.fetchall()

        return render_template('announcements/announcements_student.html', announcements=announcements, id_ = id_)
    elif state == "Teacher":
        if request.method == 'GET':
            sql_query = f"SELECT * FROM announcement JOIN course_announcement ON announcement.announcement_id = course_announcement.announcement_id WHERE course_announcement.course_id = '{id_}';"
            cur.execute(sql_query)
            announcements = cur.fetchall()

            return render_template('announcements/announcements_teacher.html', announcements=announcements, id_ = id_)
        else:
            announcement_title = request.form.get('title')
            announcement_desc = request.form.get('desc')

            tz = timezone(config['timezone'])
            current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

            sql_query = "SELECT announcement_id FROM announcement;"
            cur.execute(sql_query)
            announcement_ids = cur.fetchall()
            announcement_id = len(announcement_ids) + 1
            
            sql_query = f"INSERT INTO announcement (announcement_id, announcement_title, announcement_desc, announcement_date_time) VALUES ('{announcement_id}', '{announcement_title}', '{announcement_desc}', '{current_time}');"
            cur.execute(sql_query)
            conn.commit()

            sql_query = f"INSERT INTO  course_announcement (course_id, announcement_id) VALUES ('{id_}','{announcement_id}');"
            cur.execute(sql_query)
            conn.commit()

            sql_query = f"SELECT * FROM announcement JOIN course_announcement ON announcement.announcement_id = course_announcement.announcement_id WHERE course_announcement.course_id = '{id_}';"
            cur.execute(sql_query)
            announcements = cur.fetchall()
            return render_template('announcements/announcements_teacher.html', announcements=announcements, id_ = id_)

@app.route('/course/<id_>/assignments', methods=['GET'])
def assignments(id_):

    global state
    global user_id_
    if state == "Student":

        sql_query = f"SELECT assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date, assignment_submission_flag FROM assignment JOIN user_assignment ON user_assignment.assignment_id = assignment.assignment_id JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id WHERE course_assignment.course_id = '{id_}' AND user_assignment.u_id = '{user_id_}';"
        cur.execute(sql_query)
        assignments = cur.fetchall()

        return render_template('assignments/assignments_student.html', assignments = assignments, id_ = id_)
    elif state == "Teacher":
        return render_template('assignments/assignments_teacher.html')

@app.route('/course/<id_>/assignment/<assign_id>', methods=['GET', 'POST'])
def assignment(id_, assign_id):
    global state
    global user_id_
    if state == "Student":
        if request.method == 'GET':
            sql_query = f"SELECT * FROM assignment WHERE assignment_id = '{assign_id}';"
            cur.execute(sql_query)
            assignment = cur.fetchall()
            return render_template('assignments/assignment_student.html', assignment = assignment, id_ = id_)
        else:
            assignment_answer = request.form.get('answer')
            sql_query = f"UPDATE user_assignment SET assignment_submission = '{assignment_answer}' WHERE ;"
            cur.execute(sql_query)
            assignment = cur.fetchall()

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
