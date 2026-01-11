-- drop all tables
DROP TABLE IF EXISTS T_USER_ROLE;
DROP TABLE IF EXISTS T_ROLE_PERMISSION;
DROP TABLE IF EXISTS T_ROLE;
DROP TABLE IF EXISTS T_PERMISSION;
DROP TABLE IF EXISTS T_TODO;
DROP TABLE IF EXISTS T_ATTENDANCE;
DROP TABLE IF EXISTS T_MARK;
DROP TABLE IF EXISTS T_EXERCISE_HISTORY;
DROP TABLE IF EXISTS T_USER_CLASS;
DROP TABLE IF EXISTS T_CLASS_EXERCISE;
DROP TABLE IF EXISTS T_EXERCISE;
DROP TABLE IF EXISTS T_MESSAGE;
DROP TABLE IF EXISTS T_USER;
DROP TABLE IF EXISTS T_CLASS;

-- create all tables and indexes
CREATE TABLE `T_USER` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `login` varchar(255),
  `email` varchar(255),
  `password` varchar(255),
  `is_active` bool
);

CREATE TABLE `T_USER_ROLE` (
  `user_id` integer,
  `role_id` integer
);

CREATE TABLE `T_ROLE` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `is_active` bool,
  `is_default_user_role` bool
);

CREATE TABLE `T_ROLE_PERMISSION` (
  `role_id` integer,
  `permission_id` integer
);

CREATE TABLE `T_PERMISSION` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255)
);

CREATE TABLE `T_MESSAGE` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `user_id` integer NOT NULL,
  `sender_id` integer NOT NULL,
  `title` varchar(255),
  `content` varchar(255)
);

CREATE TABLE `T_CLASS` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `date_from` datetime,
  `date_to` datetime,
  `name` varchar(255),
  `is_active` bool
);

CREATE TABLE `T_USER_CLASS` (
  `user_id` integer,
  `class_id` integer
);

CREATE TABLE `T_EXERCISE` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `name` varchar(255),
  `description` longtext
);

CREATE TABLE `T_CLASS_EXERCISE` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `class_id` integer NOT NULL,
  `exercise_id` integer NOT NULL,
  `teacher_id` integer NOT NULL,
  `day_of_week` integer NOT NULL,
  `time_of_exercise` time NOT NULL,
  `week_interval` integer DEFAULT 1,
  `week_offset` integer DEFAULT 0
);

CREATE TABLE `T_EXERCISE_HISTORY` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `class_exercise_id` integer,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `datetime_of_class` timestamp,
  `teacher_id` integer,
  `status` varchar(255)
);

CREATE TABLE `T_ATTENDANCE` (
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `status` varchar(255)
);

CREATE TABLE `T_TODO` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `task_type` varchar(255),
  `title` varchar(255),
  `content` varchar(255),
  `status` varchar(255)
);

CREATE TABLE `T_MARK` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp default current_timestamp,
  `modified_date` timestamp default current_timestamp,
  `grade` varchar(20) default NULL
);

CREATE INDEX `T_USER_index_0` ON `T_USER` (`is_active`);
CREATE INDEX `T_MESSAGE_index_1` ON `T_MESSAGE` (`user_id`);
CREATE INDEX `T_CLASS_index_2` ON `T_CLASS` (`date_from`);
CREATE INDEX `T_CLASS_index_3` ON `T_CLASS` (`date_to`);
CREATE INDEX `T_EXERCISE_index_4` ON `T_EXERCISE` (`name`);
CREATE INDEX `T_CLASS_EXERCISE_index_5` ON `T_CLASS_EXERCISE` (`class_id`);
CREATE INDEX `T_CLASS_EXERCISE_index_6` ON `T_CLASS_EXERCISE` (`exercise_id`);
CREATE INDEX `T_CLASS_EXERCISE_index_7` ON `T_CLASS_EXERCISE` (`teacher_id`);
CREATE INDEX `T_EXERCISE_HISTORY_index_7` ON `T_EXERCISE_HISTORY` (`class_exercise_id`);
CREATE INDEX `T_EXERCISE_HISTORY_index_8` ON `T_EXERCISE_HISTORY` (`teacher_id`);
CREATE INDEX `T_EXERCISE_HISTORY_index_9` ON `T_EXERCISE_HISTORY` (`datetime_of_class`);
CREATE INDEX `T_ATTENDANCE_index_10` ON `T_ATTENDANCE` (`exercise_history_id`);
CREATE INDEX `T_ATTENDANCE_index_11` ON `T_ATTENDANCE` (`user_id`);
CREATE INDEX `T_ATTENDANCE_index_12` ON `T_ATTENDANCE` (`status`);
CREATE INDEX `T_TODO_index_13` ON `T_TODO` (`exercise_history_id`);
CREATE INDEX `T_TODO_index_14` ON `T_TODO` (`user_id`);
CREATE INDEX `T_TODO_index_15` ON `T_TODO` (`status`);
CREATE INDEX `T_MARK_index_16` ON `T_MARK` (`exercise_history_id`);
CREATE INDEX `T_MARK_index_17` ON `T_MARK` (`user_id`);

-- create foreign keys

ALTER TABLE `T_ROLE_PERMISSION` ADD FOREIGN KEY (`permission_id`) REFERENCES `T_PERMISSION` (`id`);
ALTER TABLE `T_ROLE_PERMISSION` ADD FOREIGN KEY (`role_id`) REFERENCES `T_ROLE` (`id`);
ALTER TABLE `T_USER_ROLE` ADD FOREIGN KEY (`role_id`) REFERENCES `T_ROLE` (`id`);
ALTER TABLE `T_USER_ROLE` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_MESSAGE` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_USER_CLASS` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_USER_CLASS` ADD FOREIGN KEY (`class_id`) REFERENCES `T_CLASS` (`id`);
ALTER TABLE `T_CLASS_EXERCISE` ADD FOREIGN KEY (`class_id`) REFERENCES `T_CLASS` (`id`);
ALTER TABLE `T_CLASS_EXERCISE` ADD FOREIGN KEY (`exercise_id`) REFERENCES `T_EXERCISE` (`id`);
ALTER TABLE `T_CLASS_EXERCISE` ADD FOREIGN KEY (`teacher_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_EXERCISE_HISTORY` ADD FOREIGN KEY (`class_exercise_id`) REFERENCES `T_CLASS_EXERCISE` (`id`);
ALTER TABLE `T_ATTENDANCE` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_TODO` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_MARK` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_ATTENDANCE` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_TODO` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_MARK` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_EXERCISE_HISTORY` ADD FOREIGN KEY (`teacher_id`) REFERENCES `T_USER` (`id`);

-- insert default values

INSERT INTO T_PERMISSION (name) values 
  -- high order permissions
  ('global_admin'), -- access to everything
  ('is_teacher'), -- access to teacher stuff
  ('is_student'), -- access to student stuff
  -- low order permissions
  ('can_manage_students'), -- can crud students (automatically assings student role)
  ('can_manage_teachers'), -- can crud teachers (automatically assings teacher role)
  ('can_manage_roles'), -- can crud roles, assing permissions to roles, and assing them to users (does NOT include crud of permissions)
  ('can_manage_exercise'), -- can crud exercise
  ('can_manage_class'), -- can crud class, and add users to it (T_USER_CLASS)
  ('can_assign_exercise_to_class'), -- can create entry in T_CLASS_EXERCISE
  ('can_send_message'), -- can send messages to users
  ('can_manage_exercise_history') -- managing exercise_history, attendance, todo, mark
;

-- insert roles ADMIN, TEACHER, STUDENT, SCHOOL_ADMIN
INSERT INTO T_ROLE(name, created_date, modified_date, is_active, is_default_user_role) VALUES
  ('global_admin', CURDATE(), CURDATE(), 1, 0),
  ('empty_user', CURDATE(), CURDATE(), 1, 1),
  ('default_teacher', CURDATE(), CURDATE(), 1, 0),
  ('default_student', CURDATE(), CURDATE(), 1, 0)
;

INSERT INTO T_ROLE_PERMISSION (role_id, permission_id) VALUES
  (1, 1), -- global admin
  (2, 10), -- empty user
  (3, 2), -- default teacher
  (4, 3) -- default student
;

INSERT INTO T_USER (created_date, modified_date, first_name, last_name, login, email, password, is_active) VALUES
  (CURDATE(), CURDATE(), 'admin', 'admin', 'admin', 'admin@admin.pl', MD5('admin'), 1),
  (CURDATE(), CURDATE(), 'example_user', 'example_user', 'user', 'user@user.pl', MD5('user'), 1),
  (CURDATE(), CURDATE(), 'example_user2', 'example_user2', 'user2', 'user2@user.pl', MD5('user2'), 1),
  (CURDATE(), CURDATE(), 'student', 'studentski', 'student', 'student@user.pl', MD5('student'), 1),
  (CURDATE(), CURDATE(), 'teacher', 'teacherski', 'teacher', 'teacher@user.pl', MD5('teacher'), 1)
;
 
INSERT INTO T_USER_ROLE (user_id, role_id) VALUES
  (1, 1),
  (2, 2),
  (3, 2),
  (4, 4),
  (5, 3)
;

INSERT INTO T_CLASS(created_date, modified_date, date_from, date_to, name, is_active) VALUES
  (CURDATE(), CURDATE(), CURDATE()-INTERVAL 1 MONTH, CURDATE()+INTERVAL 1 MONTH, "example_class", 1)
;

INSERT INTO T_USER_CLASS(user_id, class_id) VALUES
  (2, 1),
  (4, 1)
;

INSERT INTO T_EXERCISE(created_date, modified_date, name, description) VALUES
  (CURDATE(), CURDATE(), "example_exercise", "Liberum Veto")
;

INSERT INTO T_CLASS_EXERCISE(class_id, exercise_id, teacher_id, day_of_week, time_of_exercise) VALUES
  (1, 1, 5, 1, "08:00"),
  (1, 1, 5, 5, "12:30")
;

INSERT INTO T_EXERCISE_HISTORY (class_exercise_id, created_date, modified_date, datetime_of_class, teacher_id, status) VALUES
  (1, CURDATE(), CURDATE(), CURDATE() + INTERVAL 1 WEEK, 3, 'upcoming')
;
-- statusy: upcoming, finished, cancelled, not_started
-- przy utworzeniu exercise_history, powinna się generować attendance

-- statusy obecności: upcoming, present, absent, late, not_started
INSERT INTO T_ATTENDANCE (exercise_history_id, user_id, created_date, modified_date, status) VALUES
  (1, 2, CURDATE(), CURDATE(), 'upcoming')
;

-- Additional example data for comprehensive testing

-- Additional users (more students and teachers)
INSERT INTO T_USER (created_date, modified_date, first_name, last_name, login, email, password, is_active) VALUES
  (CURDATE(), CURDATE(), 'Anna', 'Kowalski', 'anna_k', 'anna.kowalski@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Bartek', 'Lewandowski', 'bartek_l', 'bartek.lewandowski@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Celina', 'Nowak', 'celina_n', 'celina.nowak@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Dominik', 'Zielinski', 'dominik_z', 'dominik.zielinski@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Ewa', 'Michalska', 'ewa_m', 'ewa.michalska@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Filip', 'Gajda', 'filip_g', 'filip.gajda@school.pl', MD5('pass123'), 1),
  (CURDATE(), CURDATE(), 'Grażyna', 'Wolska', 'grazyna_w', 'grazyna.wolska@school.pl', MD5('teacher_pass'), 1),
  (CURDATE(), CURDATE(), 'Henryk', 'Piotrowski', 'henryk_p', 'henryk.piotrowski@school.pl', MD5('teacher_pass'), 1),
  (CURDATE(), CURDATE(), 'Irena', 'Szymczak', 'irena_s', 'irena.szymczak@school.pl', MD5('teacher_pass'), 1)
;

-- Assign new users to roles (students and teachers)
INSERT INTO T_USER_ROLE (user_id, role_id) VALUES
  (6, 4),   -- Anna - student
  (7, 4),   -- Bartek - student
  (8, 4),   -- Celina - student
  (9, 4),   -- Dominik - student
  (10, 4),  -- Ewa - student
  (11, 4),  -- Filip - student
  (12, 3),  -- Grażyna - teacher
  (13, 3),  -- Henryk - teacher
  (14, 3)   -- Irena - teacher
;

-- Additional classes
INSERT INTO T_CLASS(created_date, modified_date, date_from, date_to, name, is_active) VALUES
  (CURDATE(), CURDATE(), CURDATE()-INTERVAL 2 MONTH, CURDATE()+INTERVAL 2 MONTH, 'Mathematics 101', 1),
  (CURDATE(), CURDATE(), CURDATE()-INTERVAL 1 MONTH, CURDATE()+INTERVAL 1 MONTH, 'Physics 201', 1),
  (CURDATE(), CURDATE(), CURDATE()-INTERVAL 3 MONTH, CURDATE()+INTERVAL 3 MONTH, 'Chemistry Lab', 1),
  (CURDATE(), CURDATE(), CURDATE()-INTERVAL 1 WEEK, CURDATE()+INTERVAL 2 WEEK, 'Advanced Programming', 1)
;

-- Assign students to classes
INSERT INTO T_USER_CLASS(user_id, class_id) VALUES
  (2, 1),   -- example_user - example_class
  (4, 1),   -- student - example_class
  (6, 2),   -- Anna - Mathematics 101
  (7, 2),   -- Bartek - Mathematics 101
  (8, 2),   -- Celina - Mathematics 101
  (6, 3),   -- Anna - Physics 201
  (9, 3),   -- Dominik - Physics 201
  (10, 3),  -- Ewa - Physics 201
  (11, 4),  -- Filip - Advanced Programming
  (7, 4),   -- Bartek - Advanced Programming
  (8, 4)    -- Celina - Advanced Programming
;

-- Additional exercises
INSERT INTO T_EXERCISE(created_date, modified_date, name, description) VALUES
  (CURDATE(), CURDATE(), 'Algebra Practice', 'Basic algebra problems and equations'),
  (CURDATE(), CURDATE(), 'Calculus Problems', 'Integration and differentiation exercises'),
  (CURDATE(), CURDATE(), 'Physics Experiments', 'Laboratory experiments with data collection'),
  (CURDATE(), CURDATE(), 'Circuit Analysis', 'Electronic circuit analysis and design'),
  (CURDATE(), CURDATE(), 'Code Review', 'Review and refactor existing code'),
  (CURDATE(), CURDATE(), 'Algorithm Challenge', 'Implement and optimize sorting algorithms')
;

-- Assign exercises to classes with teachers
INSERT INTO T_CLASS_EXERCISE(class_id, exercise_id, teacher_id, day_of_week, time_of_exercise) VALUES
  (2, 2, 5, 2, "10:00"),    -- Mathematics 101: Algebra, teacher 5 (teacher), Monday 10:00
  (2, 3, 5, 4, "14:00"),    -- Mathematics 101: Calculus, teacher 5, Wednesday 14:00
  (3, 4, 12, 1, "09:00"),   -- Physics 201: Physics Experiments, teacher 12 (Grażyna), Monday 09:00
  (3, 5, 12, 3, "11:00"),   -- Physics 201: Circuit Analysis, teacher 12, Tuesday 11:00
  (4, 6, 13, 2, "15:00"),   -- Advanced Programming: Code Review, teacher 13 (Henryk), Monday 15:00
  (4, 7, 13, 5, "16:00")    -- Advanced Programming: Algorithm Challenge, teacher 13, Thursday 16:00
;

-- Generate more exercise history records
INSERT INTO T_EXERCISE_HISTORY (class_exercise_id, created_date, modified_date, datetime_of_class, teacher_id, status) VALUES
  (2, CURDATE(), CURDATE(), CURDATE() + INTERVAL 1 DAY, 5, 'upcoming'),
  (2, CURDATE(), CURDATE(), CURDATE() + INTERVAL 8 DAY, 5, 'upcoming'),
  (3, CURDATE(), CURDATE(), CURDATE() + INTERVAL 2 DAY, 5, 'upcoming'),
  (4, CURDATE(), CURDATE(), CURDATE() - INTERVAL 5 DAY, 12, 'finished'),
  (4, CURDATE(), CURDATE(), CURDATE() + INTERVAL 2 DAY, 12, 'upcoming'),
  (5, CURDATE(), CURDATE(), CURDATE() - INTERVAL 3 DAY, 12, 'finished'),
  (5, CURDATE(), CURDATE(), CURDATE() + INTERVAL 4 DAY, 12, 'upcoming'),
  (6, CURDATE(), CURDATE(), CURDATE() - INTERVAL 1 DAY, 13, 'finished'),
  (6, CURDATE(), CURDATE(), CURDATE() + INTERVAL 6 DAY, 13, 'upcoming'),
  (7, CURDATE(), CURDATE(), CURDATE() - INTERVAL 2 DAY, 13, 'finished'),
  (7, CURDATE(), CURDATE(), CURDATE() + INTERVAL 5 DAY, 13, 'upcoming')
;

-- Generate attendance for historical and upcoming exercises
INSERT INTO T_ATTENDANCE (exercise_history_id, user_id, created_date, modified_date, status) VALUES
  -- Exercise history 1 (upcoming)
  (1, 6, CURDATE(), CURDATE(), 'upcoming'),
  (1, 7, CURDATE(), CURDATE(), 'upcoming'),
  (1, 8, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 2 (upcoming)
  (2, 6, CURDATE(), CURDATE(), 'upcoming'),
  (2, 7, CURDATE(), CURDATE(), 'upcoming'),
  (2, 8, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 3 (upcoming)
  (3, 6, CURDATE(), CURDATE(), 'upcoming'),
  (3, 9, CURDATE(), CURDATE(), 'upcoming'),
  (3, 10, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 4 (finished - past)
  (4, 6, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'present'),
  (4, 9, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'present'),
  (4, 10, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'absent'),
  -- Exercise history 5 (upcoming)
  (5, 6, CURDATE(), CURDATE(), 'upcoming'),
  (5, 9, CURDATE(), CURDATE(), 'upcoming'),
  (5, 10, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 6 (finished - past)
  (6, 6, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'present'),
  (6, 9, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'late'),
  (6, 10, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'present'),
  -- Exercise history 7 (upcoming)
  (7, 6, CURDATE(), CURDATE(), 'upcoming'),
  (7, 9, CURDATE(), CURDATE(), 'upcoming'),
  (7, 10, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 8 (finished - past)
  (8, 11, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'present'),
  (8, 7, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'present'),
  (8, 8, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'present'),
  -- Exercise history 9 (upcoming)
  (9, 11, CURDATE(), CURDATE(), 'upcoming'),
  (9, 7, CURDATE(), CURDATE(), 'upcoming'),
  (9, 8, CURDATE(), CURDATE(), 'upcoming'),
  -- Exercise history 10 (finished - past)
  (10, 11, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'present'),
  (10, 7, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'absent'),
  (10, 8, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'late'),
  -- Exercise history 11 (upcoming)
  (11, 11, CURDATE(), CURDATE(), 'upcoming'),
  (11, 7, CURDATE(), CURDATE(), 'upcoming'),
  (11, 8, CURDATE(), CURDATE(), 'upcoming')
;

-- Add marks/grades for completed exercises
INSERT INTO T_MARK (exercise_history_id, user_id, created_date, modified_date, grade) VALUES
  (4, 6, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'A'),
  (4, 9, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'B+'),
  (4, 10, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 5 DAY, 'C'),
  (6, 6, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'A-'),
  (6, 9, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'A'),
  (6, 10, CURDATE()-INTERVAL 3 DAY, CURDATE()-INTERVAL 3 DAY, 'B'),
  (8, 11, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'A'),
  (8, 7, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'B+'),
  (8, 8, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'A-'),
  (10, 11, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'B'),
  (10, 7, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'C+'),
  (10, 8, CURDATE()-INTERVAL 2 DAY, CURDATE()-INTERVAL 2 DAY, 'B-')
;

-- Add tasks/todos for students
INSERT INTO T_TODO (exercise_history_id, user_id, created_date, modified_date, task_type, title, content, status) VALUES
  (4, 6, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 3 DAY, 'homework', 'Solve Problem Set 1', 'Complete problems 1-10 from Chapter 2', 'completed'),
  (4, 9, CURDATE()-INTERVAL 5 DAY, CURDATE()-INTERVAL 4 DAY, 'homework', 'Solve Problem Set 1', 'Complete problems 1-10 from Chapter 2', 'completed'),
  (4, 10, CURDATE()-INTERVAL 5 DAY, CURDATE(), 'homework', 'Solve Problem Set 1', 'Complete problems 1-10 from Chapter 2', 'in_progress'),
  (5, 6, CURDATE(), CURDATE(), 'assignment', 'Research Project', 'Write a 5-page report on calculus applications', 'pending'),
  (5, 9, CURDATE(), CURDATE(), 'assignment', 'Research Project', 'Write a 5-page report on calculus applications', 'pending'),
  (5, 10, CURDATE(), CURDATE(), 'assignment', 'Research Project', 'Write a 5-page report on calculus applications', 'pending'),
  (6, 6, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'lab', 'Lab Report', 'Document experimental results and analysis', 'completed'),
  (6, 9, CURDATE()-INTERVAL 1 DAY, CURDATE()-INTERVAL 1 DAY, 'lab', 'Lab Report', 'Document experimental results and analysis', 'completed'),
  (7, 6, CURDATE(), CURDATE(), 'quiz', 'Circuit Quiz', 'Complete online quiz on basic circuits', 'pending'),
  (7, 9, CURDATE(), CURDATE(), 'quiz', 'Circuit Quiz', 'Complete online quiz on basic circuits', 'pending'),
  (9, 11, CURDATE(), CURDATE(), 'assignment', 'Code Implementation', 'Implement binary search algorithm', 'pending'),
  (9, 7, CURDATE(), CURDATE(), 'assignment', 'Code Implementation', 'Implement binary search algorithm', 'pending'),
  (9, 8, CURDATE(), CURDATE(), 'assignment', 'Code Implementation', 'Implement binary search algorithm', 'pending')
;

-- Add sample messages between users
INSERT INTO T_MESSAGE (user_id, sender_id, title, content) VALUES
  (6, 5, 'Grades Posted', 'Your latest grades have been posted on the system.'),
  (9, 5, 'Grades Posted', 'Your latest grades have been posted on the system.'),
  (11, 13, 'Assignment Question', 'I have a question about problem 5 in the homework.'),
  (13, 11, 'RE: Assignment Question', 'Please check chapter 3, section 2 for a similar example.'),
  (7, 6, 'Study Group', 'Want to form a study group for the upcoming exam?'),
  (4, 2, 'Class Reminder', 'Remember to submit your lab report by Friday.'),
  (8, 7, 'Project Collaboration', 'Should we work together on the research project?'),
  (12, 6, 'Attendance Issue', 'I noticed you were absent last class. Is everything okay?')
;