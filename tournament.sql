-- Table definitions for the Udacity tournament project.
-- Create new DB (Suggestion from Reviewer: https://review.udacity.com/#!/reviews/524665)
CREATE DATABASE tournament;

-- Connect to DATABASE (Suggestion from Reviewer: https://review.udacity.com/#!/reviews/524665)
\connect tournament
-- Remove OLD Data from DB if exists (Suggestion from Reviewer: https://review.udacity.com/#!/reviews/524665)
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS matches CASCADE;

DROP VIEW IF EXISTS Standings CASCADE;
DROP VIEW IF EXISTS Count CASCADE;
DROP VIEW IF EXISTS Wins CASCADE;

-- Create Tables
CREATE TABLE players (
	ID serial PRIMARY KEY,
	Name varchar(255) NOT NULL
);

-- Create Table Tournaments
CREATE TABLE tournaments (
	ID serial PRIMARY KEY,
	Name varchar(255) NOT NULL
);

-- Create Table Matches
CREATE TABLE matches (
	ID serial PRIMARY KEY,
	TournamentID int NOT NULL,
	PlayerOne int NOT NULL,
	PlayerTwo int NOT NULL, 
	Winner int NOT NULL
);

-- Wins View shows number of wins for each Player
CREATE VIEW Wins AS
	SELECT players.ID, COUNT(matches.PlayerTwo) AS n 
	FROM players
	LEFT JOIN (SELECT * FROM matches) as Matches
	ON players.ID = Matches.Winner
	GROUP BY players.ID;

-- Count View shows number of matches for each Player
CREATE VIEW Count AS
	SELECT players.ID, COUNT(matches.PlayerOne) AS n 
	FROM players
	LEFT JOIN matches
	ON players.ID = matches.PlayerTwo
	GROUP BY players.ID;

-- Standings View shows number of wins and matches for each Player
CREATE VIEW Standings AS 
	SELECT players.ID as PlayerID, players.Name as PlayerName, Wins.n as wins, Count.n as Matches 
	FROM players, Count, Wins
	WHERE players.ID = Wins.id and Wins.id = Count.id;