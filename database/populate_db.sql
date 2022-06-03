--user 
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (1, 'Admin', 'admin1@uchicago.edu', '@password1', 'Admin', 'a', 'b', 'c', "True");
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (2, 'Mike Smith', 'msmith@uchicago.edu', '@password2', 'Student', 'a', 'b', 'c');
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (3, 'Elice Smith', 'esmith@uchicago.edu', '@password3', 'Teacher', 'a', 'b', 'c');
INSERT INTO user (u_id, user_full_name, user_email, user_pwd, user_type, user_a1, user_a2, user_a3) VALUES (4, 'Laura Smith', 'lsmith@uchicago.edu', '@password4', 'Student', 'a', 'b', 'c');


INSERT INTO course (course_id, course_name, course_desc, course_capacity, course_teacher) VALUES (1, 'Algos', 'Design and analyze algos', 20, 3);
INSERT INTO course (course_id, course_name, course_desc, course_capacity, course_teacher) VALUES (2, 'ML', 'Design convex optimization algorithms', 20, 3);
INSERT INTO course (course_id, course_name, course_desc, course_capacity, course_teacher) VALUES (3, 'HPC', 'Parallelize using MPI', 20, 3);


INSERT INTO announcement (announcement_id, announcement_title, announcement_desc, announcement_date_time) VALUES (1, 'Start of class', 'Welcome', "2022-06-01 00:00:00");
INSERT INTO announcement (announcement_id, announcement_title, announcement_desc, announcement_date_time) VALUES (2, 'Change of class hours', 'Alert', "2022-05-31 00:00:00");
INSERT INTO announcement (announcement_id, announcement_title, announcement_desc, announcement_date_time) VALUES (3, 'Surprise', 'Pop quiz next week. Prepare!', "2022-05-30 00:00:00");


INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (1, 'HW1', 'Greedy', 30, "2022-06-01 00:00:00", "2022-06-04 00:00:00");
INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (2, 'HW2', 'Divide and Conquer', 30, "2022-06-01 00:00:00", "2022-06-10 00:00:00");
INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (3, 'HW3', 'Dynamic Programming', 30, "2022-05-01 00:00:00", "2022-05-30 00:00:00");

INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (4, 'HW1', 'Conjugate Gradient', 30, "2022-06-01 00:00:00", "2022-06-04 00:00:00");
INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (5, 'HW2', 'Backpropogation', 30, "2022-06-01 00:00:00", "2022-06-10 00:00:00");
INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (6, 'HW3', 'PAC Learning', 30, "2022-05-01 00:00:00", "2022-05-30 00:00:00");

INSERT INTO assignment (assignment_id, assignment_title, assignment_desc, assignment_total_points, assignment_post_date, assignment_due_date) VALUES (7, 'HW1', 'MPI + OpenMP', 50, "2022-06-01 00:00:00", "2022-06-5 00:00:00");


INSERT INTO user_course (u_id, course_id) VALUES (2, 1);
INSERT INTO user_course (u_id, course_id) VALUES (2, 2);
INSERT INTO user_course (u_id, course_id) VALUES (2, 3);

INSERT INTO user_course (u_id, course_id) VALUES (4, 1);
INSERT INTO user_course (u_id, course_id) VALUES (4, 3);



INSERT INTO course_announcement (course_id, announcement_id) VALUES (1, 1);
INSERT INTO course_announcement (course_id, announcement_id) VALUES (1, 2);
INSERT INTO course_announcement (course_id, announcement_id) VALUES (1, 3);

INSERT INTO course_announcement (course_id, announcement_id) VALUES (2, 1);
INSERT INTO course_announcement (course_id, announcement_id) VALUES (2, 3);

INSERT INTO course_announcement (course_id, announcement_id) VALUES (3, 2);



INSERT INTO course_assignment (course_id, assignment_id) VALUES (1, 1);
INSERT INTO course_assignment (course_id, assignment_id) VALUES (1, 2);
INSERT INTO course_assignment (course_id, assignment_id) VALUES (1, 3);

INSERT INTO course_assignment (course_id, assignment_id) VALUES (2, 4);
INSERT INTO course_assignment (course_id, assignment_id) VALUES (2, 5);
INSERT INTO course_assignment (course_id, assignment_id) VALUES (2, 6);

INSERT INTO course_assignment (course_id, assignment_id) VALUES (3, 7);




INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 1);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 2);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 3);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 4);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 5);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 6);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (2, 7);

INSERT INTO user_assignment (u_id, assignment_id) VALUES (4, 1);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (4, 2);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (4, 3);
INSERT INTO user_assignment (u_id, assignment_id) VALUES (4, 7);