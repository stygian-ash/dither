CREATE SCHEMA IF NOT EXISTS dither;
USE dither;
CREATE TABLE IF NOT EXISTS Users ( user_id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(255) UNIQUE, displayname TINYTEXT, bio TEXT, location TINYTEXT, pronouns TINYTEXT, email TINYTEXT, password_hash TEXT, ban_duration DATETIME, is_admin BOOL);
CREATE TABLE IF NOT EXISTS Posts ( post_id INT PRIMARY KEY AUTO_INCREMENT, content TEXT, author_id INT, date_posted DATETIME, replies_to INT, quotes INT, FOREIGN KEY(author_id) REFERENCES Users(user_id), FOREIGN KEY(replies_to) REFERENCES Posts(post_id), FOREIGN KEY(quotes) REFERENCES Posts(post_id));
CREATE TABLE IF NOT EXISTS Media ( media_id INT PRIMARY KEY AUTO_INCREMENT, mime_type TINYTEXT, file LONGBLOB, thumbnail MEDIUMBLOB, post_id INT, FOREIGN KEY(post_id) REFERENCES Posts(post_id));
CREATE TABLE IF NOT EXISTS Interactions ( user_id INT, post_id INT, type ENUM('like', 'repost'), date DATETIME, PRIMARY KEY(user_id, post_id), FOREIGN KEY(user_id) REFERENCES Users(user_id), FOREIGN KEY(post_id) REFERENCES Posts(post_id));
CREATE TABLE IF NOT EXISTS Followers ( follower_id INT, followee_id INT, PRIMARY KEY(follower_id, followee_id), FOREIGN KEY(follower_id) REFERENCES Users(user_id), FOREIGN KEY(followee_id) REFERENCES Users(user_id));
CREATE TABLE IF NOT EXISTS Reports ( report_id INT PRIMARY KEY AUTO_INCREMENT, post_id INT, reported_by INT, reason TEXT, note TEXT, FOREIGN KEY(post_id) REFERENCES Posts(post_id), FOREIGN KEY(reported_by) REFERENCES Users(user_id));
