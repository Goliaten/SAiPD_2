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
  `id` integer PRIMARY KEY,
  `created_date` timestamp,
  `modified_date` timestamp,
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
  `id` integer PRIMARY KEY,
  `created_date` timestamp,
  `modified_date` timestamp,
  `is_active` bool
);

CREATE TABLE `T_ROLE_PERMISSION` (
  `role_id` integer,
  `permission_id` integer
);

CREATE TABLE `T_PERMISSION` (
  `id` integer PRIMARY KEY,
  `name` varchar(255)
);

CREATE TABLE `T_MESSAGE` (
  `id` integer PRIMARY KEY,
  `user_id` integer,
  `title` varchar(255),
  `content` varchar(255)
);

CREATE TABLE `T_CLASS` (
  `id` integer PRIMARY KEY,
  `created_date` timestamp,
  `modified_date` timestamp,
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
  `id` integer PRIMARY KEY,
  `created_date` timestamp,
  `modified_date` timestamp,
  `name` varchar(255),
  `description` varchar(255)
);

CREATE TABLE `T_CLASS_EXERCISE` (
  `id` integer PRIMARY KEY,
  `class_id` integer,
  `exercise_id` integer
);

CREATE TABLE `T_EXERCISE_HISTORY` (
  `id` integer PRIMARY KEY,
  `class_exercise_id` integer,
  `created_date` timestamp,
  `modified_date` timestamp,
  `datetime_of_class` timestamp,
  `teacher_id` integer,
  `status` varchar(255)
);

CREATE TABLE `T_ATTENDANCE` (
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp,
  `modified_date` timestamp,
  `status` varchar(255)
);

CREATE TABLE `T_TODO` (
  `id` integer PRIMARY KEY,
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp,
  `modified_date` timestamp,
  `task_type` varchar(255),
  `title` varchar(255),
  `content` varchar(255),
  `status` varchar(255)
);

CREATE TABLE `T_MARK` (
  `id` integer PRIMARY KEY,
  `exercise_history_id` integer,
  `user_id` integer,
  `created_date` timestamp,
  `modified_date` timestamp
);

CREATE INDEX `T_USER_index_0` ON `T_USER` (`is_active`);
CREATE INDEX `T_MESSAGE_index_1` ON `T_MESSAGE` (`user_id`);
CREATE INDEX `T_CLASS_index_2` ON `T_CLASS` (`date_from`);
CREATE INDEX `T_CLASS_index_3` ON `T_CLASS` (`date_to`);
CREATE INDEX `T_EXERCISE_index_4` ON `T_EXERCISE` (`name`);
CREATE INDEX `T_CLASS_EXERCISE_index_5` ON `T_CLASS_EXERCISE` (`class_id`);
CREATE INDEX `T_CLASS_EXERCISE_index_6` ON `T_CLASS_EXERCISE` (`exercise_id`);
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
ALTER TABLE `T_EXERCISE_HISTORY` ADD FOREIGN KEY (`class_exercise_id`) REFERENCES `T_CLASS_EXERCISE` (`id`);
ALTER TABLE `T_ATTENDANCE` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_TODO` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_MARK` ADD FOREIGN KEY (`exercise_history_id`) REFERENCES `T_EXERCISE_HISTORY` (`id`);
ALTER TABLE `T_ATTENDANCE` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_TODO` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_MARK` ADD FOREIGN KEY (`user_id`) REFERENCES `T_USER` (`id`);
ALTER TABLE `T_EXERCISE_HISTORY` ADD FOREIGN KEY (`teacher_id`) REFERENCES `T_USER` (`id`);

-- insert default values