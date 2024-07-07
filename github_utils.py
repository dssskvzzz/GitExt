from github import Github
import os 
import logging
import curses
import time

logging.basicConfig(filename='logs/logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')

def get_github_user(token):
    g = Github(token)
    return g.get_user()

def download_files_from_repo(token, repo_name, directory_path, repo_owner): 
    g = Github(token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')

    stdscr = None
    total_files = 0
    count = 0

    def download_contents(contents, current_path):
        nonlocal count, total_files
        
        for content in contents:
            count += 1
            stdscr.clear()
            stdscr.addstr(0, 0, f"Downloading files: {count}/{total_files}")
            stdscr.addstr(1, 0, f"Current file/directory: {content.name}")
            
            progress = int(count / total_files * 100)
            if progress > 100:
                progress = 100
            
            animation = '#' * (progress // 2) + ' ' * (50 - progress // 2)
            stdscr.addstr(2, 0, f"Progress: {progress}% [{animation}]")
            
            stdscr.refresh()

            if content.type == "dir":
                subdir_contents = repo.get_contents(content.path)
                download_contents(subdir_contents, os.path.join(current_path, content.name))
            else:
                file_content = repo.get_contents(content.path)
                file_path = os.path.join(current_path, content.name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as file:
                    file.write(file_content.decoded_content)

    try:
        contents = repo.get_contents("")
        total_files = len(contents)

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        # Start download
        download_contents(contents, directory_path)

    finally:
        if stdscr:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

import os
import logging
from github import Github

def upload_files_with_replacement(token, repo_name, directory_path, repo_owner):
    g = Github(token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')
    
    # Step 1: Delete all existing contents in the repository
    contents = repo.get_contents("")
    for content_file in contents:
        try:
            repo.delete_file(content_file.path, "Deleting existing file or folder", content_file.sha)
            logging.info(f"Deleted existing file or folder: {content_file.path}")
        except Exception as e:
            logging.error(f"Failed to delete {content_file.path}: {e}")
    
    # Step 2: Upload new files and folders
    total_files = 0
    count = 0

    def upload_directory(path, repo_path):
        nonlocal count, total_files

        for root, dirs, files in os.walk(path):
            for file in files:
                count += 1
                print(f"Uploading files: {count}/{total_files}")
                print(f"Current file: {file}")
                
                progress = int(count / total_files * 100)
                if progress > 100:
                    progress = 100
                
                animation = '#' * (progress // 2) + ' ' * (50 - progress // 2)
                print(f"Progress: {progress}% [{animation}]")

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as file_content:
                        content = file_content.read()
                        repo_path_file = os.path.normpath(os.path.relpath(file_path, path)).replace(os.path.sep, '/')
                        try:
                            repo.create_file(repo_path_file, "Creating file", content)
                            logging.info(f"Uploaded new file: {repo_path_file}")
                        except Exception as e:
                            logging.error(f"Failed to upload {repo_path_file}: {e}")
                except Exception as e:
                    logging.error(f"An error occurred while uploading {file}: {e}")
                    continue

    # Calculate total files for progress tracking
    for root, dirs, files in os.walk(directory_path):
        total_files += len(files)

    # Upload files from directory_path to the root of the repository
    upload_directory(directory_path, "")

            
def upload_files_without_replacement(token, repo_name, directory_path, repo_owner):
    g = Github(token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')

    # Step 1: Get all existing files in the repository
    existing_files = repo.get_contents("")
    existing_file_paths = {file.path for file in existing_files}

    # Step 2: Upload new files from specified directory
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'rb') as file_content:
                content = file_content.read()

                if file_name in existing_file_paths:
                    # File already exists, replace it
                    existing_file = repo.get_contents(file_name)
                    repo.update_file(existing_file.path, f"Updated {file_name}", content, existing_file.sha)
                    print(f'File {file_name} updated in repository {repo_name}.')
                else:
                    # File does not exist, create new file
                    repo.create_file(file_name, f"Added {file_name}", content)
                    print(f'File {file_name} created in repository {repo_name}.')