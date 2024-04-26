import os
from re import search
from click import clear
import pyautogui
import json
import time
#import playsound
def get_file_path():
    choice_type = input("Choose 'folder' to process all files in a folder or 'file' to process a single file: ").strip().lower()
    if choice_type == 'folder':
        print("Folders available:")
        # Assuming folders are directly within "AutomatedSearch/jsons/"
        folders = [f for f in os.listdir("AutomatedSearch/jsons/") if os.path.isdir(os.path.join("AutomatedSearch/jsons/", f))]
        for i, folder in enumerate(folders):
            print(f"{i+1}. {folder}")
        choice = int(input("Choose a folder by number: ")) - 1
        return "AutomatedSearch/jsons/" + folders[choice], 'folder'
    else:  # Default to 'file'
        # Your existing logic for choosing a file
        json_files = [f for f in os.listdir("AutomatedSearch/jsons/") if f.endswith('.json')]
        text_files = [f for f in os.listdir("AutomatedSearch/jsons/") if f.endswith('.txt')]
        available_files = [file for file in json_files if file.replace('.json', '.txt') not in text_files]
        for i, file in enumerate(available_files):
            print(f"{i+1}. {file}")
        choice = int(input("Choose a file by number: ")) - 1
        return "AutomatedSearch/jsons/" + available_files[choice]


def get_delay_setting():
    print("Choose a delay setting: bard (60 seconds), bing (2 minutes), gptresearcher (2 minutes), or custom.")
    setting = input("Your choice: ")
    if setting == "bard":
        return 60, 'bard'
    elif setting == "bing":
        return 80, 'bing'
    elif setting == "gptresearcher":
        return 265, 'gptresearcher'
    elif setting == "custom":
        delay = input("Enter the delay in seconds: ")
        return int(delay), 'custom'
    else:
        print("Invalid choice. Defaulting to 5 seconds.")
        return 5

def get_search_box_coordinates():
    print(f"Please move your cursor to the search box within the next 5 seconds.")
    time.sleep(5)  # Wait for the specified delay
    return pyautogui.position()
def get_search_enter_coordinates():
    print(f"Please move your cursor to the enter button within the next 5 seconds.")
    time.sleep(5)  # Wait for the specified delay
    return pyautogui.position()
def perform_searches(queries, search_box, search_button, delay, get_started, file_path):
    output_file = "search_log.txt"  # Define the log file name
    previous_query = None
    file_written = False  # Flag to check if the file name has been written

    for i, query in enumerate(queries):
        if get_started:
            # Scroll to the top of the page
            pyautogui.click(search_box)
            pyautogui.press('home')
            time.sleep(2)
            pyautogui.click(get_started)
            # Additional logic if needed for scrolling or clicking "get started" again
            time.sleep(2)
        pyautogui.click(search_box)
        pyautogui.click(search_box)
        if previous_query:
            query_length = len(previous_query)
            pyautogui.press('backspace', presses=query_length*2)
        pyautogui.typewrite(query, interval=0.1)
        pyautogui.press('enter')
        print(f"Searching for: {query}")
        previous_query = query
        time.sleep(2)  # These waits ensure that the UI has time to update
        pyautogui.click(search_button)  # can be redundant but just in case
        time.sleep(delay)  # Wait for the search to complete

        # Writing to file
        with open(output_file, 'a') as f:  # Open the file in append mode
            if not file_written:  # If the file name hasn't been written yet
                f.write(f"File: {os.path.basename(file_path)}\n")  # Write the file name
                file_written = True  # Set the flag to True after writing
            f.write(f"{query}\n")  # Append the query

    print("All searches are complete.")


def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_buffer_percentage():
    print("Enter a buffer percentage to add to the estimated completion time.")
    buffer_percentage = input("Your choice (default is 10%): ")
    return int(buffer_percentage) if buffer_percentage else 10
def get_started_button_coordinates():
    print(f"Please move your cursor to the get started button within the next 5 seconds.")
    time.sleep(5)  # Wait for the specified delay
    return pyautogui.position()
def main():
    file_path_or_folder, choice_type = get_file_path()
    delay, setting = get_delay_setting()  # Select delay setting once
    buffer_percentage = get_buffer_percentage()  # Get buffer percentage once

    if choice_type == 'folder':
        json_files = [os.path.join(file_path_or_folder, f) for f in os.listdir(file_path_or_folder) if f.endswith('.json')]
    else:
        json_files = [file_path_or_folder]

    for file_path in json_files:
        try:
            print(f"Processing file: {file_path}")
            queries = read_queries_from_file(file_path)
            if not isinstance(queries, list):
                raise ValueError("The JSON content is not a list of queries.")

            # No need to retrieve delay and buffer settings again for each file
            # The logic for calculating estimated completion time and performing searches remains unchanged

            if setting == 'gptresearcher':
                get_started = get_started_button_coordinates()
            else:
                get_started = None

            search_box = get_search_box_coordinates()
            search_button = get_search_enter_coordinates()

            perform_searches(queries, search_box, search_button, delay, get_started, file_path)

        except FileNotFoundError:
            print(f"No file found at {file_path}")
        except json.JSONDecodeError:
            print("Failed to decode JSON. Please check the file content.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
if __name__ == "__main__":
    main()
