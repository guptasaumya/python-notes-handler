# Python Notes Handler

## Description

Notes Handler is a program that, on execution, helps the user keep track of his/her notes over time. It facilitates basic CRUD (create, read, update, delete) persistent storage operations on notes. Apart from these basic operations, users can also perform complex tasks such as restoring notes from the previous session, getting completion statistics on created notes, to list a few. The program is user friendly with its elaborative menu system. It tries its best to guide the user at every step of what has been done and what must be done, hence an easy-to-use tool for a new user. 

This program was created as part of the ```Python- and R-programming``` course held at Dalarna University for the master in the data science program.

## Getting Started

### Dependencies

* Python - The program is built on Python. If not already present, install it. If you are new to Python, check out ```https://www.python.org/about/gettingstarted/``` for downloading and installation help. It is built using Python 3.9.1 version. It is advisable to install or switch to the same version to avoid any disparity in program execution.
* The program is using certain packages from PyPI to ensure tabular output and pretty display. Ensure that all the packages mentioned in the ‘requirements.txt’ file are available within the environment you would like to work. If not already present, install them using pip or conda. Follow the directions given in ```https://packaging.python.org/tutorials/installing-packages/#requirements-for-installing-packages``` for installation using pip or check the next section.

### Installing

* Clone this repository or download it as a zip and extract it in a folder. Next, go to the folder containing the program files. Four files should be available: ```Main.py```, ```Notes.py```, ```userInterface.py``` and ```requirements.txt``` (for installing dependencies). 
* Once there, open the terminal and use ```pip install -r requirements.txt``` to install all packages in one go. Again, the motive is to ensure that all packages are installed in the environment where you plan to execute the program.

### Executing program

To run the program, use ```python Main.py```. Notes Handler is running now, and you should see the primary menu item, waiting for your response.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
