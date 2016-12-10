-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    win INTEGER DEFAULT 0,
    matches INTEGER DEFAULT 0
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    winner INTEGER,
    loser INTEGER,
    FOREIGN KEY (winner) REFERENCES players(id),
    FOREIGN KEY (loser) REFERENCES players(id)
);
