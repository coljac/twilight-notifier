#!env python
import pystray
from PIL import Image, ImageDraw
from twilight import *
from pathlib import Path
from time import sleep
import os
import webbrowser
from threading import Event

sleeptime = 300

color_default = '#777777' # Default gray
color_background = '#000000' 
color_active = '#FF0000' # Waiting turn (friends)
color_strangers = '#D608D2' # Waiting turn (anyone)
color_both = '#01C626' # Waiting turns (both)
friends = []
here = str(Path(__file__).resolve().parent)            
running = Event()

def create_image(color):                                   
    height=32                                              
    width=32                                               
    image = Image.new('RGB', (width, height), color)      
    image2 = Image.open("icon.png")                 
    image.paste(image2, (0, 0), image2)
    return image


def run(icon):
    slept = 1e10
    while not running.is_set():
        check(icon)
        running.wait(sleeptime)
    return

def check(icon):
    color = color_default
    colors = {"friends": color_active, 
            "strangers": color_strangers, 
            "none": color_default, 
            "both": color_both}


    result = "none"
    if True:
        count, gameIds, playerCounts = get_counts()
        friends_games = strangers_games = False
        for k, v in playerCounts.items():
            if k in friends:
                friends_games = True
            else:
                strangers_games = True

        if friends_games and strangers_games:
            result = "both"
        elif friends_games:
            result = "friends"
        elif strangers_games:
            result = "strangers"

    color = colors[result]
    icon.icon = create_image(color)
    icon.visible = True

def clear(icon):
    markread(archive=False)
    icon.icon = create_image(color_default)
    icon.visible = True

def launch(icon):
    # launch = "steam -applaunch 406290"
    url = "steam://run/406290"
    # os.system(launch)
    webbrowser.open(url, new=2)
    clear(icon)

def quit(icon):
    running.set()
    icon.stop()

def main(argv):
    if os.path.exists(f"{here}/friends.txt"):
        with open(f"{here}/friends.txt", "r") as f:
            friends.extend(f.read().splitlines())

    menu = pystray.Menu(
            pystray.MenuItem("Launch", launch),
            pystray.MenuItem("Check now", check),
            pystray.MenuItem("Clear", clear),
            pystray.MenuItem("Quit", quit),
            )

    icon = pystray.Icon("TS Notifier", 
            icon=create_image(color_default),
            title="TS Notifier",
            menu=menu)
    icon.visible = True
    icon.run(run)

if __name__ == '__main__':
    main(sys.argv[1:])


