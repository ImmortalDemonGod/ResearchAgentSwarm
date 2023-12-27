import os
import pyautogui
import json
import time
import playsound

def get_file_path():
    json_files = [f for f in os.listdir("AutomatedSearch/jsons/") if f.endswith('.json')]
    text_files = [f for f in os.listdir("AutomatedSearch/jsons/") if f.endswith('.txt')]
    available_files = [file for file in json_files if file.replace('.json', '.txt') not in text_files]
    for i, file in enumerate(available_files):
        print(f"{i+1}. {file}")
    choice = int(input("Choose a file by number: ")) - 1
    return "jsons/" + available_files[choice]

def get_delay_setting():
    print("Choose a delay setting: bard (60 seconds), bing (2 minutes), or custom.")
    setting = input("Your choice: ")
    if setting == "bard":
        return 60
    elif setting == "bing":
        return 80
    elif setting == "custom":
        delay = input("Enter the delay in seconds: ")
        return int(delay)
    else:
        print("Invalid choice. Defaulting to 5 seconds.")
        return 5

def get_search_box_coordinates():
    print(f"Please move your cursor to the search box within the next 5 seconds.")
    time.sleep(5)  # Wait for the specified delay
    return pyautogui.position()

def get_user_input():
    return input("Do you want to continue? (yes/no): ")

def perform_searches(queries, coordinates, delay):
    x, y = coordinates
    for i, query in enumerate(queries):
        if i > 0 and i % 25 == 0:
            user_input = get_user_input()
            if user_input.lower() != 'yes':
                break
        pyautogui.click(x, y)
        pyautogui.typewrite(query)
        pyautogui.press('enter')
        print(f"Searching for: {query}")
        time.sleep(2)
        pyautogui.press('enter')  
        time.sleep(delay)  # Wait for the search to complete
    print("All searches are complete.")
    playsound.playsound('AutomatedSearch/done_sound.mp3')

def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_buffer_percentage():
    print("Enter a buffer percentage to add to the estimated completion time.")
    buffer_percentage = input("Your choice (default is 10%): ")
    return int(buffer_percentage) if buffer_percentage else 10

def main():
    file_path = get_file_path()
    try:
        queries = read_queries_from_file(file_path)
        if not isinstance(queries, list):
            raise ValueError("The JSON content is not a list of queries.")
        delay = get_delay_setting()
        buffer_percentage = get_buffer_percentage()  # New function to get the buffer percentage
        total_time = len(queries) * (delay + 2)  # Include the 2 second delay after each search
        buffer_time = total_time * buffer_percentage / 100  # Calculate the buffer time
        total_time += buffer_time  # Add the buffer time to the total time
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Estimated completion time (including buffer): {hours} hours, {minutes} minutes, and {seconds} seconds.")
        coordinates = get_search_box_coordinates()
        perform_searches(queries, coordinates,delay)
    except FileNotFoundError:
        print(f"No file found at {file_path}")
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
