import subprocess
import curses
from config_manager import load_token, save_token, delete_token
from menu import main_menu, display_settings
from github_utils import get_github_user


def main(stdscr):
    stdscr.clear()

    token = load_token()

    if token is None:
        stdscr.addstr(0, 0, "Enter your GitHub Personal Access Token:")
        stdscr.refresh()

        curses.echo()
        token = stdscr.getstr(1, 0).decode("utf-8")
        curses.noecho()

        save_token(token)

    try:
        user = get_github_user(token)
        while True:
            choice = main_menu(stdscr, user)
            if choice == "settings":
                key = display_settings(stdscr)
                if key == ord('1'):
                    delete_token()
                    stdscr.addstr(5, 0, "Token deleted. Restart the program.")
                    stdscr.refresh()
                    stdscr.getch()
                    break
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, "Authentication or data retrieval error.")
        stdscr.addstr(1, 0, str(e))
        stdscr.addstr(3, 0, "Delete the config/access.json file for re-authentication.")

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
