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
        # return db and cursor
        return db, cursor
    except:
        print("Couldn't connect the database")


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query_delete_match = "TRUNCATE matches CASCADE"

    cursor.execute(query_delete_match)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "TRUNCATE players CASCADE"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query_count = "SELECT count(id) from players"
    cursor.execute(query_count)

    # number of players
    output = int(cursor.fetchone()[0])

    db.commit()
    db.close()

    # return
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

    cursor.execute(query, parameter)
    db.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place
    , or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, cursor = connect()

    # SELECT player's id, player's.name,
    q_id_name = "SELECT players.id, players.name,"

    # how many times the player won
    q_win = "(SELECT count(matches.winner) FROM matches"
    q_win += " WHERE players.id = matches.winner) as wins, "
    # how many time the player matched
    q_match = "(SELECT count(*) FROM matches "
    q_match += "WHERE players.id = matches.winner OR "
    q_match += "players.id = matches.loser) AS matches "

    q_order_by_w = "FROM players ORDER BY wins;"

    # Execute the query
    cursor.execute(q_id_name+q_win+q_match+q_order_by_w)

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
    param = (winner, loser,)

    # execute the query
    cursor.execute(query_1, param)

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

    # get players record
    the_list = playerStandings()

    output = []
    a_id = ""
    a_name = ""
    b_id = ""
    b_name = ""

    index = 1
    for row in the_list:
        if (index % 2) == 1:
            a_id = row[0]
            a_name = row[1]
        else:
            b_id = row[0]
            b_name = row[1]
            output.append([a_id, a_name, b_id, b_name])
        index = index+1
    db.commit()
    db.close()
    return output
