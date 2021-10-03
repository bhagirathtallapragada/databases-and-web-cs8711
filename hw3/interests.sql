SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS interests;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE interests(
sid integer,
PRIMARY KEY(sid),
sname varchar(50),
degree varchar(255));

DROP TABLE IF EXISTS pls;

CREATE TABLE pls(
sid integer,
c_java varchar(255),
c_cplusplus varchar(255),
c_pascal varchar(255),
FOREIGN KEY (sid) REFERENCES interests(sid));

DROP TABLE IF EXISTS hobbies;

CREATE TABLE hobbies(
sid integer,
c_stamp_collection varchar(255),
c_coin_collection varchar(255),
c_reading varchar(255),
c_crossword_puzzles varchar(255),
c_painting varchar(255),
c_screen_printing varchar(255),
FOREIGN KEY (sid) REFERENCES interests(sid));

