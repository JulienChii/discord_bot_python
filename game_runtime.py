import time
import main


cur_adventures = [] # Playername , timestamp, lenght

def set_adventure(playername, adventure, required_time):
    if len(cur_adventures) == 0:
        start_time = time.time()
        required_time = start_time + required_time
        cur_adventures.append([playername, start_time, adventure,required_time])
        print(cur_adventures)
        return True # Adventure started
    else:
        for i in cur_adventures:
            if i[0] == playername:
                return False # Adventure already running
            else:
                cur_adventures.append([playername, time.time(), adventure,required_time])
                return True # Adventure started

def get_adventure(playername):
    if len(cur_adventures) == 0:
        return None
    else:
        for i in cur_adventures:
            if i[0] == playername:
                remaining_time  = time.time() - i[3]
                print(+remaining_time)
                return remaining_time
        return None

def update_adventure_list():
    if len(cur_adventures) == 0:
        return # No adventures are currently running
    else:
        for i in cur_adventures:
            remaining_time  = time.time() - i[3]
            if round(remaining_time) >= 0:
                main.send_message(i[0],"Adventure finished!")
                print("Adventure finished for player:", i[0])
                
                cur_adventures.remove(i)
                continue
            else:
                print("Adventure still running for player:", i[0])
