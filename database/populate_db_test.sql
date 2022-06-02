--user 
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (1, 'John Smith', 'jsmith@uchicago.edu', 'password1', 'Admin', 'a', 'b', 'c');
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (2, 'Mike Smith', 'msmith@uchicago.edu', 'password2', 'Student', 'a', 'b', 'c');
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (3, 'Elice Smith', 'esmith@uchicago.edu', 'password3', 'Teacher', 'a', 'b', 'c');


INSERT INTO course (course_id, course_name, course_desc, course_capacity, course_teacher) VALUES (1, 'Algos', 'Desing and analyze algos', 20, 3);


INSERT INTO announcement (announcement_id, announcement_title, announcement_desc, announcement_date_time) VALUES (1, 'Start of class', 'Welcome', "2022-06-01 00:00:00");


INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (1, 'HW1', 'Greedy', 30, "2022-06-01 00:00:00", "2022-06-10 00:00:00");

INSERT INTO user_course (u_id, course_id) VALUES (2, 1);

INSERT INTO course_announcement (course_id, announcement_id) VALUES (1, 1);

INSERT INTO course_assignment (course_id, assignment_id) VALUES (1, 1);

INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 1);