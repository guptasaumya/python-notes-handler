# -*- coding: utf-8 -*-
# Python Project
# Python Notes Handler
# Saumya Gupta, DS


# Import required packages
import sys
import os
import datetime
import pandas as pd
from tabulate import tabulate
import yaml
from Note import *
from Main import retrieve_max_id

# Customize pandas behaviour to display more number of columns than 5
pd.set_option('display.max_columns', 10)

# Call function to retrieve maximum ID value from saved notes to help continue from previous state
id_max = retrieve_max_id()


class userInterface:
    """
    Represents user interface

    Class Attributes
    ----------
    idCounter : (int) Represent note IDs; increments on note creation
    noteObjectList : (dict) Dictionary with note IDs as keys and corresponding 'Note' class objects as values

    Instance Attributes
    ----------
    userChoice : (int) Input entered by user, in response to primary menu item

    Methods
    -------
    handle_user_input() : Decides which handler to call based on 'userChoice'
    handle_create() : Creates note object
    handle_read() : Displays specific note object data
    handle_update() : Updates specific note object
    handle_delete() : Deletes specific note object
    handle_add_completion_date() : Adds/updates completion date to/of note object
    handle_find_days_to_complete() : Displays number of days it took to complete note
    handle_save_in_file() : Saves all current note objects into file
    handle_restore_file_contents() : Restores notes from saved file; DOES NOT overwrite already existing notes
    handle_show_stats() : Display notes statistics focussing note completion
    print_notes_list() : Displays list of notes
    is_note_present(idInput) : Checks if concerned note is present in 'noteObjectList'
    """
    idCounter = id_max if id_max else 0
    noteObjectList = {}

    def __init__(self, userChoice):
        """
        Initializes note attributes
        :param userChoice: Input entered by user, in response to primary menu item
        """
        self.userChoice = userChoice

    def handle_user_input(self):
        """
        Decides which handler to call based on 'userChoice', ex. calls 'handle_create'() is 'userChoice' is '1';
        Responsible to exit program (session) if 'userChoice' is '10'
        :return: None
        """
        if self.userChoice == '1':
            UserInterface.handle_create(self)

        elif self.userChoice == '2':
            UserInterface.handle_read(self)

        elif self.userChoice == '3':
            UserInterface.handle_update(self)

        elif self.userChoice == '4':
            UserInterface.handle_delete(self)

        elif self.userChoice == '5':
            UserInterface.handle_add_completion_date(self)

        elif self.userChoice == '6':
            UserInterface.handle_find_days_to_complete(self)

        elif self.userChoice == '7':
            UserInterface.handle_save_in_file(self)

        elif self.userChoice == '8':
            UserInterface.handle_restore_file_contents(self)

        elif self.userChoice == '9':
            UserInterface.handle_show_stats(self)

        elif self.userChoice == '10':
            print('\nSad to see you go. See you soon again!')

            sys.exit()

    def handle_create(self):
        """
        Takes and validates note properties from user;
        Creates new note object;
        Appends new note object to 'noteObjectList'
        :return: None
        """
        # Increment note counter attribute
        UserInterface.idCounter += 1

        # Initially consider empty input
        emptyTitleInput = True

        while emptyTitleInput:
            # Take input from user
            titleInput = input('Enter title (An apt title to summarize the note) : ')

            if (not titleInput == '') and (not titleInput.isspace()):
                # Set empty input to False if input is one desired to break loop
                emptyTitleInput = False

            else:
                # Prompt user to enter correct input next time
                print("ERROR : Note title cannot be empty.")

        # Similar code for text input
        emptyTextInput = True

        while emptyTextInput:
            textInput = input("Enter text (Note's main body) : ")

            if (not textInput == '') and (not textInput.isspace()):
                emptyTextInput = False

            else:
                print("ERROR : Note text cannot be empty.")

        # Similar code for input regarding completion status
        wrongInputCheck = True

        while wrongInputCheck:
            # Convert to lower case to accommodate all cases
            isCompletedInput = input("Is this note complete? (Y/N) : ").lower()

            if isCompletedInput in ['y', 'n', 'yes', 'no']:
                # Set note property according to user input
                isCompletedInput = True if isCompletedInput in ['y', 'yes'] else False

                wrongInputCheck = False

            else:
                print("\nERROR : Invalid Input!\nEnter: 'Y' for completed and 'N' for not completed.")

        # Current timestamp for creation date
        dateCreated = datetime.datetime.now()

        # Create note object
        note = Note(UserInterface.idCounter, dateCreated, titleInput, textInput, isCompletedInput)

        # If note is marked complete set completion date as current timestamp
        if note.isCompleted:
            note.mark_complete(datetime.datetime.now())

        # Append note object to keep track of created notes
        UserInterface.noteObjectList[UserInterface.idCounter] = note

        # Prompt user what has changed
        print(
            "\nSUCCESS : A new Note - '" + titleInput + "' - has been created with ID: " + str(UserInterface.idCounter))

    def handle_read(self):
        """
        Takes and validates note ID from user:
        Displays corresponding note object data
        :return: (str) 'Error 1' if no notes have been created;
                       'Error 2' if note corresponding to entered ID hasn't been created by user
                       'Error 3' if note ID entered is invalid data type
        """
        try:
            # Call function to check if no notes have been created
            notesListIsEmpty = UserInterface.print_notes_list(self)

            if notesListIsEmpty:
                return 'Error 1'

            idInput = int(input('\nEnter note ID: '))

            # Call function to check if note is present in list
            noteIsPresent = UserInterface.is_note_present(self, idInput)

            if not noteIsPresent:
                return 'Error 2'

            # Call function to get all data for desired note
            noteData = UserInterface.noteObjectList[idInput].get_all_data()

            # Print note data in tabular form
            print('\nHere is note ID ' + str(idInput) + ':\n')
            print(tabulate(list(map(list, noteData.items())), ["Attribute", "Value"]))

            # Return note ID selected for further use
            return idInput

        except ValueError:
            print('\nERROR : Invalid Input! Please enter a valid note ID number.')
            print('Starting Over...')

            return 'Error 3'

    def handle_update(self):
        """
        Calls 'handle_read()';
        Display second menu item; Takes input regarding which note property to update
        Updates corresponding property of selected note object
        :return: None
        """
        # Call function to perform necessary duties, getting note ID input being one of them
        idInput = UserInterface.handle_read(self)

        # Variable contains error strings if not note ID value
        if idInput == 'Error 1' or idInput == 'Error 2' or idInput == 'Error 3':
            return

        # Display second menu item
        print("\nWhat do you want to update: \n(For example, enter '1' to update note title.)")
        print('\n1. Note title.')
        print('2. Note text.')
        print('3. Note completion status.')
        print('4. Exit.')

        # Similar code for checking wrong input
        wrongInputCheck = True

        while wrongInputCheck:
            userSecondInput = input('\nEnter selection: ')

            if userSecondInput not in ['1', '2', '3', '4']:
                print('\nERROR : Invalid Input!\nEnter from one of the options above (Integers ranging 1-4).')

            else:
                wrongInputCheck = False

        noteObject = UserInterface.noteObjectList[idInput]

        # Decide action according to user input
        if userSecondInput == '1':
            # Similar code for checking wrong input
            emptyTitleInput = True

            while emptyTitleInput:
                newTitleInput = input('Enter new title: ')

                # Check if input entered is empty text or text with bunch of whitespaces
                if (not newTitleInput == '') and (not newTitleInput.isspace()):
                    emptyTitleInput = False

                else:
                    print("ERROR : Note title cannot be empty.")

            noteObject.update_title(newTitleInput)

            # Update completion date to current timestamp if update was done to note already marked complete
            if noteObject.isCompleted:
                noteObject.mark_complete(datetime.datetime.now())

        elif userSecondInput == '2':
            # Similar code for checking wrong input
            emptyTextInput = True

            while emptyTextInput:
                newTextInput = input('Enter new text: ')

                if (not newTextInput == '') and (not newTextInput.isspace()):
                    emptyTextInput = False

                else:
                    print("ERROR : Note text cannot be empty.")

            noteObject.update_text(newTextInput)

            if noteObject.isCompleted:
                noteObject.mark_complete(datetime.datetime.now())

        elif userSecondInput == '3':
            noteObject.change_completion_status()

            # Change completion date to 'None', if completion status of previously completed note is changed
            if not noteObject.isCompleted:
                noteObject.mark_incomplete()

                print('\nSUCCESS : Note marked incomplete.')

            else:
                # Change completion date to current timestamp, if completion status of previously non-completed note
                # is changed
                noteObject.mark_complete(datetime.datetime.now())

                print('\nSUCCESS : Note marked complete.')

        else:
            # In user selected 'Exit' option
            print('\nGoing to the main menu...')

            return

        print('\nSUCCESS : Note ID ' + str(idInput) + ' has been updated.')

    def handle_delete(self):
        """
        Calls 'handle_read()';
        Deletes corresponding note object from 'noteObjectList'
        :return: None
        """
        idInput = UserInterface.handle_read(self)

        if idInput == 'Error 1' or idInput == 'Error 2' or idInput == 'Error 3':
            return

        # Deleting note from dictionary
        del UserInterface.noteObjectList[idInput]

        print('\nSUCCESS : Note ID ' + str(idInput) + ' has been deleted.')

    def handle_add_completion_date(self):
        """
        Calls 'handle_read()';
        Takes and validates date input
        Completion date is added if selected note is non-completed, updated otherwise
        :return: None
        """
        try:
            idInput = UserInterface.handle_read(self)

            if idInput == 'Error 1' or idInput == 'Error 2' or idInput == 'Error 3':
                return

            dateCompleted = input("\nEnter the completion date (YYYY-MM-DD) ('2018-12-31' for 31st December 2018) : ")

            # Convert date string to datetime object
            dateCompleted = datetime.datetime.strptime(dateCompleted, '%Y-%m-%d')

            noteObject = UserInterface.noteObjectList[idInput]

            # Completion date entered should be future date
            if (noteObject.dateCreated - datetime.timedelta(days=1)) < dateCompleted:
                # Change completion date to date input irrespective of completion status of note
                noteObject.mark_complete(dateCompleted)

                print('\nSUCCESS : Note has been marked complete with the specified completion date.')

            else:
                print("\nERROR : Note completion date cannot be before note creation date!")
                print('Starting Over...')

                return

        except ValueError:
            print("\nERROR : Note completion date is either not correct or not in the specified format!")
            print('Starting Over...')

            return

    def handle_find_days_to_complete(self):
        """
        Calls 'handle_read()';
        Displays number of days it took to complete selected completed note;
        Displays error if non-completed note is selected
        :return: None
        """
        idInput = UserInterface.handle_read(self)

        if idInput == 'Error 1' or idInput == 'Error 2' or idInput == 'Error 3':
            return

        noteObject = UserInterface.noteObjectList[idInput]

        # Calculate time delta only if selected note is marked complete
        if noteObject.isCompleted:
            timedelta = noteObject.dateCompleted - noteObject.dateCreated

        else:
            print("\nERROR : Note not supplied with completion date!")
            print('Starting Over...')

            return

        print('\nIt took ' + str(timedelta.days) + ' days for the note to be completed.')

    def handle_save_in_file(self):
        """
        Saves all current note objects into file (created automatically)
        Displays error if input regarding continuing or moving back is erroneous
        :return: None;
        """
        notesListIsEmpty = UserInterface.print_notes_list(self)

        if notesListIsEmpty:
            return

        try:
            savedNotesList = []

            # Get list of saved notes from file
            if (os.path.exists('Notes.txt')) and (os.path.getsize('Notes.txt') != 0):
                with open('Notes.txt', 'r') as f:
                    for line in f.readlines():
                        savedNotesList.append(int(line[13]))

            userThirdInput = 0

            # Warn user if there exists non empty notes file
            if (os.path.exists('Notes.txt')) and (os.path.getsize('Notes.txt') != 0) and len(
                    set(savedNotesList) - set(list(UserInterface.noteObjectList.keys()))) > 0:
                print("\nWARNING : There are some notes already available in the file. Consider restoring before "
                      "saving. Saving before restoring will overwrite file's contents.\nNOTE : Restoration will not "
                      "overwrite the notes already present in the program, but add notes that are not already present "
                      "in the program. In order to not lose any note data, go back to the main menu, select '8' from "
                      "main menu.")

                # Ask user choice about continuing or going back to main menu
                userThirdInput = int(input("Enter '1' to go back to the main menu & '0' if you want to proceed "
                                           "anyway: "))

            # If user wants to continue
            if userThirdInput == 0:
                # File used to save is always 'Notes.txt'
                with open('Notes.txt', 'w') as f:
                    # Write note object to file one by one
                    for noteObject in list(UserInterface.noteObjectList.values()):
                        f.write("%s\n" % noteObject.get_all_data())

                print("\nSUCCESS : All notes above have been saved to file - 'Notes.txt'")

            # If user wants to rethink about restoring by going back to main menu
            else:
                return

        except ValueError:
            print("\nERROR : Invalid Input!\nEnter either '1' or '0'.")
            print('Starting Over...')

            return

    def handle_restore_file_contents(self):
        """
        Restores contents stored in file in program;
        Displays only restored contents on terminal
        Displays error if no notes have been saved to file before
        :return: None
        """
        try:
            # In case created file created was manually emptied by user
            if os.path.getsize('Notes.txt') == 0:
                print(
                    "\nERROR : File is empty. Either file contents have been deleted or no notes have been saved to "
                    "file"
                    " previously. To save all notes to file, enter '7'.")
                print('Starting Over...')

                return

            notesDictList = []

            with open('Notes.txt', 'r') as f:
                for line in f.readlines():
                    # Using yaml to parse dictionary object from string
                    notesDictList.append(yaml.safe_load(line))

            # Further beautifying result
            notesDF = pd.DataFrame(notesDictList)

            print("\nNOTE : Restoration from file does not overwrite notes already present in the program, but add "
                  "notes that are not already present in the program (including currently deleted notes that were "
                  "saved previously).")

            for note in range(len(notesDF)):
                note_ID = int(notesDF.loc[note, "Note ID"])

                # Restore notes not existing in program already, to avoid overwriting any possible updated note
                if note_ID not in list(UserInterface.noteObjectList.keys()):
                    noteObject = Note(int(notesDF.loc[note, "Note ID"]),
                                      datetime.datetime.strptime(notesDF.loc[note, "Creation Date"],
                                                                 '%Y-%m-%d %H:%M:%S.%f'),
                                      notesDF.loc[note, "Title"],
                                      notesDF.loc[note, "Text"],
                                      True if notesDF.loc[note, "Completed"] == 'Yes' else False,
                                      None if notesDF.loc[
                                                  note, "Completion Date"] == 'None' else datetime.datetime.strptime(
                                          notesDF.loc[note, "Creation Date"], '%Y-%m-%d %H:%M:%S.%f'))

                    # Simultaneously add note object to class attribute to keep track of newly added notes
                    UserInterface.noteObjectList[int(notesDF.loc[note, "Note ID"])] = noteObject

            # In case of updates done to any note, user must save notes using menu option first,
            # before expecting to see those changes in file

            print('\nSUCCESS : All notes restored.')
            print('\nHere is the list of notes present in the file:\n')
            print(notesDF)
            print("\nTo see the list of all notes present in the session now and read any note, enter '2'.")

        except FileNotFoundError:
            print("\nERROR : No file has been created. No notes have been saved to file previously. To save all notes "
                  "to file, enter '7'.")
            print('Starting Over...')

            return

    def handle_show_stats(self):
        """
        Display notes statistics focussing note completion
        :return: None
        """
        notesTotalCount = len(UserInterface.noteObjectList)

        notesIncompleteCount = 0

        print('\nTotal number of notes created: ' + str(notesTotalCount))

        if notesTotalCount == 0:
            print('Total number notes not completed: Not applicable')

            return

        for noteObject in list(UserInterface.noteObjectList.values()):
            if not noteObject.isCompleted:
                notesIncompleteCount += 1

        print('Total number notes not completed: ' + str(notesIncompleteCount))
        # Calculating and rounding to prettify result
        print('% of notes not completed: ' + str(round(100 * (notesIncompleteCount / notesTotalCount), 2)) + '%')

    def print_notes_list(self):
        """
        Displays list of all notes if 'userChoice' isn't '5' or '6';
        Displays list of completed and non-completed notes separately
        :return: (bool) True if 'noteObjectList' is empty, False otherwise
        """
        noteObjectList = UserInterface.noteObjectList

        if not list(noteObjectList.keys()):
            print("\nERROR : No notes have been created yet! To create a note, enter '1'.\nIf notes have been "
                  "previously stored in a file, enter '8' to restore contents to program.")

            return True

        elif (self.userChoice != '5') and (self.userChoice != '6'):
            print('\nHere is the list of all notes available:\n')

            noteKeys = list(noteObjectList.keys())

            noteValues = []

            for noteObject in list(noteObjectList.values()):
                noteValues.append(noteObject.title)

            allNotesDict = dict(zip(noteKeys, noteValues))

            print(tabulate(list(map(list, allNotesDict.items())), ["ID", "Note Title"]))

            return False

        else:
            nonCompletedNotesDict = {}

            completedNotesDict = {}

            for noteObject in list(noteObjectList.values()):
                if not noteObject.isCompleted:
                    nonCompletedNotesDict[noteObject.ID] = noteObject.title

                else:
                    completedNotesDict[noteObject.ID] = noteObject.title

            print('\nHere is the list of all non-completed notes:\n')
            print(tabulate(list(map(list, nonCompletedNotesDict.items())), ["ID", "Note Title"]))

            print('\nHere is the list of all completed notes:\n')
            print(tabulate(list(map(list, completedNotesDict.items())), ["ID", "Note Title"]))

            return False

    def is_note_present(self, idInput):
        """
        Checks if concerned note is present in 'noteObjectList'
        :param idInput: (int) Note ID entered by user
        :return: (bool) True if note is present, False otherwise
        """
        if idInput in list(UserInterface.noteObjectList.keys()):
            return True

        else:
            print("\nERROR : Note not found!\nAbove is the list of notes available.")
            print('Starting Over...')

            return False

# This is end of script.
