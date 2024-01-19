import os
from re import search
from click import clear
import pyautogui
import json
import time
#import playsound

def get_file_path():
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
def perform_searches(queries, search_box, search_button, delay, get_started):
    previous_query = None
    for i, query in enumerate(queries):
        if get_started:
            # Scroll to the top of the page
            pyautogui.click(search_box)
            pyautogui.press('home')
            time.sleep(2)
            pyautogui.click(get_started)
            #pyautogui.scroll(6000*10)
            time.sleep(2)
            #pyautogui.click(get_started)
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
        time.sleep(2)
        #pyautogui.press('enter')
        time.sleep(2)
        #pyautogui.press('enter')   
        pyautogui.click(search_button) # can be redundant but just in case
        time.sleep(delay)  # Wait for the search to complete
    print("All searches are complete.")
    #playsound.playsound('done_sound.mp3')

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
    file_path = get_file_path()
    try:
        queries = read_queries_from_file(file_path)
        if not isinstance(queries, list):
            raise ValueError("The JSON content is not a list of queries.")
        delay, setting = get_delay_setting()
        buffer_percentage = get_buffer_percentage()  # New function to get the buffer percentage
        total_time = len(queries) * (delay + 2)  # Include the 2 second delay after each search
        buffer_time = total_time * buffer_percentage / 100  # Calculate the buffer time
        total_time += buffer_time  # Add the buffer time to the total time
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Estimated completion time (including buffer): {hours} hours, {minutes} minutes, and {seconds} seconds.")
        if setting == 'gptresearcher':
            get_started = get_started_button_coordinates()
        else:
            get_started = None
        search_box = get_search_box_coordinates()
        search_button = get_search_enter_coordinates()
        perform_searches(queries, search_box, search_button, delay, get_started)
    except FileNotFoundError:
        print(f"No file found at {file_path}")
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
