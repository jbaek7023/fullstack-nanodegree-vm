#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        #return db and cursor
        return db, cursor
    except:
        print("Couldn't connect the database")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query_delete_match = "DELETE FROM matches"
    query_update_player = "UPDATE players SET matches=0, win=0"

    cursor.execute(query_delete_match)
    cursor.execute(query_update_player)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players"
    cursor.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query_count = "SELECT count(id) from players"
    cursor.execute(query_count)

    #number of players
    output = int(cursor.fetchone()[0])

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
    db, cursor = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    
    cursor.execute(query,parameter)
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
    db, cursor = connect()
    query_select_by_win = "SELECT * from players ORDER BY win;"
    cursor.execute(query_select_by_win)
    
    output = cursor.fetchall()
    db.commit()
    db.close()
    return output

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    #
    query_1 = "INSERT INTO matches(winner, loser) VALUES (%s, %s);"
    query_2 = "UPDATE players SET win = win + 1 WHERE id = %s;"
    query_3 = "UPDATE players SET matches = matches +1 WHERE id= %s OR id = %s;"

    param_w_l = (winner, loser,)
    param_w = (winner,)

    #execute the query
    cursor.execute(query_1, param_w_l)
    cursor.execute(query_2, param_w)
    cursor.execute(query_3, param_w_l)

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
    db, cursor = connect()
    
    #get players record
    query = "SELECT * FROM players ORDER BY win"
    cursor.execute(query)    

    the_list = cursor.fetchall()

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