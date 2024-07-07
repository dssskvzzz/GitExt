def display_projects(stdscr, user):
    stdscr.clear()
    stdscr.addstr(0, 0, "List of Projects:")
    projects = user.get_projects()
    row = 1
    for project in projects:
        stdscr.addstr(row, 0, project.name)
        row += 1
    stdscr.addstr(row + 1, 0, "Press any key to return to the menu...")
    stdscr.refresh()
    stdscr.getch()
