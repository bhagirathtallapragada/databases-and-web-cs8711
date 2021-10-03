SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS senate;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE senate(
vid integer,
PRIMARY KEY(vid),
vname varchar(30),
rankk varchar(255));

DROP TABLE IF EXISTS candidate;

CREATE TABLE candidate(
vid integer,
c_ashwin varchar(255),
c_cai varchar(255),
c_cao varchar(255),
c_alex varchar(255),
FOREIGN KEY (vid) REFERENCES senate(vid));

