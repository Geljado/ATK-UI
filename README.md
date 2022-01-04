# ATK-UI
An simple ui extension for the Asobo-Tool-Kit by widberg

## Requirements
- [Python3](https://www.python.org/)
- [Asobo Tool Kit](https://github.com/widberg/atk)

## IMPORTANT:
If want to close the programm, close the game first, then the "Symmies ATK UI" then the console.
If you don't, dead processes will stack up, that you need to clear of manually in the task manager.



To start click the start.bat
It's recommended to have Game-, AsoboToolKit-, and UI-Program-Folder next to each other:
## ![](https://user-images.githubusercontent.com/35775147/134157302-3921754f-880c-47cf-bc12-665d755f591c.png)

Default Launch Command:
> python layout_symmies_ui.py -up

## Usage

You can search commands in the list with the search entry.

If you select a command you can either press enter or press the "Run Command" button in order to send it to the ATK for execution.
Every command send to the ATK this way will be written inside a runCommand(...) parameter;

In order to send commands directly to the ATK, use the "Run ATK Command" Entry and button.

## Options
-game *game.exe (Default is Wall-E.exe, you want to change it to what ever game you trying to launch)

-hook (Hooks in to running game; if left out, start's a new game up.)

-up (Goes with the working directory one up; Don't use this option if you use -chdir)

-chdir *path (Change Working Directory, so that the programm can find the executables)

-atkpath (Set a path to the atk directly, don't use any " include the the *atk.js at the end)

-gamepath (Set a path to the game directly, don't use any "; include the the *game.exe at the end)
