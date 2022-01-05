text_errors=["error","Error","Failed","failed"]

purple_text=["     ____",
"    / _  |   Frida 15.0.13 - A world-class dynamic instrumentation toolkit",
"   | (_| |",
"    > _  |   Commands:",
"   /_/ |_|       help      -> Displays the help system",
#"   . . . .       object?   -> Display information about 'object'",
#"   . . . .       exit/quit -> Exit",
#"   . . . .",
#"   . . . .   More info at https://frida.re/docs/home/"
]

text_1 =\
"""
Graphical User Interface (ATK-UI) provided by Geljado
In collaboration with Widberg and their software Asobo Tool Kit


For help consult README.md
Further In-App Guides may come with version 2.1 & 2.2
"""

text_2 =\
"""How to Delete / Reset all Data:

To delete all profiles , find the delete the "gameprofiles.json" file.
To reset all app settings, find "appconfig.json", delete it and then restart the program.

Files could also show up as "gameprofiles" and "appconfig" if you have no file extensions enabled.
"""

text_3=\
"""Installation guide:

Important: The programm was programmed on python version 3.9.7- Higher versions of python might not work due to dependencies!
If you get an "Unexpected Python Version" error, it may be why ATK is not launching.

Now we need to install Frida
for that you type in to the console:
pip3 install frida-tools

Now you can copy the UI-progam to a desired folder.
Make sure that you copy atk (folder), modules (folder), main.py and start.bat .
In order to start the program you can double click the start.bat file.
(Windows will likely give a warning)

Please report further errors on the github:
https://github.com/Geljado/ATK-UI/issues
"""
text_4 =\
"""Coming in version 2.1 & 2.2
"""
text_5 =\
"""Coming in version 2.1 & 2.2
In the meantime check out appconfig.json for rudimentary options.
"""
text_6 =\
"""Welcome to the ATK-UI
Under the Data tab, you can create a Profile.
Then you can try to Auto-Get the commands from the game.
You can also launch the game hook from there.
(Important notice, version 2.0 only has hooking so far)

Use the searchbar for finding commands easier.
In the Variable entry, you can enter a variable that goes along with executed command.

To execute, simple press return after you selected a command from the list, or pre the "Game Execute" button.

If you want to communicate with the ATK directly, you can use the ATK /- Console Entry and button.
(Enter does not work for that field)
"""
