CREATE DATABASE IF NOT EXISTS football_league;

USE football_league;

CREATE TABLE IF NOT EXISTS competition(
  id int(11) NOT NULL,
  name varchar(200) NOT NULL,
  code varchar(200) NOT NULL,
  area_name varchar(200) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS team(
  id int(11) NOT NULL,
  name varchar(200) NOT NULL,
  tla varchar(200) NOT NULL,
  shortName varchar(200) NOT NULL,
  area_name varchar(200) NOT NULL,
  email varchar(200) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS competition_team(
  id int(11) AUTO_INCREMENT,
  id_competition int(11) NOT NULL,
  id_team int(11) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_competition) REFERENCES competition(id),
  FOREIGN KEY (id_team) REFERENCES team(id)
);

CREATE TABLE IF NOT EXISTS player(
  id int(11) NOT NULL,
  name varchar(200) NOT NULL,
  position varchar(200) NOT NULL,
  dateOfBirth date NOT NULL,
  countryOfBirth varchar(200) NOT NULL,
  nationality varchar(200) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS team_player(
  id int(11) AUTO_INCREMENT,
  id_team int(11) NOT NULL,
  id_player int(11) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_team) REFERENCES team(id),
  FOREIGN KEY (id_player) REFERENCES player(id)
);
