import time, random, sys, os

import tkinter as tk
from tkinter import ttk

from modules.symmies_widgets import *
from modules.launch_sub import MySubLauncher
from modules.data import StandartCommands

class Simplement(tk.Tk):

    def __init__(self, master=None, game_exe:str="WALL-E.exe", game_hooking:bool=False, work_dir:str="",atk_path:str="", game_path:str=""):
        #create window
        super().__init__(master)

        self.title("Symmies ATK UI")
        self.geometry("270x400")
        #self.attributes('-toolwindow', True)
        
        self.resizable(width=False, height=False)
        self.createWidgets()

        self.bind("<Key>", self.key_handler)
        self.SearchBarLen = 0

        self.bind("<Return>", self.send_command)

        #Launch Subprocess
        self.process = MySubLauncher(game_exe=game_exe, game_hooking=game_hooking, work_dir=work_dir, atk_path=atk_path , game_path=game_path )
        
        self.mainloop()

    def key_handler(self, *args, **kwargs):
        MySearchTerm = self.MySearchText.get()

        #Check if characters changed due to length
        if len(MySearchTerm) == self.SearchBarLen:
            return
        #Set SearchBarLen to current size for next check
        self.SearchBarLen = len(MySearchTerm)

        if MySearchTerm != "":
            #If search isn't empty, do a fuzzy search, replace and go to top of list
            Result = FuzzySearchTier(StandartCommands, MySearchTerm, join = True)
            self.CommandList.set_list(Result)
            self.CommandList.go_top()
        else:
            #Otherwise if search empty, restore the Standart List
            self.CommandList.set_list(StandartCommands)

    def send_command(self,*args,**kwargs):

        command = self.CommandList.get_item(return_item=True)
        variable = self.MyValueText.get()

        #Convert if varible is None
        #print(variable.lower())
        

        if command != "":
            #print(command+" "+variable)
            command = MakeCommand(command+" "+variable)
            self.process.write_stdin(command)

    def send_atk_command(self):
        #Send raw text as command
        command = self.MyATKEntryText.get()
        if command != "":
            self.process.write_stdin(command)
    
    def createWidgets(self):
        #Create Interactive
        self.Label1 = tk.LabelFrame(self,text="Command List")
        self.Label1.pack(padx=30, pady=5, fill="both")
        self.CommandList = InteractiveLog(self.Label1, ReadoutButton=False)
        self.CommandList.set_list(StandartCommands)
        self.CommandList.pack()
        
        self.Label2 = tk.LabelFrame(self,text="Search")
        self.Label2.pack(padx=30, pady=5, fill="both")
        self.MySearch = tk.Entry(self.Label2)
        self.MySearchText = tk.StringVar()
        self.MySearch["textvariable"] = self.MySearchText
        self.MySearch.pack(pady=2)

        self.Label3 = tk.LabelFrame(self,text="Variable & Enter")
        self.Label3.pack(padx=30, pady=5, fill="both")
        self.MyValue = tk.Entry(self.Label3)
        self.MyValueText = tk.StringVar()
        self.MyValue["textvariable"] = self.MyValueText
        self.MyValue.pack(pady=2)
        self.EnterButton = tk.Button(self.Label3,text="Run Command", command=self.send_command)
        self.EnterButton.pack(pady=2)

        #Aditional button for ATK commands
        self.Label4 = tk.LabelFrame(self,text="Run ATK Command")
        self.Label4.pack(padx=30, pady=5, fill="both")
        self.MyATKEntry = tk.Entry(self.Label4)
        self.MyATKEntryText = tk.StringVar()
        self.MyATKEntry["textvariable"] = self.MyATKEntryText
        self.MyATKEntry.pack(pady=1)

        self.MyATKEnter = tk.Button(self.Label4,text="Run Command", command=self.send_atk_command)
        self.MyATKEnter.pack(pady=2)

def main():
    work_dir = ""
    game_hooking = False
    game_exe = ""
    atk_path = ""
    game_path = ""

    
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]

    for n in range(len(sys.argv)):
        
        #Directory to work from
        if sys.argv[n] == "-chdir":
            work_dir = sys.argv[n+1]

        #Enable hooking mode
        if sys.argv[n] == "-hook":
            game_hooking = True

        if sys.argv[n] == "-up":
            work_dir = os.path.dirname(os.getcwd())

        if sys.argv[n] == "-game":
            game_exe = sys.argv[n+1]

        if sys.argv[n] == "-atkpath":
            atk_path = sys.argv[n+1]

        if sys.argv[n] == "-gamepath":
            game_path = sys.argv[n+1]
            
    try:
        Simplement(work_dir=work_dir, game_hooking=game_hooking, game_exe=game_exe, atk_path=atk_path , game_path=game_path)
    except Exception as e:
        print(e)
        input()

if __name__ == "__main__":
    main()
    

