import sqlite3
import os
import game_info
import error_codes as ec

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
                    cur.execute("INSERT INTO playerinfo (name, class,attack,defense) VALUES (?,?,?,?)", (player_name, character_data["name"], character_data["stats"]["attack"], character_data["stats"]["defense"]))
                    data = cur.fetchone()
                    con.commit()
                    return ec.error_codes_create_character["0"]["message"]
          except sqlite3.Error as er:
                    if er.sqlite_errorcode == 2067:
                              return ec.error_codes_create_character["1"]["message"] 
                    
                    print("SQLite error:", er.sqlite_errorcode)
          return None
