from flask import Flask, request, render_template, flash
from datetime import datetime, timedelta
from pytz import timezone
from config import config

import sqlite3
import re



app = Flask(__name__, static_folder='static')

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
                    # Get assignments for user
                    sql_query = f"SELECT * FROM assignment JOIN user_assignment ON assignment.assignment_id = user_assignment.assignment_id WHERE u_id = '{user_id_}';"
                    cur.execute(sql_query)
                    user_assignments = cur.fetchall()

                    tz = timezone(config['timezone'])
                    time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                    time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
                    time_now_plus_3days = time_now + timedelta(days=3)

                    # Assignments that are due in 3 days
                    assignments_to_do = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') >= time_now and datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') <= time_now_plus_3days and not bool(x[8]), user_assignments))

                    # Assignments that are after 3 days
                    assignments_upcoming = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') > time_now_plus_3days and not bool(x[8]), user_assignments))

                    # passed due assignments
                    assignments_past = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') < time_now, user_assignments))

                    return render_template('dashboard/dashboard_student.html', assignments_to_do=assignments_to_do, assignments_upcoming=assignments_upcoming, assignments_past=assignments_past)
                elif state == "Teacher":
                    # Get assigntments that need grading (past)
                    sql_query = f"SELECT course_name, assignment_title, user_full_name, assignment_due_date FROM assignment JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id JOIN user_assignment ON user_assignment.assignment_id = course_assignment.assignment_id JOIN course ON course.course_id = course_assignment.course_id JOIN user ON user.u_id = user_assignment.u_id WHERE course_teacher = '{user_id_}' AND assignment_grade = 'Not graded yet!';"
                    cur.execute(sql_query)
                    assignments_to_grade = cur.fetchall()

                    tz = timezone(config['timezone'])
                    time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
                    time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')

                    

                    # passed due assignments
                    assignments_to_grade = list(filter(lambda x: datetime.strptime(x[3], '%Y-%m-%d %H:%M:%S') < time_now, assignments_to_grade))
                    course_names = sorted(list(set([x[0] for x in assignments_to_grade])))

                    assignments_to_grade_new = {}
                    assignments_to_grade_new = {x:[] for x in course_names}
                    for x in assignments_to_grade:
                        assignments_to_grade_new[x[0]].append(x[1:])

                    for x in assignments_to_grade_new:
                        assignments_to_grade_new[x] = sorted(assignments_to_grade_new[x], key=lambda x: x[0])
                    
                    assignments_to_grade_final = []
                    for x in assignments_to_grade_new:
                        for y in assignments_to_grade_new[x]:
                            element = [x]
                            element.extend(list(y))
                            assignments_to_grade_final.append(element)

                    return render_template('dashboard/dashboard_teacher.html', assignments_to_grade=assignments_to_grade_final, course_names=course_names)
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
    global user_id_
    if state == "Student":
        # Get assignments for user
        sql_query = f"SELECT * FROM assignment JOIN user_assignment ON assignment.assignment_id = user_assignment.assignment_id WHERE u_id = '{user_id_}';"
        cur.execute(sql_query)
        user_assignments = cur.fetchall()

        tz = timezone(config['timezone'])
        time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')
        time_now_plus_3days = time_now + timedelta(days=3)

        # Assignments that are due in 3 days
        assignments_to_do = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') >= time_now and datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') <= time_now_plus_3days and not bool(x[8]), user_assignments))

        # Assignments that are after 3 days
        assignments_upcoming = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') > time_now_plus_3days and not bool(x[8]), user_assignments))

        # passed due assignments
        assignments_past = list(filter(lambda x: datetime.strptime(x[5], '%Y-%m-%d %H:%M:%S') < time_now, user_assignments))

        return render_template('dashboard/dashboard_student.html', assignments_to_do=assignments_to_do, assignments_upcoming=assignments_upcoming, assignments_past=assignments_past)

    elif state == "Teacher":
        # Get assigntments that need grading (past)
        sql_query = f"SELECT course_name, assignment_title, user_full_name, assignment_due_date FROM assignment JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id JOIN user_assignment ON user_assignment.assignment_id = course_assignment.assignment_id JOIN course ON course.course_id = course_assignment.course_id JOIN user ON user.u_id = user_assignment.u_id WHERE course_teacher = '{user_id_}' AND assignment_grade = 'Not graded yet!';"
        cur.execute(sql_query)
        assignments_to_grade = cur.fetchall()

        tz = timezone(config['timezone'])
        time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')

        # passed due assignments
        assignments_to_grade = list(filter(lambda x: datetime.strptime(x[3], '%Y-%m-%d %H:%M:%S') < time_now, assignments_to_grade))
        course_names = sorted(list(set([x[0] for x in assignments_to_grade])))

        assignments_to_grade_new = {}
        assignments_to_grade_new = {x:[] for x in course_names}
        for x in assignments_to_grade:
            assignments_to_grade_new[x[0]].append(x[1:])

        for x in assignments_to_grade_new:
            assignments_to_grade_new[x] = sorted(assignments_to_grade_new[x], key=lambda x: x[0])
        
        assignments_to_grade_final = []
        for x in assignments_to_grade_new:
            for y in assignments_to_grade_new[x]:
                element = [x]
                element.extend(list(y))
                assignments_to_grade_final.append(element)

        return render_template('dashboard/dashboard_teacher.html', assignments_to_grade=assignments_to_grade_final, course_names=course_names)
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

@app.route('/course/<id_>/assignments', methods=['GET', 'POST'])
def assignments(id_):

    global state
    global user_id_
    if state == "Student":
        if request.method == 'GET':
    
            new_assignments = []

            sql_query = f"SELECT assignment.assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date, assignment_submission_flag FROM assignment JOIN user_assignment ON user_assignment.assignment_id = assignment.assignment_id JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id WHERE course_assignment.course_id = '{id_}' AND user_assignment.u_id = '{user_id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()

            tz = timezone(config['timezone'])
            time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')

            for assignment in assignments:
                due_date = assignment[5]
                due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
                if due_date > time_now:
                    new_assignments.append(assignment)


            return render_template('assignments/assignments_student.html', assignments = new_assignments, id_ = id_)
        
    elif state == "Teacher":
        if request.method == 'GET':
            sql_query = f"SELECT * FROM assignment JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id WHERE course_assignment.course_id = '{id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()
            return render_template('assignments/assignments_teacher.html', assignments = assignments, id_ = id_)
        else:
            assignment_name = request.form.get('assign_name')
            assignment_desc = request.form.get('desc')
            assignment_total_points = request.form.get('points')
            assignment_due_date = request.form.get('due_date')
            assignment_due_date = " ".join((assignment_due_date + ":00").split("T"))

            tz = timezone(config['timezone'])
            assignment_post_date = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

            sql_query = "SELECT assignment_id FROM assignment;"
            cur.execute(sql_query)
            assignment_ids = cur.fetchall()
            assignment_id = len(assignment_ids) + 1

            # Update assignment table
            sql_query = f"INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES ({assignment_id}, '{assignment_name}', '{assignment_desc}', {assignment_total_points}, '{assignment_post_date}', '{assignment_due_date}');"
            cur.execute(sql_query)
            conn.commit()

            # Update course_assignment table
            sql_query = f"INSERT INTO course_assignment (course_id, assignment_id) VALUES ({id_}, '{assignment_id}');"
            cur.execute(sql_query)
            conn.commit()

            # Update user_assignment table
            sql_query = f"SELECT u_id FROM user_course WHERE course_id = '{id_}';"
            cur.execute(sql_query)
            user_ids = cur.fetchall()
            user_ids = [x[0] for x in user_ids]

            for u_id in user_ids:
                sql_query = f"INSERT INTO user_assignment (u_id, assignment_id) VALUES ('{u_id}', '{assignment_id}');"
                cur.execute(sql_query)
                conn.commit()

            sql_query = f"SELECT * FROM assignment JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id WHERE course_assignment.course_id = '{id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()
            
            return render_template('assignments/assignments_teacher.html', assignments = assignments, id_ = id_)


@app.route('/course/<id_>/assignment/<assign_id>', methods=['GET', 'POST'])
def assignment(id_, assign_id):
    global state
    global user_id_
    if state == "Student":
        if request.method == 'GET':
            sql_query = f"SELECT * FROM assignment WHERE assignment_id = '{assign_id}';"
            cur.execute(sql_query)
            assignment = cur.fetchall()
            return render_template('assignments/assignment_student.html', assignment = assignment, id_ = id_, assign_id = assign_id)
        else:
            assignment_answer = request.form.get('answer')
            sql_query = f"UPDATE user_assignment SET assignment_submission = '{assignment_answer}', assignment_submission_flag = True WHERE assignment_id = '{assign_id}' AND u_id = '{user_id_}';"
            print(sql_query)
            cur.execute(sql_query)
            conn.commit()

            new_assignments = []

            sql_query = f"SELECT assignment.assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date, assignment_submission_flag FROM assignment JOIN user_assignment ON user_assignment.assignment_id = assignment.assignment_id JOIN course_assignment ON course_assignment.assignment_id = assignment.assignment_id WHERE course_assignment.course_id = '{id_}' AND user_assignment.u_id = '{user_id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()

            tz = timezone(config['timezone'])
            time_now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            time_now = datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S')

            for assignment in assignments:
                due_date = assignment[5]
                due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
                if due_date > time_now:
                    new_assignments.append(assignment)

            return render_template('assignments/assignments_student.html', assignments = new_assignments, id_ = id_)

@app.route('/course/<id_>/grades', methods=['GET', 'POST'])
def grades(id_):
    global state
    global user_id_
    if state == "Student":
        if request.method == 'GET':
            sql_query = f"SELECT assignment_title, assignment_grade, assignment_total_points FROM user_assignment JOIN course_assignment ON course_assignment.assignment_id = user_assignment.assignment_id JOIN assignment ON assignment.assignment_id = course_assignment.assignment_id WHERE course_assignment.course_id = '{id_}' AND user_assignment.u_id = '{user_id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()

            return render_template('grades/grades_students.html', assignments = assignments, id_ = id_)
    elif state == "Teacher":
        if request.method == 'GET':
            sql_query = f"SELECT assignment_title, user_full_name, assignment_submission, assignment_grade, assignment_total_points, assignment.assignment_id, user.u_id FROM user_assignment JOIN course_assignment ON course_assignment.assignment_id = user_assignment.assignment_id JOIN assignment ON assignment.assignment_id = course_assignment.assignment_id JOIN user ON user_assignment.u_id = user.u_id WHERE course_assignment.course_id = '{id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()

            assignments = sorted(assignments, key=lambda x: x[0])
            assignment_names = sorted(list(set([x[0] for x in assignments])))

            return render_template('grades/grades_teacher.html', id_ = id_, assignments = assignments, assignment_names = assignment_names)
        else:
            # Get information to update grade
            assignment_grade = int(request.form.get('edit_grade'))
            assignment_id = int(request.form.get('assignment_id'))
            user_id = int(request.form.get('user_id'))

            # Update user_assignment table
            sql_query = f"UPDATE user_assignment SET assignment_grade = '{assignment_grade}' WHERE assignment_id = '{assignment_id}' AND u_id = '{user_id}';"
            cur.execute(sql_query)
            conn.commit()


            # Get the same as before for reloading page
            sql_query = f"SELECT assignment_title, user_full_name, assignment_submission, assignment_grade, assignment_total_points, assignment.assignment_id, user.u_id FROM user_assignment JOIN course_assignment ON course_assignment.assignment_id = user_assignment.assignment_id JOIN assignment ON assignment.assignment_id = course_assignment.assignment_id JOIN user ON user_assignment.u_id = user.u_id WHERE course_assignment.course_id = '{id_}';"
            cur.execute(sql_query)
            assignments = cur.fetchall()

            assignments = sorted(assignments, key=lambda x: x[0])
            assignment_names = sorted(list(set([x[0] for x in assignments])))

            return render_template('grades/grades_teacher.html', id_ = id_, assignments = assignments, assignment_names = assignment_names)

@app.route('/myaccount', methods=['GET'])
def myaccount():
    global state
    global user_id_

    admin_flag = state == "Admin"

    sql_query = f"SELECT user_full_name, user_email, u_id FROM user WHERE u_id = '{user_id_}';"
    cur.execute(sql_query)
    user_information = cur.fetchall()
    user_information = user_information[0]

    return render_template('myaccount/myaccount.html', user_information = user_information, admin_flag = admin_flag)
    
@app.route('/myaccount/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    global state
    global user_id_
    admin_flag = state == "Admin"
    
    if request.method == 'GET':

        return render_template('/myaccount/myaccount_edit_profile.html', admin_flag = admin_flag)

    else:
        user_name = request.form.get('full_name')
        user_email = request.form.get('email')
        user_id = int(request.form.get('id'))

        sql_query = f"SELECT u_id FROM user;"
        cur.execute(sql_query)
        user_ids = cur.fetchall()
        
        user_ids = [int(x[0]) for x in user_ids]
        unique_flag = user_id not in user_ids

        valid_information_flag = verify_email(user_email) and verify_id(user_id) and unique_flag
        
        if valid_information_flag:
            sql_query = f"UPDATE user SET user_full_name = '{user_name}', user_email = '{user_email}', u_id = '{user_id}' WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            conn.commit()

            if state == "Teacher":
                sql_query = f"UPDATE course SET course_teacher = '{user_id}' WHERE course_teacher = '{user_id_}';"
                cur.execute(sql_query)
                conn.commit()
            elif state == "Student":
                sql_query = f"UPDATE user_course SET u_id = '{user_id}' WHERE u_id = '{user_id_}';"
                cur.execute(sql_query)
                conn.commit()

                sql_query = f"UPDATE user_assignment SET u_id = '{user_id}' WHERE u_id = '{user_id_}';"
                cur.execute(sql_query)
                conn.commit()

            user_id_ = user_id
            sql_query = f"SELECT user_full_name, user_email, u_id FROM user WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            user_information = cur.fetchall()
            user_information = user_information[0]

            
            return render_template('myaccount/myaccount.html', user_information = user_information, admin_flag = admin_flag)
        else:
            return render_template('myaccount/myaccount_edit_profile.html', admin_flag = admin_flag)

@app.route('/myaccount/change_password', methods=['GET', 'POST'])
def change_password():
    global state
    global user_id_
    
    admin_flag = state == "Admin"

    if request.method == 'GET':
        return render_template('myaccount/myaccount_change_password.html', admin_flag = admin_flag)
    else:
        old_password = request.form.get('current_pwd')
        new_password = request.form.get('new_pwd')
        new_password_confirm = request.form.get('confirm_pwd')

        sql_query = f"SELECT user_pwd FROM user WHERE u_id = '{user_id_}';"
        cur.execute(sql_query)
        user_pwd = cur.fetchall()
        user_pwd = user_pwd[0][0]

        old_password_flag = old_password == user_pwd
        valid_password_flag = verify_password(new_password) and verify_password(new_password_confirm) and verify_confirmed_password(new_password, new_password_confirm)

        if old_password_flag and valid_password_flag:

            #Update user_pwd
            sql_query = f"UPDATE user SET user_pwd = '{new_password}' WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            conn.commit()

            sql_query = f"SELECT user_full_name, user_email, u_id FROM user WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            user_information = cur.fetchall()
            user_information = user_information[0]

            return render_template('myaccount/myaccount.html', user_information = user_information, admin_flag = admin_flag)
        
        else:

            return render_template('myaccount/myaccount_change_password.html', admin_flag = admin_flag)

@app.route('/myaccount/change_sec_questions', methods=['GET', 'POST'])
def change_sec_questions():
    global state
    global user_id_
    
    admin_flag = state == "Admin"
    if request.method == 'GET':
        return render_template('myaccount/myaccount_change_sec_questions.html', admin_flag  = admin_flag)
    else:
        current_password = request.form.get('current_pwd')
        a1 = request.form.get('security_question_1')
        a2 = request.form.get('security_question_2')
        a3 = request.form.get('security_question_3')

        sql_query = f"SELECT user_pwd FROM user WHERE u_id = '{user_id_}';"
        cur.execute(sql_query)
        user_pwd = cur.fetchall()
        user_pwd = user_pwd[0][0]

        valid_password_flag = current_password == user_pwd

        if valid_password_flag:
            # Update user security questions
            sql_query = f"UPDATE user SET user_a1 = '{a1}', user_a2 = '{a2}', user_a3 = '{a3}' WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            conn.commit()

            # Get user information
            sql_query = f"SELECT user_full_name, user_email, u_id FROM user WHERE u_id = '{user_id_}';"
            cur.execute(sql_query)
            user_information = cur.fetchall()
            user_information = user_information[0]

            return render_template('myaccount/myaccount.html', user_information = user_information, admin_flag = admin_flag)
        else:
            return render_template('myaccount/myaccount_change_sec_questions.html', admin_flag  = admin_flag)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    global state
    global user_id_

    if state == "Admin":
        if request.method == 'GET':
            sql_query = f"SELECT u_id, user_full_name, user_email, active, user_type FROM user;"
            cur.execute(sql_query)
            user_information = cur.fetchall()

            for i in range(len(user_information)):
                user_information[i] = list(user_information[i])
                if user_information[i][3] == "True":
                    user_information[i][3] = 'Active'
                else:
                    user_information[i][3] = 'Inactive'
            
            sql_query = f"SELECT course_id, course_name FROM course;"
            cur.execute(sql_query)
            courses = cur.fetchall()

            return render_template('settings/settings.html', user_information = user_information, courses = courses)
        else:
            action_desc = request.form.get('action_desc')
            user_id = int(request.form.get('user_id'))
            if action_desc == 'toggle':
                sql_query = f"SELECT active FROM user WHERE u_id = '{user_id}';"
                cur.execute(sql_query)
                active = cur.fetchall()
                active = False if active[0][0] == "False" else True
                active = not active

                sql_query = f"UPDATE user SET active = '{active}' WHERE u_id = {user_id};"
                cur.execute(sql_query)
                conn.commit()
            else:
                course_id = int(request.form.get('courses'))

                sql_query = f"SELECT course_id FROM user_course WHERE u_id = '{user_id}';"
                cur.execute(sql_query)
                user_courses = cur.fetchall()
                user_courses = [int(x[0]) for x in user_courses]
                if course_id not in user_courses:
                    sql_query = f"INSERT INTO user_course (u_id, course_id) VALUES ('{user_id}', '{course_id}');"
                    cur.execute(sql_query)
                    conn.commit()




            sql_query = f"SELECT u_id, user_full_name, user_email, active, user_type FROM user;"
            cur.execute(sql_query)
            user_information = cur.fetchall()

            for i in range(len(user_information)):
                user_information[i] = list(user_information[i])
                if user_information[i][3] == "True":
                    user_information[i][3] = 'Active'
                else:
                    user_information[i][3] = 'Inactive'
            
            sql_query = f"SELECT course_id, course_name FROM course;"
            cur.execute(sql_query)
            courses = cur.fetchall()

            return render_template('settings/settings.html', user_information = user_information, courses = courses)


# Helper Functions



if __name__ == '__main__':
    app.run(host=config['host'], 
            port=config['port'], 
            debug=config['debug'])
