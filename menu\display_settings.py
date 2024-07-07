import os
from config_manager import CONFIG_PATH

def display_settings(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Settings:")
    stdscr.addstr(1, 0, "1. Delete token and exit")
    stdscr.addstr(3, 0, "Press '1' to delete the token or any other key to return to the menu...")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord('1'):
        os.remove(CONFIG_PATH)
        stdscr.addstr(5, 0, "Token deleted. Restart the program.")
        stdscr.refresh()
        stdscr.getch()
        exit()
    return key
