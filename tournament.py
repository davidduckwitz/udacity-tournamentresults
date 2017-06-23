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
    try:
        db = psycopg2.connect("dbname='tournament' user='postgres' password='postgres'")
	c = db.cursor()
	return db, c
    except:
	print "Unable to connect to database"		

def deleteMatches():    
    db, c = connect()    
    c.execute("DELETE FROM matches;")
    db.commit()   
    db.close()

def deletePlayers():
    db, c = connect()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()

def deleteTournaments():    
    db, c = connect()
    c.execute("DELETE FROM tournaments;")
    db.commit()    
    db.close()

def countPlayers():    
    db, c = connect()
    c.execute("SELECT count(*) from players;")
    rows = c.fetchall()    
    db.close()
    return int(rows[0][0])

def createTournament(name, tournamentID = None):    
    db, c = connect()    
    if tournamentID is None:
        c.execute("INSERT INTO tournaments VALUES (DEFAULT, %s);", (name, ))
    else:
        c.execute("INSERT INTO tournaments VALUES (DEFAULT, %s, %s);", (tournamentID, name))
    db.commit()    
    db.close()

def registerPlayer(name):    
    db, c = connect()   
    c.execute("INSERT INTO players VALUES (DEFAULT, %s);", (name, ))
    db.commit()    
    db.close()

def playerStandings(tournamentID = 1):    
    db, c = connect()
    c.execute("SELECT PlayerID, PlayerName, Wins, Matches FROM Standings order by Wins asc")
    rows = c.fetchall()    
    db.close()
    l = list()
    i=0
    while i < len(rows):
        l.append((int(rows[i][0]), rows[i][1], int(rows[i][2]), int(rows[i][3])))
        i=i+1
    return l

def reportMatch(winner, loser, draw, tournamentID = 1):    
    db, c = connect()
    if draw:
        c.execute("INSERT INTO Matches VALUES (DEFAULT, 1, %s,%s,%s)",(winner,loser,winner))
        c.execute("INSERT INTO Matches VALUES (DEFAULT, 1, %s,%s,&s)",(loser,winner,winner))
    else:
        c.execute("INSERT INTO Matches VALUES (DEFAULT, 1, %s,%s,%s)",(winner,loser,winner))
        c.execute("INSERT INTO Matches VALUES (DEFAULT, 1, %s,%s,%s)",(loser,winner,0))    
    db.commit()    
    db.close()

def swissPairings():    
    db, c = connect()
    c.execute("SELECT * FROM Standings ORDER BY wins DESC;")
    rows = c.fetchall()
    db.close()
    i=0
    standings = playerStandings()
    num = int(countPlayers())
    pairings = []
    if (num > 0): 
        for i in range (num):
            if (i % 2 == 0):
                id1 = standings[i][0]
                name1 = standings[i][1]
                id2 = standings[i + 1][0]
                name2 = standings[i + 1][1]
                pair = (id1, name1, id2, name2)
                pairings.append(pair)
	return pairings
