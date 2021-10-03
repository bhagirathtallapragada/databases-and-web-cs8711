SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS student;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE student(
sno integer,
PRIMARY KEY(sno),
firstname varchar(50),
lastname varchar(50),
status varchar(255),
semester varchar(255));

DROP TABLE IF EXISTS courses;

CREATE TABLE courses(
sno integer,
c_2310 varchar(255),
c_4710 varchar(255),
c_8710 varchar(255),
FOREIGN KEY (sno) REFERENCES student(sno));

