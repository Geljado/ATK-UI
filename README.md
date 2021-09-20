# Symmies-ATK-UI
An simple ui extension for the Asobo-Tool-Kit by widberg

## Requirements
- [Python3](https://www.python.org/)
- [Asobo Tool Kit](https://github.com/widberg/atk)

## IMPORTANT:
If want to close the programm, close the game first, then the "Symmies ATK UI" then the console.
If you don't, dead processes will stack up, that you need to clear of manually in the task manager.

## Starting
To start, doubleclick the start.bat
It's recommended to have the Game-folder and the Asobo-Toolk-Kit-Folder and This UI-Program-Folder in the same directory.
Default Launch Command:
> python layout_symmies_ui.py -up

## Options
-game *game.exe (change to what your game.exe is called.)

-hook (Hooks in to running game; if left out, start's the game up.)

-up (Goes with the working directory one up; Default)

-chdir *path (Change Working Directory, so that the programm can find the executables)
