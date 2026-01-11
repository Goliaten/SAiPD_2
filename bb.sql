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
  `user_id` integer,
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
  `modified_date` timestamp default current_timestamp
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