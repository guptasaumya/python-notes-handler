# -*- coding: utf-8 -*-
# Python Project
# Python Notes Handler
# Saumya Gupta, DS


class Note:
    """
    Represents a single note

    Attributes
    ----------
    ID : (int) Unique identification number of note
    dateCreated : (datetime) Creation date of note
    title : (str) Title of note
    text : (str) Text/body of note
    isCompleted : (bool) True if note is completed, otherwise False
    dateCompleted : (datetime) Completion date of note

    Methods
    -------
    update_title(new_title) : Updates title of note
    update_text(new_text) : Updates text/body of note
    change_completion_status() : Toggles completion status of note
    mark_complete(dateCompleted) : Marks note complete
    mark_incomplete() : Marks note incomplete
    get_all_data() : Returns dictionary of notes data
    """
    def __init__(self, ID, dateCreated, title, text, isCompleted, dateCompleted=None):
        """
        Initializes note attributes
        :param ID: (int) ID for note generated automatically using incremental counter
        :param dateCreated: (datetime) Current timestamp
        :param title: (str) Title input by user
        :param text: (str) Text/body input by user
        :param isCompleted: (bool) True if note marked completed by user, otherwise False
        """
        self.ID = ID
        self.dateCreated = dateCreated
        self.title = title
        self.text = text
        self.isCompleted = isCompleted
        self.dateCompleted = dateCompleted

    def update_title(self, new_title):
        """
        Updates title of note to 'new_title'
        :param new_title: New title input by user
        :return: None
        """
        self.title = new_title

    def update_text(self, new_text):
        """
        Updates text of note to 'new_text'
        :param new_text: New text input by user
        :return: None
        """
        self.text = new_text

    def change_completion_status(self):
        """
        Toggles completion status of note; True changes to False and vice versa
        :return: None
        """
        self.isCompleted = not self.isCompleted

    def mark_complete(self, dateCompleted):
        """
        Marks note complete; completion date is set to 'dateCompleted': sets 'isCompleted' to True
        :param dateCompleted: Completion date entered by user or current timestamp
        :return: None
        """
        self.dateCompleted = dateCompleted
        self.isCompleted = True

    def mark_incomplete(self):
        """
        Marks note incomplete; completion date is set to 'None': sets 'isCompleted' to False
        :return: None
        """
        self.dateCompleted = None
        self.isCompleted = False

    def get_all_data(self):
        """
        Returns dictionary of notes data
        :return: (dict) Dictionary consisting note's metadata
        """
        return {
            'Note ID': str(self.ID),
            'Title': self.title,
            'Text': self.text,
            'Completed': 'Yes' if self.isCompleted else 'No',
            'Creation Date': str(self.dateCreated),
            'Completion Date': str(self.dateCompleted) if self.dateCompleted else None
        }

# This is end of script.
