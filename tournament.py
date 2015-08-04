#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
    

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("DELETE FROM matches;")
        connection.commit()
        connection.close()
    except Exception as e:
        print e



def deletePlayers():
    """Remove all the player records from the database."""
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("DELETE FROM players;")
        connection.commit()
        connection.close()
    except Exception as e:
        print e

def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    c = connection.cursor()
    c.execute("SELECT count(*) AS num FROM players")
    count = c.fetchall()
    connection.close()
    return count.pop()[0]




def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = str(name)
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("INSERT INTO players(name) values(%s)", (name,))
        connection.commit()
        connection.close()
    except Exception as e:
        print "error: " + str(e)

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("""SELECT * FROM standings;
				 """)
        return c.fetchall()
    except Exception as e:
    	print "error: " + str(e)



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("""INSERT INTO matches(p1,p2,winner) values(%s,%s,%s)""" , (loser,winner,winner))
        connection.commit()
        connection.close()
    except Exception as e:
        print "error: " + str(e)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    try:
        connection = connect()
        c = connection.cursor()
        c.execute("""SELECT wincount.id, players.name
                  FROM wincount 
                  LEFT OUTER JOIN players ON players.id = wincount.id
                  ORDER BY wins DESC""")
        rawdata = c.fetchall()
        rawpairs = []
        if len(rawdata) % 2:
            rawpairs.append(("NA","bye"))
        pairs = []
        for e in rawdata:
            rawpairs.append(e)
        while len(rawpairs) > 1:
            pairs.append((rawpairs.pop() + rawpairs.pop()))
        if len(rawpairs) != 0:
            pairs.append(rawpairs.pop())
        return pairs



    except Exception as e:
        print "error: " + str(e)
