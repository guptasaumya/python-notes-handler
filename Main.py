# -*- coding: utf-8 -*-
# Python Project
# Python Notes Handler
# Saumya Gupta, DS


# Import required packages
from os import path
from UserInterface import *


def retrieve_max_id():
    """
    Retrieves maximum ID value from saved notes to help continue from previous state
    :return: (int) Maximum note ID
    """
    notesDictList = []

    # Retrieve notes data if there exists non empty notes file
    if (path.exists('Notes.txt')) and (path.getsize('Notes.txt') != 0):
        with open('Notes.txt', 'r') as f:
            for line in f.readlines():
                # Using yaml to parse dictionary object from string
                notesDictList.append(yaml.safe_load(line))

        # Store in pandas dataframe for ease of access
        notesDF = pd.DataFrame(notesDictList)

        # Convert notes ID column from string to integer type
        notesDF['Note ID'] = pd.to_numeric(notesDF['Note ID'])

        # Generate ID for next new note to be created
        max_id = notesDF['Note ID'].max()

        return max_id


def display_menu():
    """
    Displays menu item
    :return: None
    """
    print("\n\n" + str(60 * '*'))

    print('Welcome to your Notes Handler!')
    print("\nChoose one of the below menu options and enter to proceed: \n(For example, enter '1' to add a new "
          "note.)")

    print('\n1. Add a new note.')
    print('2. Read a specific note.')
    print('3. Update a specific note.')
    print('4. Delete a specific note.')
    print('5. Add note completion date.')
    print('6. Find number of days it took to complete the notes.')
    print('7. Save all notes to file.')
    print('8. Restore file contents.')
    print('9. Show notes statistics.')
    print('10. Exit.')

    print(str(60 * '*'))


def validate_user_input(user_input):
    """
    Validates user input
    :param user_input: Input entered by user, in response to primary menu item
    :return: (bool) True if user input is expected, False otherwise
    """
    if user_input not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        print('\nERROR : Invalid Input!\nEnter from the given options above (ranging 1-10).')
        print('Starting Over...')

        return False

    else:
        return True


def main():
    """
    Main program:
    Takes and validates user input for primary menu item;
    Interacts with UserInterface class
    :return: None
    """
    # Loop to keep displaying primary menu item unless user wants to terminate session
    while True:
        # Call function to display primary menu item
        display_menu()

        # Get input in response to primary menu item
        user_choice = input('\nEnter selection: ')

        # Call function validate user choice
        validation_output = validate_user_input(user_choice)

        if not validation_output:
            # Go to start of loop in case of invalid input
            continue

        # Create object
        user_interface_object = UserInterface(user_choice)

        # Call instance method to pass control to class
        user_interface_object.handle_user_input()


if __name__ == '__main__':
    main()

# This is end of script.
