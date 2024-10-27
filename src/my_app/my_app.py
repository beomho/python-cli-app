import argparse
import mpv
from ._version import __version__
from simple_term_menu import TerminalMenu
import requests
from bs4 import BeautifulSoup
from .Youtube import Youtube 
from .Spinner import Spinner 

def my_log(loglevel, component, message):
    #print('[{}] {}: {}'.format(loglevel, component, message))
    return

player = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)

player.fullscreen = True
player.loop_playlist = 'inf'
# Option access, in general these require the core to reinitialize
player['vo'] = 'gpu'

def main(parser=argparse.ArgumentParser()):

    #print("Executing 'main()' from my app!")
    parser.add_argument("-v", "--version", action="store_true", help="Shows the app version.")
    parser.add_argument("-t", "--square", type=int, required=False, help="Square a number.")
    parser.add_argument("-s", "--search", type=str, required=False, help="Search Title")

    args = parser.parse_args()

    if args.version:
        return __version__
    elif args.square:
        return square(args.square)
    elif args.search:

        query = args.search
        maxResults= 20 

        playList = {}

        spinner = Spinner()
        spinner.start("Searching...")

        obj=Youtube(query,maxResults)
        playList = obj.main()

        terminal_menu = TerminalMenu([*playList.keys()])
        spinner.stop()
        menu_entry_index = terminal_menu.show()

        selectedUrl = list(playList.values())[menu_entry_index-1]
        print(f"You have selected {selectedUrl}!")


        player = mpv.MPV(log_handler=my_log, ytdl=True, input_default_bindings=True, input_vo_keyboard=True)

        for key, value in playList.items():
            player.playlist_append(value) 

        player.playlist_pos = 0
        spinner.start("Waiting...")
        #player.play(selectedUrl)
        while True:
            # To modify the playlist, use player.playlist_{append,clear,move,remove}. player.playlist is read-only
            #print(player.playlist)
            #spinner.stop()
            player.wait_for_playback()
            #player.wait_for_playback()



        return "END"
    else:
        return "Hello World"


@player.on_key_press('s')
def my_s_binding():
    pillow_img = player.screenshot_raw()
    pillow_img.save('screenshot.png')

@player.on_key_press('F10')
def my_s_binding_F10():
    print("F10")

def square(x: int):
    y = x * x
    print(f"The square of {x} is {y}!")
    return y

del player
