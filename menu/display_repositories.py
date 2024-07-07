import curses
import os
import logging
from config_manager import load_token
from github_utils import download_files_from_repo, upload_files_with_replacement, upload_files_without_replacement

logging.basicConfig(filename='logs/logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')

def display_repositories(stdscr, user):
    stdscr.clear()
    repos = user.get_repos()
    repos_list = [repo.name for repo in repos]
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Repository List (select and press Enter to return):")

        for idx, repo in enumerate(repos_list):
            if idx == current_row:
                stdscr.addstr(idx + 1, 0, f"> {repo}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, repo)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(repos_list) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            repo_name = repos_list[current_row]
            logging.info(f"Selected repository '{repo_name}' for submenu.")
            submenu(stdscr, user, repo_name)
            break

def submenu(stdscr, user, repo_name):
    submenu_options = ["Download Files", "Upload Files", "Delete"]
    current_option = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Actions for repository '{repo_name}':")

        for idx, option in enumerate(submenu_options):
            if idx == current_option:
                stdscr.addstr(idx + 1, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, option)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(submenu_options) - 1:
            current_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            action = submenu_options[current_option]
            logging.info(f"Selected option '{action}' for repository '{repo_name}'")
            if action == "Download Files":
                stdscr.clear()
                stdscr.addstr(0, 0, "You selected 'Download'. Press Enter to continue.")
                stdscr.refresh()
                stdscr.getch()
                logging.info("Pressed Enter key to continue downloading files.")
                download_files_submenu(stdscr, user, repo_name)
            elif action == "Upload Files":
                upload_files_submenu(stdscr, user, repo_name)
            elif action == "Delete":
                stdscr.clear()
                stdscr.addstr(0, 0, "You selected 'Delete'. Press Enter to continue.")
                stdscr.refresh()
                stdscr.getch()
                logging.info("Pressed Enter key to continue deletion.")
            break

def download_files_submenu(stdscr, user, repo_name):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Downloading files from repository '{repo_name}':")
    stdscr.addstr(2, 0, "Enter the directory path for download (press Enter to continue):")
    stdscr.refresh()

    curses.echo()
    directory_path = stdscr.getstr(3, 0).decode('utf-8')
    curses.noecho()

    if os.path.isdir(directory_path):
        stdscr.clear()
        stdscr.addstr(0, 0, f"Token: {load_token()}, Repository: {repo_name}, Directory: {directory_path}")
        logging.info(f"Downloading files from repository {repo_name} to directory {directory_path} with token {load_token()}. User login: {user.login}")
        download_files_from_repo(token=load_token(), repo_name=repo_name, directory_path=directory_path, repo_owner=user.login)
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "Error: Entered path is not a directory.")
        stdscr.addstr(2, 0, "Press Enter to continue.")
        stdscr.refresh()
        stdscr.getch()
        logging.error(f"Error downloading files from repository '{repo_name}': entered path '{directory_path}' is not a directory.")

def upload_files_submenu(stdscr, user, repo_name):
    submenu_options = ["Upload with Replacement", "Upload without Replacement"]
    current_option = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Upload options for repository '{repo_name}':")

        for idx, option in enumerate(submenu_options):
            if idx == current_option:
                stdscr.addstr(idx + 1, 0, f"> {option}", curses.A_REVERSE)
            else:
                stdscr.addstr(idx + 1, 0, option)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_option > 0:
            current_option -= 1
        elif key == curses.KEY_DOWN and current_option < len(submenu_options) - 1:
            current_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            action = submenu_options[current_option]
            logging.info(f"Selected upload option '{action}' for repository '{repo_name}'")
            stdscr.clear()
            stdscr.addstr(0, 0, f"Enter the directory path to upload from (press Enter to continue):")
            stdscr.refresh()

            curses.echo()
            directory_path = stdscr.getstr(1, 0).decode('utf-8')
            curses.noecho()

            if os.path.isdir(directory_path):
                token = load_token()
                if action == "Upload with Replacement":
                    upload_files_with_replacement(token=token, repo_name=repo_name, directory_path=directory_path, repo_owner=user.login)
                    logging.info(f"Uploaded files with replacement from '{directory_path}' to repository '{repo_name}'")
                elif action == "Upload without Replacement":
                    upload_files_without_replacement(token=token, repo_name=repo_name, directory_path=directory_path, repo_owner=user.login)
                    logging.info(f"Uploaded files without replacement from '{directory_path}' to repository '{repo_name}'")
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "Error: Entered path is not a directory.")
                stdscr.addstr(2, 0, "Press Enter to continue.")
                stdscr.refresh()
                stdscr.getch()
                logging.error(f"Error uploading files to repository '{repo_name}': entered path '{directory_path}' is not a directory.")
            break

