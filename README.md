# ATK-UI [Abandoned, Outdated, Broken & Poor code-quality]
An UI extension for the Asobo-Tool-Kit by Widberg

## Requirements
- [Python 3.9.7](https://www.python.org/)
- [Frida](https://github.com/frida/frida)
- [Asobo Tool Kit](https://github.com/widberg/atk)
  (ATK Included)

# Installation:

Let's start by checking out that you have the right version of python installed:

Open the windows commandline.
You can do this by pressing "WindowsKey + R" then type "cmd" in the text-entry and hit enter.

Then type in "python" and hit enter
If it gives you an error that says that python doesn't exsist, you need to go to [python.org](https://www.python.org/) in order to download and install python 3.9.7.
Important: The programm was programmed on python version 3.9.7- Higher versions of python might not work due to dependencies!

Now we need to install Frida.
For that you type in to the console:
pip3 install frida-tools

Now you can copy the UI-progam to a desired folder.
Make sure that you copy atk (folder), modules (folder), data (folder), main.py and start.bat .
In order to start the program you can double click the start.bat file.
(Windows will likely give a warning)

There we go.

# Usage:
Welcome to the ATK-UI
Under the Data tab, you can create a Profile.
Then you can try to Auto-Get the commands from the game.
You can also launch the game hook from there.
(Important notice, version 2.0 only has hooking so far)

Use the searchbar for finding commands easier.
In the Variable entry, you can enter a variable that goes along with executed command.

To execute, simple press return after you selected a command from the list, or pre the "Game Execute" button.

If you want to communicate with the ATK directly, you can use the ATK /- Console Entry and button.
(Enter does not work for that field)
