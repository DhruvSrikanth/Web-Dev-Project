DROP TABLE IF EXISTS user;
CREATE TABLE user (
    u_id INT NOT NULL,
    user_full_name VARCHAR(64),
    user_email VARCHAR(64) UNIQUE NOT NULL,
    user_pwd VARCHAR(64),
    user_type VARCHAR(64),
    user_a1 VARCHAR(64),
    user_a2 VARCHAR(64),
    user_a3 VARCHAR(64),
    active BOOLEAN DEFAULT FALSE,

    PRIMARY KEY (u_id)
);


DROP TABLE IF EXISTS course;
CREATE TABLE course (
    course_id INT NOT NULL,
    course_name VARCHAR(64),
    course_desc VARCHAR(1024),
    course_capacity INT,
    course_teacher INT,

    FOREIGN KEY (course_teacher) REFERENCES user(u_id) ON UPDATE CASCADE,
    PRIMARY KEY (course_id)
);


DROP TABLE IF EXISTS announcement;
CREATE TABLE announcement (
    announcement_id INT NOT NULL,
    announcement_title VARCHAR(64),
    announcement_desc VARCHAR(1024),
    announcement_date_time TEXT,

    PRIMARY KEY (announcement_id)
);


DROP TABLE IF EXISTS assignment;
CREATE TABLE assignment (
    assignment_id INT NOT NULL,
    assignment_title VARCHAR(64),
    assignment_desc VARCHAR(1024),
    assignment_total_points INT,
    assignment_post_date TEXT,
    assignment_due_date TEXT,

    PRIMARY KEY (assignment_id)
);


DROP TABLE IF EXISTS user_course;
CREATE TABLE user_course (
    u_id INT NOT NULL,
    course_id INT NOT NULL,

    FOREIGN KEY (u_id) REFERENCES user(u_id) ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    PRIMARY KEY(u_id, course_id)
);


DROP TABLE IF EXISTS course_announcement;
CREATE TABLE course_announcement (
    announcement_id INT NOT NULL,
    course_id INT NOT NULL,

    FOREIGN KEY (announcement_id) REFERENCES announcement(announcement_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    PRIMARY KEY(course_id, announcement_id)
);


DROP TABLE IF EXISTS course_assignment;
CREATE TABLE course_assignment (
    course_id INT NOT NULL,
    assignment_id INT NOT NULL,

    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    PRIMARY KEY(course_id, assignment_id)
);


DROP TABLE IF EXISTS user_assignment;
CREATE TABLE user_assignment (
    u_id INT NOT NULL,
    assignment_id INT NOT NULL,
    assignment_submission_flag BOOLEAN DEFAULT FALSE,
    assignment_submission VARCHAR(1024) DEFAULT "Assignment not submitted!",
    assignment_grade VARCHAR(64) DEFAULT "Not graded yet!",

    FOREIGN KEY (assignment_id) REFERENCES assignment(assignment_id),
    FOREIGN KEY (u_id) REFERENCES user(u_id) ON UPDATE CASCADE,
    PRIMARY KEY(u_id, assignment_id)
);