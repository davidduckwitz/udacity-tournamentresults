# Udacity Full Stack Web Developer Nanodegree Tournament Results

Requirements:
1. PostgreSQL (tested with V9.4)
2. Python 2.7

How to Start:
1. After Installing PostgreSQL and Python 2.7, Import the "tournament.sql" to your PostgreSQL DB:
--> in Postgres Console: "\i '/tournament.sql'"
2. Change DB Settings to your Own Settings (You have setted on PostgreSQL Install): LINE 15 in tournament.py
--> Edit user='YOUR POSTGRESQL USER' password'YOUR POSTGRESQL PASSWORD'
3. Run tournament_test.py
--> python ./tournaqment_test.py

If all is Working, you will se following Output:

1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!

Attention!!
Use this Script just and only for getting Ideas and Inspiration, but don't use it at your own !!
(c) 2017 by David Duckwitz
