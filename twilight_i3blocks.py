#!/home/coljac/anaconda3/bin/python
from twilight import *
from pathlib import Path

color_default = '#777777' # Default gray
color_background = '#000000' 
color_active = '#FF0000' # Waiting turn (friends)
color_strangers = '#D608D2' # Waiting turn (anyone)
color_both = '#01C626' # Waiting turns (both)
flag_white = "🏳️"
flag_black = "🏴"

def main(argv):
    here = str(Path(__file__).resolve().parent)
    if os.path.exists(f"{here}/friends.txt"):
        with open(f"{here}/friends.txt", "r") as f:
            friends = f.read().splitlines()
    else:
        friends = []

    button = os.getenv("BLOCK_BUTTON", "0") 
    clicked = button == "1" # Clicked; clear status, mark read

    # Middle click: launch TS
    if button == "2": 
        launch = "i3-msg -q exec '/usr/games/steam -applaunch 406290'"
        # launch = "/home/coljac/dev/python/wtf/start_ts.sh &"
        os.system(launch)
        clicked = True

    # if button == "3": 
        # You could do something different here

    response = flag_black
    color = color_default
    
    if not clicked:
        count, gameIds, playerCounts = get_counts()
        friends_games = strangers_games = False
        response = flag_white if count > 0 else flag_black
        for k, v in playerCounts.items():
            if k in friends:
                friends_games = True
            else:
                strangers_games = True

        if friends_games and strangers_games:
            color = color_both
        elif friends_games:
            color = color_active
        elif strangers_games:
            color = color_strangers

    sys.stdout.write(f"{response}\n{response}\n{color}\n{color_background}")
    sys.stdout.flush()

    if clicked:
        markread(archive=True)

if __name__ == '__main__':
    main(sys.argv[1:])


