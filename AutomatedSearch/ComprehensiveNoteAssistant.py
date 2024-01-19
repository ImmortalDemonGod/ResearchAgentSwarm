import time
import pyautogui
#import playsound

def get_search_box_coordinates():
    """
    Prompts the user to move the cursor to Claude's input field and returns the coordinates.
    """
    print(f"Please move your cursor to Claude's input field within the next 5 seconds.")
    time.sleep(5)
    return pyautogui.position()

def move_cursor_and_type(coordinates, text):
    """
    Moves the cursor to a specific position and types the given text.
    """
    pyautogui.click(coordinates)
    pyautogui.typewrite(text)
    pyautogui.press('enter')

def create_notes_with_claude(coordinates):
    """
    Instructs Claude to create comprehensive notes using the provided text.
    """
    note_creation_text = "Let's create a comprehensive set of notes using the text provided"
    move_cursor_and_type(coordinates, note_creation_text)
    time.sleep(60)  # Adjust this delay based on Claude's response time

def evaluate_notes_with_claude(coordinates):
    """
    Asks Claude to critically evaluate the current set of notes for overlooked areas.
    """
    evaluation_text = ("Please critically evaluate our current set of notes in order to find overlooked areas that the text covers but our notes don't. Provide your feedback in a structured list format, starting each point with a number followed by a period. For example: 1. First point: [brief description] 2. Second point: [brief description] ...and so on. Focus on key areas such as concepts, techniques, and insights that are missing or underexplored.")
    move_cursor_and_type(coordinates, evaluation_text)
    time.sleep(60)  # Adjust this delay based on Claude's response time

def read_overlooked_points_from_file(file_path):
    """
    Reads overlooked points from a file, assuming each point is in a separate paragraph.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Splitting by line breaks and filtering out non-point lines
    lines = content.split('\n')
    points = [line for line in lines if line.startswith(tuple(str(i) for i in range(1, 10)))]

    return points

def append_to_notes(points, coordinates):
    """
    Appends each point to the notes.
    """
    for point in points:
        notes = f"Adding to our notes use the text to answer/address: {point}"
        move_cursor_and_type(coordinates, notes)
        time.sleep(60)  # Adjust this delay based on Claude's response time

def main():
    """
    Main function to automate the process of creating and refining notes with Claude.
    """
    coordinates = get_search_box_coordinates()
    # ask the user if they want to skip the create notes step
    if input("Do you want to skip the create notes step? (yes/no): ").lower() == 'yes':
        print("Skipping the create notes step.")
    else:
        create_notes_with_claude(coordinates)
    # ask the user if they want to skip the evaluate notes step
    if input("Do you want to skip the evaluate notes step? (yes/no): ").lower() == 'yes':
        print("Skipping the evaluate notes step.")
    else:
        evaluate_notes_with_claude(coordinates)
    #playsound.playsound('AutomatedSearch/done_sound.mp3')

    # Prompt to check if the file with overlooked points is ready
    if input("Is the file with overlooked points ready? (yes/no): ").lower() == 'yes':
        file_path = "AutomatedSearch/overlooked_points.txt"
        overlooked_points = read_overlooked_points_from_file(file_path)
        append_to_notes(overlooked_points, coordinates)
    else:
        print("Please prepare the file and run the script again.")

    #playsound.playsound('AutomatedSearch/done_sound.mp3')
    print("All tasks are complete.")

if __name__ == "__main__":
    main()
