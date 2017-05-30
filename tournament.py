#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
# This content id produced by David Duckwitz
# (c) 2017 by David Duckwitz (Project for Nanodegree - Udacity)
# You can take this for getting ideas, but please create your own script

import time
import psycopg2
from random import shuffle

def connect():
    #Connect to Database
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    #Connect to Database
    db = connect()
    c = db.cursor()
    #Delete from Database
    c.execute("DELETE FROM matches")
    db.commit()
    #Close DB Connection
    db.close()

def deletePlayers():
    deleteTournamentPlayers()
    #Connect to Database
    db = connect()
    c = db.cursor()
    #Delete from Database
    c.execute("DELETE FROM players;")
    db.commit()
    #Close DB Connection
    db.close()

def deleteTournamentPlayers():
    #Connect to Database
    db = connect()
    c = db.cursor()
    #Delete from Database
    c.execute("DELETE FROM tournament_players;")
    db.commit()
    #Close DB Connection
    db.close()

def deleteTournaments():
    #Connect to Database
    db = connect()
    c = db.cursor()
    #Delete from Database
    c.execute("DELETE FROM tournaments;")
    db.commit()
    #Close DB Connection
    db.close()

def countPlayers():
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("SELECT count(*) from players;")
    rows = c.fetchall()
    #Close DB Connection
    db.close()

    return int(rows[0][0])

def createTournament(name, tournamentID = None):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    if tournamentID is None:
        c.execute("INSERT INTO tournaments VALUES (DEFAULT, %s);", (name, ))
    else:
        c.execute("INSERT INTO tournaments VALUES (%s, %s);", (tournamentID, name))

    db.commit()
    #Close DB Connection
    db.close()


def registerPlayer(name, tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("INSERT INTO players VALUES (DEFAULT, %s);", (name, ))

    if tournamentID is not None:
        c.execute("SELECT currval(pg_get_serial_sequence('players', 'id'));")
        playerID = int(c.fetchall()[0][0])

        c.execute("INSERT INTO tournament_players VALUES (%s, %s, DEFAULT)", (tournamentID, playerID))

    db.commit()
    #Close DB Connection
    db.close()

def addPlayerToTournament(tournamentID, playerID):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("INSERT INTO tournament_players VALUES (%s, %s, DEFAULT)", (tournamentID, playerID))

    db.commit()
    #Close DB Connection
    db.close()

def playerStandings(tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("SELECT PlayerID, PlayerName, Wins, Games FROM player_stats WHERE TournamentID = %s" , (tournamentID, ))
    rows = c.fetchall()
    #Close DB Connection
    db.close()

    l = list()

    for row in rows:
        l.append((int(row[0]), row[1], int(row[2]), int(row[3])))

    return l

def playerStats(tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("SELECT * FROM player_stats WHERE TournamentID = %s;", (tournamentID, ))
    rows = c.fetchall()
    #Close DB Connection
    db.close()

    return [(int(row[1]), row[2], int(row[3]), int(row[4]), int(row[5])) for row in rows]

def reportMatch(firstPlayer, secondPlayer, winner, tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("INSERT INTO matches VALUES (DEFAULT, %s, %s, %s, %s);", (tournamentID, firstPlayer, secondPlayer, winner))
    db.commit()
    #Close DB Connection
    db.close()

def swissPairings(tournamentID = 1):
    
    standings = playerStandings(tournamentID)

    if len(standings) % 2 != 0:
        # there is an odd amount of players
        players = playersWithoutBye()
        shuffle(players)

        luckyPlayer = players.pop()
        setBye(luckyPlayer[0])

        # report the match / remove the lucky player 
        reportMatch(luckyPlayer[0], None, luckyPlayer[0])
        standings = [player for player in standings if player[0] != luckyPlayer[0]]

    l = list()

    while len(standings) >= 2:
        firstPlayer = standings.pop(0)
        secondPlayer = standings.pop(0)

        l.append((firstPlayer[0], firstPlayer[1], secondPlayer[0], secondPlayer[1]))

    return l

def playersWithoutBye(tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("""SELECT PlayerID, Name FROM tournament_players
                 INNER JOIN players ON tournament_players.PlayerID = players.ID
                 WHERE HadBye = 0 AND TournamentID = %s;""", (tournamentID, ))
    rows = c.fetchall()
    #Close DB Connection
    db.close()

    return [(int(row[0]), row[1]) for row in rows]

def setBye(playerID, tournamentID = 1):
    #Connect to Database
    db = connect()
    c = db.cursor()
    #run Database Query
    c.execute("UPDATE tournament_players SET HadBye = 1 WHERE TournamentID = %s AND PlayerID = %s;", (tournamentID, playerID))
    db.commit()
    #Close DB Connection
    db.close()
