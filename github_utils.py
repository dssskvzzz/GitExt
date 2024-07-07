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
        # Clean up curses and return to normal terminal mode
        if stdscr:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

def upload_files_with_replacement(token, repo_name, directory_path, repo_owner):
    g = Github(token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')

    stdscr = None
    total_files = 0
    count = 0

    def upload_directory(path, repo_path):
        nonlocal count, total_files

        for root, dirs, files in os.walk(path):
            for file in files:
                count += 1
                stdscr.clear()
                stdscr.addstr(0, 0, f"Uploading files: {count}/{total_files}")
                stdscr.addstr(1, 0, f"Current file: {file}")

                progress = int(count / total_files * 100)
                if progress > 100:
                    progress = 100

                animation = '#' * (progress // 2) + ' ' * (50 - progress // 2)
                stdscr.addstr(2, 0, f"Progress: {progress}% [{animation}]")

                stdscr.refresh()

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as file_content:
                        content = file_content.read()
                        repo_file_path = os.path.relpath(file_path, path)
                        repo_file_path = os.path.join(repo_path, repo_file_path)  # Correct path for repo
                        try:
                            # Check if it's a directory and create it if not exists
                            if os.path.isdir(file_path):
                                try:
                                    repo.get_contents(repo_file_path)
                                except:
                                    repo.create_file(repo_file_path, "Creating folder", "")
                            else:
                                # Otherwise, upload the file
                                try:
                                    repo_file = repo.get_contents(repo_file_path)
                                    repo.update_file(repo_file.path, "Replacing file", content, repo_file.sha)
                                    logging.info(f"Replaced file: {repo_file_path}")
                                except:
                                    repo.create_file(repo_file_path, "Creating file", content)
                                    logging.info(f"Created file: {repo_file_path}")
                        except Exception as e:
                            logging.error(f"An error occurred while processing {file_path}: {e}")
                            continue  # Skip to the next file
                except Exception as e:
                    logging.error(f"An error occurred while opening {file_path}: {e}")
                    continue  # Skip to the next file

            for dir in dirs:
                count += 1
                stdscr.clear()
                stdscr.addstr(0, 0, f"Uploading files: {count}/{total_files}")
                stdscr.addstr(1, 0, f"Current file: {dir}")

                progress = int(count / total_files * 100)
                if progress > 100:
                    progress = 100

                animation = '#' * (progress // 2) + ' ' * (50 - progress // 2)
                stdscr.addstr(2, 0, f"Progress: {progress}% [{animation}]")

                stdscr.refresh()

                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as file_content:
                        content = file_content.read()
                        repo_file_path = os.path.relpath(file_path, path)
                        repo_file_path = os.path.join(repo_path, repo_file_path)  # Correct path for repo
                        try:
                            # Check if it's a directory and create it if not exists
                            if os.path.isdir(file_path):
                                try:
                                    repo.get_contents(repo_file_path)
                                except:
                                    repo.create_file(repo_file_path, "Creating folder", "")
                            else:
                                # Otherwise, upload the file
                                try:
                                    repo_file = repo.get_contents(repo_file_path)
                                    repo.update_file(repo_file.path, "Replacing file", content, repo_file.sha)
                                    logging.info(f"Replaced file: {repo_file_path}")
                                except:
                                    repo.create_file(repo_file_path, "Creating file", content)
                                    logging.info(f"Created file: {repo_file_path}")
                        except Exception as e:
                            logging.error(f"An error occurred while processing {file_path}: {e}")
                            continue  # Skip to the next file
                except Exception as e:
                    logging.error(f"An error occurred while opening {file_path}: {e}")
                    continue  # Skip to the next file
                    
    
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        for _, _, files in os.walk(directory_path):
            total_files += len(files)

        upload_directory(directory_path, "")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if stdscr:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

def upload_files_without_replacement(token, repo_name, directory_path, repo_owner):
    g = Github(token)
    repo = g.get_repo(f'{repo_owner}/{repo_name}')

    stdscr = None
    total_files = 0
    count = 0

    def upload_directory(path, repo_path):
        nonlocal count, total_files

        for root, dirs, files in os.walk(path):
            for file in files:
                count += 1
                stdscr.clear()
                stdscr.addstr(0, 0, f"Uploading files: {count}/{total_files}")
                stdscr.addstr(1, 0, f"Current file: {file}")
                
                progress = int(count / total_files * 100)
                if progress > 100:
                    progress = 100
                
                animation = '#' * (progress // 2) + ' ' * (50 - progress // 2)
                stdscr.addstr(2, 0, f"Progress: {progress}% [{animation}]")
                
                stdscr.refresh()

                file_path = os.path.join(root, file)
                with open(file_path, "rb") as file_content:
                    content = file_content.read()
                    repo_path_file = os.path.relpath(file_path, path)
                    try:
                        repo.get_contents(repo_path_file)
                        logging.info(f"File {repo_path_file} already exists. Skipping.")
                    except:
                        repo.create_file(repo_path_file, "Creating file", content)
    
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        # Count the total number of files
        for _, _, files in os.walk(directory_path):
            total_files += len(files)

        # Start upload
        upload_directory(directory_path, "")

    finally:
        # Clean up curses and return to normal terminal mode
        if stdscr:
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()