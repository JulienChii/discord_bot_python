import sqlite3
import os


con =  sqlite3.connect('playerinfo.db')
cur = con.cursor()

def get_player_info(player_name):
    """
    Get player info from the database.
    """
    cur.execute("SELECT * FROM players WHERE playername=?", (player_name))
    return cur.fetchone()



def insert_character_data(player_name, character_data):
          try:
                    cur.execute("INSERT INTO players (playername, character_data) VALUES (?,?,?,?)", (player_name, character_data["name"], character_data["attack"], character_data["defense"]))
          except sqlite3.Error as er:
                    print("SQLite error:", er)
          return NULL

          con.commit()

