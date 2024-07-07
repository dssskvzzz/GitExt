import curses
from .display_info import display_info
from .display_repositories import display_repositories
from .display_projects import display_projects
from .display_settings import display_settings

def main_menu(stdscr, user):
    current_row = 0
    menu = ["Information", "Repositories", "Projects", "Settings"]

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select an option and press Enter:")
        for idx, row in enumerate(menu):
            if idx == current_row:
                stdscr.addstr(idx + 1, 0, f"> {row}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, row)

        stdscr.clrtoeol()
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                display_info(stdscr, user)
            elif current_row == 1:
                display_repositories(stdscr, user)
            elif current_row == 2:
                display_projects(stdscr, user)
            elif current_row == 3:
                return "settings"
