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
    db = connect()
    c= db.cursor()
    c.execute("DELETE FROM matches")
    c.execute("UPDATE players SET matches=0, win=0")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(id) from players")

    #number of players
    output = int(c.fetchone()[0])

    db.commit()
    db.close()

    #return
    return output

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c= db.cursor()
    c.execute("INSERT into players(name) values (%s);",(name,))
    db.commit()
    db.close()
    

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
    db = connect()
    c= db.cursor()
    c.execute("SELECT * from players ORDER BY win;")
    output = c.fetchall()
    db.commit()
    db.close()
    return output

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c= db.cursor()
    c.execute("INSERT INTO matches(winner, loser) VALUES (%s, %s);",(winner, loser,))
    c.execute("UPDATE players SET win = win + 1 WHERE id = %s;", (winner,))
    c.execute("UPDATE players SET matches = matches +1 WHERE id= %s OR id = %s;", (winner, loser,))
    db.commit()
    db.close()
 
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
    db = connect()
    c = db.cursor()
    
    #get players record
    c.execute("SELECT * FROM players ORDER BY win")    
    the_list = c.fetchall()

    output =[]
    player_a_id=""
    player_a_name=""
    player_b_id=""
    player_b_name=""
    
    index=1 
    for row in the_list:
        if (index%2) == 1:
            player_a_id = row[0]
            player_a_name = row[1]
        else:
            player_b_id = row[0]
            player_b_name = row[1]
            output.append([player_a_id, player_a_name, player_b_id, player_b_name])
        index = index+1
    db.commit()
    db.close()
    return output