#Standart Libary Imports
import sys, os, random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, simpledialog, messagebox

#Modules Import
from modules.storage import Storage
from modules.constructors import ControlPanel
from modules.functions import *
from modules.drone import Drone, GetGameCommands
from modules.widgets import ListBoxBeta
#text import
from data.text import *
#Constants & Lambdas

screen_positioning_function = lambda screen_length, app_length, percent: int(((screen_length/100)*percent)-((app_length/100)*percent))

#Version and edit date
version = 2.0
last_edit = [5,1,2022]

class MainWindow(tk.Tk):
    
    def quitter(self,*args):
        #Ask if user want to quit, if not in dev mode;
        if not self.DevMode:
            answer = ans2bool( messagebox.askquestion("Closing Program","Do you want to quit?") )
            #If user does not agree, return back
            if not answer:
                return
        #Kill processes:
            self._kill_atk_process()
        #quit main window:
        self.destroy()
        self.quit()

    def versionChecker(self):
        "Checking for right version of python"
        Version = [int(i) for i in sys.version.split(" ")[0].split(".")]
        if Version[0] > 3 or Version[1] > 9 or Version[2] > 7:
            self.log("Unexpected Python Version !\nThis version of python is higher than expected,\nFrida and other functions might not work!\nDevelopment version was Python 3.9.7.\n", "info")

    def log(self, *args):
        "Write something in to the self.global_log variable; automated detection for flags"
        #Cast to string, so that it causes no error for development;
        
        if len(args) >= 2:
            self.global_log.append((str(args[0]),args[1]))
        #Comes second, so colours work
        elif len(args) >= 1:
            self.global_log.append(str(args[0]))
        

    def _after_run(self):
        "Frequently checks if something was written in to self.global_log"
        if len(self.global_log) > 0:#pop(0) => 0 for reverse
            message = self.global_log.pop(0)
            if self.DevMode:
                pass
                #print(message)
            if isinstance(message, str):
                self.frame1.log(message)
            else:
                self.frame1.log(message[0],message[1])

        self.after(10, self._after_run)
            
    def __init__(self, master=None):
        #Global log list
        self.global_log = []

        #Version Checker since Firda does not work on 3.10 yet; as of 22.10.2021
        self.versionChecker()

        #init tk.Tk
        super().__init__(master)
        
        #Permenant Data
        self.atk_path =  os.sep.join((os.getcwd(),'atk','atk.js')) #This path changes, so DONT store it in AppConfig

        #Game Storage
        self.Profiles = Storage("gameprofiles.json",log=self.log)
        #App Config Storage
        self.AppConfig = Storage("appconfig.json",log=self.log)

        #AppConfig Settings:
        self.DevMode = self.AppConfig != "DevMode"
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        app_width = self.AppConfig != ("Width",920)
        app_height = self.AppConfig != ("Height",480)
        x_pos = screen_positioning_function(screen_width, app_width, 5)
        y_pos = screen_positioning_function(screen_height, app_height, 50)
        self.app_width = app_width
        self.app_height = app_height
        #Temporary Values
        title = self.AppConfig != ("Title","ATK-UI 2.0")
        geometry = "{}x{}+{}+{}".format(app_width,app_height,x_pos,y_pos)
        resizable = self.AppConfig != "resizable"
        
        
        
        #Images
        self.hallicon_ico_path = os.sep.join((os.getcwd(),'data','hallicon.ico'))
        self.hallicon_png_path = os.sep.join((os.getcwd(),'data','hallicon.gif'))

        self.hallicon_icon  = tk.PhotoImage(self.hallicon_ico_path)
        self.hallicon_image = tk.PhotoImage(file=self.hallicon_png_path)
        
        
        self.iconbitmap(self.hallicon_icon)
        
        #Set title and window size.
        self.title(title)
        self.geometry(geometry)
        self.resizable(width=resizable, height=resizable)

        #Overwrite Quiting Function
        self.protocol("WM_DELETE_WINDOW", self.quitter)

        #Creat widgets
        self.createWidgets()
        self.modWidgets()

        self.refresh_command_list()
        #Save Configs
        self.AppConfig.save()

        #Run mainloop and after functions if there are any.
        #self.mainloop()
        self.after(10, self._after_run)
    
    def createWidgets(self):
        
        """Begining of Menu definiton"""
        #Create Root Menu
        self.root_menu = tk.Menu(self)

        #Create Data Menu
        self.menu_data = tk.Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label="Data",menu=self.menu_data)
        
        self.menu_data.add_command(label="Add Profile", command=self.addProfile)
        self.menu_data.add_command(label="Delete Profile", command = self.remove_profile)
        
        
        ### !!! DEBUG ONLY !!! ###
        self.menu_data.add_separator()
        self.menu_data.add_command(label="Add Command", command = self.addCommand)
        self.menu_data.add_command(label="Remove Command", command = self.remove_command)
        self.menu_data.add_command(label="Reset Commands", command = self.reset_commands)
        
        self.menu_data.add_command(label="Auto-get Commands", command = self.auto_get_cmd)
        
        self.menu_data.add_command(label="Launch ATK (Hook)", command = self.launchATK)

        ### !!! DEBUG ONLY !!! ###
        
        if self.DevMode:
            self.menu_data.add_separator()
            self.menu_data.add_command(label="Import Profile", state=tk.DISABLED)
            self.menu_data.add_command(label="Export Profile", state=tk.DISABLED)

        
        if self.DevMode:
            self.menu_data.add_separator()
            self.menu_data.add_command(label="Reset Profile Data", state=tk.DISABLED)
            self.menu_data.add_command(label="Reset Config Data", state=tk.DISABLED)
        self.menu_data.add_separator()
        def reset_all_data_info():
            self.log(text_2)
        self.menu_data.add_command(label="Erase All Data",command=reset_all_data_info)
        self.menu_data.add_command(label="Help", command=self.help)
        #Create Profile Menue
        self.menu_profiles = tk.Menu(self.root_menu, tearoff=0)
        self.root_menu.add_cascade(label="Profiles",menu=self.menu_profiles)
        #This one is important for the readout.
        self.profile_selection_value = tk.StringVar()
        

        #Developer only Menu
        if self.DevMode:
            self.menu_developer = tk.Menu(self.root_menu, tearoff=0)
            self.root_menu.add_cascade(label="Developer Menu",menu=self.menu_developer)
            
            self.menu_developer.add_command(label="Show Data", command=self.show_data)
        
        self.config(menu=self.root_menu)
        #Done with menu


        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        
        self.frame1 = ControlPanel(self.notebook)
        self.frame1.pack(fill="both", expand=True)
        
        self.frame2 = tk.Frame(self.notebook)
        self.frame2.pack(fill="both", expand=True)
        
        self.frame3 = tk.Frame(self.notebook)
        self.frame3.pack(fill="both", expand=True)

        self.frame4 = tk.Frame(self.notebook)
        self.frame4.pack(fill="both", expand=True)

        #The main way of Controlling
        self.notebook.add(self.frame1, text="Control Panel")
        #A button panel for options. Maybe rename it to Extras
        #Options range from import/exporting to auto getting values and commands;
        self.notebook.add(self.frame2, text="Settings")
        tk.Label(self.frame2,text=text_5).pack(expand=True,fill="both")
        
        #The data manager, to change values in app;
        self.notebook.add(self.frame3, text="Data Manager")
        tk.Label(self.frame3,text=text_4).pack(expand=True,fill="both")
        
        self.notebook.add(self.frame4, text="About")
        self.hallicon_image_label = tk.Label(self.frame4, image=self.hallicon_image)
        self.hallicon_image_label.pack(expand=True, fill="both", side=tk.LEFT)
        
        self.hallicon_descriptive_label = tk.Label(self.frame4,text=text_1,justify=tk.LEFT)
        self.hallicon_descriptive_label.pack(expand=True, fill="both", side=tk.RIGHT)

    def modWidgets(self):
        #This is for adding functionallity to the widgets
        #Refresh Profile List, Set to first element
        self.refresh_profiles()
        self.select_first_profile()
        #bind search & create varialbes
        self.bind("<Key>", self.command_search)
        self.search_entry = self.frame1.search_entry
        self.search_term_len = 0
        
        #bind return for command entry
        self.bind("<Return>", self.enter_command)
        self.frame1.execute_button["command"] = self.enter_command

        self.frame1.atk_execute_button["command"] = self.atk_enter_command
        
        #connect frame1 functions:
    def enter_command(self,*args):
        #Create and send commands to ATK
        try:
            command = self.frame1.command_list.getItem()
            variable = self.frame1.variable_entry_text.get()
            command = "runCommand(\"{}\");\n".format(command+" "+variable)
            self.subprocess.write_stdin(command)
        except:
            pass

    def atk_enter_command(self,*args):
        #Send commands directly to ATK
        try:
            command = self.frame1.atk_entry_text.get()
            self.subprocess.write_stdin(command)
        except:
            pass

        #self.process.sendto
        
    def command_search(self, *args):
        #Check if characters changed due to length
        search_term = self.frame1.search_entry.get()
        if len(search_term) == self.search_term_len:
            return
        
        current_profile_data, current_profile_name = self.getProfile()

        #Set SearchBarLen to current size for next check
        self.search_term_len = len(search_term)

        if search_term != "":
            #If search isn't empty, do a fuzzy search, replace and go to top of list
            Result = FuzzySearchTier(list(current_profile_data["cmd"]), search_term, join = True)
            
            self.frame1.setList(Result)
            self.frame1.top()
        else:
            #Otherwise if search empty, restore the Standart List
            self.frame1.setList(current_profile_data["cmd"])
        
        
    def select_first_profile(self):
        try:
            self.profile_selection_value.set( list(self.Profiles.data.keys())[0] )
        except:
            self.log(text_6)

    def addProfile(self):
        #Let user select exe
        path = filedialog.askopenfilename(filetypes =[("Game File", "*.exe")],initialdir=os.getcwd())
        #if user didn't select anything, quit back to normal menu
        if path == "":
            return
        #Fix the seperators
        path = os.sep.join(path.split("/"))
        #Get users desired profile name:
        profile_name = simpledialog.askstring("Name Profile", "Add a Profile Name:")
        #check if name is empty
        if profile_name == "" or profile_name == None:
            #error if empty or exsits
            messagebox.showerror("Profile Error",message="Name must not be empty")
        #check if name already exsits in storage
        elif self.Profiles == profile_name:
            messagebox.showerror("Profile Error",message="Profile {} already Exsits!".format(profile_name))
        else:
            #Add to Profile | Version of the Programm | Path of game | CMD dict | launch options (Only Str), (Only List)
            self.Profiles += profile_name,{"version":version,"path":path, "cmd":{}, "launch_opt":["-n",["--no-pause","--","-w"]]}
            #always use self.refresh_profiles to add new ones; It makes sure they work correctly
            self.refresh_profiles()
            self.profile_selection_value.set(profile_name.lower())
            self.refresh_command_list()
            self.Profiles.save()
            self.log("Created Profile: \"{}\" ".format(profile_name.lower()),"info")

    def refresh_profiles(self):
        #Clear list
        self.menu_profiles.delete(0,tk.END)
        #Adds profiles as radio buttons
        for profile_name, empty1 in self.Profiles:
            self.menu_profiles.add_radiobutton(label=profile_name, value=profile_name, variable=self.profile_selection_value, command=self.refresh_command_list)

    def remove_profile(self):
        #Remove Selected Profile
        selected_profile = self.profile_selection_value.get()
        #If nothing's selected, do nothing
        if selected_profile == "":
            return
        answer = ans2bool( messagebox.askquestion("Delete Profile","Do you want to delete \"{}\"?\nThis can't be undone!".format(selected_profile)) )
        if not answer:
            return
        #Delete profile with math!!! and.. maybe do not forget to save. Idiot!
        self.Profiles - selected_profile
        self.refresh_profiles()
        self.select_first_profile()
        self.Profiles.save()
        self.log("Deleted Profile: \"{}\"".format(selected_profile),"info")
        
    def getProfile(self):
        #Function for convinience, returns profile from storage and gets name
        selected_profile = self.profile_selection_value.get()
        return self.Profiles * selected_profile, selected_profile

    def refresh_command_list(self):
        try:
            current_profile_data, current_profile_name = self.getProfile()
            self.frame1.setList(current_profile_data["cmd"])
        except:
            pass

    #Game Launching & Command Getters
    def _kill_atk_process(self):
        try:
            self.subprocess.kill()
        except Exception as e:
            self.log(e,"info")
            self.log("You may ignore this error","info")
            
    def launchATK(self):
        self._kill_atk_process()
        selected_profile = self.profile_selection_value.get()
        path = (self.Profiles * selected_profile)["path"]
        self.subprocess = Drone(path, log=self.log)
        self.subprocess._launch()



    def addCommand(self,*args):
        #Get Current Profile and Name
        current_profile_data, current_profile_name = self.getProfile()
        
        def add_to_cmd(*args):
        #Get list of commands, sperate by "," and " "
            commands = textarea_for_commands.get("1.0",tk.END)
            textarea_for_commands.delete("1.0",tk.END)
            commands = " ".join(commands.split(","))
            commands = " ".join(commands.split("\n"))
            commands = " ".join(commands.split(" "))
            for i in commands.split(" "):
                if i != "":
                    textarea_for_commands.insert(tk.END,i+", ")
            commands = [cmd for cmd in commands.split(" ") if cmd != ""]
        #Only if it does not exsist; add it;
            for cmd in commands:
                if not cmd in current_profile_data["cmd"]:
                    current_profile_data["cmd"][cmd] = None
            self.refresh_command_list()
            self.Profiles.save()
        #Create seperate Window for widgets
        window = tk.Toplevel(self)
        x_pos = self.winfo_x() + self.app_width + 4
        window.geometry("280x{}+{}+{}".format(self.app_height, x_pos, self.winfo_y()))
        window.title("Add Commands")
        #Create textarea_for_commands and other widgets
        info_label = tk.Label(window,text="Commands must be seperated with , or <space> ").pack()
        textarea_for_commands = tk.Text(window)
        textarea_for_commands.pack()
        textarea_for_commands.bind("<Return>", add_to_cmd)
        add_command_button = tk.Button(window, text="Add commands", command=add_to_cmd)
        add_command_button.pack()
        #Mainloop so window is displayed properly
        window.mainloop()
        
    def remove_command(self):
        #Get Current Profile and Name
        current_profile_data, current_profile_name = self.getProfile()
        def del_cmd(*args):
            #Get selection, if empty return
            cmd = list_box_commands.getItem()
            if not cmd:
                return
            #Ask, and delete, then save.
            answer = ans2bool( messagebox.askquestion("Delete Command","Do you want to delete \"{}\"?".format(cmd)) )
            if answer:
                del current_profile_data["cmd"][cmd]
                self.Profiles.save()
                update_list()
                self.refresh_command_list()
                
        def update_list():
            #Refresh / Populate list
            list_box_commands.setList([cmd for cmd in current_profile_data["cmd"]])

        def quitter():
            self.refresh_command_list()
            window.destroy()
            window.quit()
                
        #Create Window and InteractiveLog
        window = tk.Toplevel(self)
        #Geometry & titel
        x_pos = self.winfo_x() + self.app_width + 4
        window.geometry("280x{}+{}+{}".format(self.app_height, x_pos, self.winfo_y()))
        window.title("Remove Commands")
        window.protocol("WM_DELETE_WINDOW", quitter)
        #Widgets
        label_profile_name = tk.Label(window, text="Selected Profile: {}".format(current_profile_name), font=("consolas", 11), fg="red", bg="black").pack(fill="x")
        list_box_commands = ListBoxBeta(window)
        window.bind("<Return>", del_cmd)
        window.bind("<Delete>", del_cmd)
        list_box_commands.pack(expand=True, fill="both")
        button_delete = tk.Button(window, text="Delete Command", command=del_cmd).pack()
        #Update list & Mainloop
        update_list()
        window.mainloop()

    def reset_commands(self):
        current_profile_data, current_profile_name = self.getProfile()
        answer = ans2bool( messagebox.askquestion("Delete All Commands","Do you want to delete all commands on this profile?\nThis can super duper not be undone!!") )
        if answer:
            current_profile_data["cmd"] = {}
            self.Profiles.save()
            self.refresh_command_list()

    def auto_get_cmd(self):
        
        #Get Current Profile and Name
        current_profile_data, current_profile_name = self.getProfile()

        #Ask user for consent... again.
        answer = ans2bool( messagebox.askquestion("Auto-Get Commands","Do you want update the commands of \"{}\"?\nCommands and their variables will be overwritten!\n\nFurther more the program might freeze and need a restart if games don't launch correctly afterwards.".format(current_profile_name)) )

        #If user does not agree, return
        if not answer:
            return
        current_profile_data["cmd"] = {}
        self.log("Gathering Commands...","info")
        #Get Atk path, and GamePath
        atk_path = self.atk_path
        game_path = current_profile_data["path"]
        #Create Log list
        Mylog = []
        #Init GetGameCommands / Logger class; Then get the log;
        MyLogger = GetGameCommands(game_path,atk_path,log=self.log)
        Mylog = MyLogger._command_readout()
        #Primitive Command Adder (VERY MESSY)
        #MyCommands will be the string with the commands;
        MyCommands = ""
        counted_commands = 0
        for log_item in Mylog:
            if "," in log_item:
                MyCommands = log_item
        #Scroll through split list
        for command in MyCommands.split(","):
            #If not empty and not \n write to cmd storage
            if command != "" and not "\n" in command:
                current_profile_data["cmd"][command] = None
                counted_commands += 1
            #Treat every \n command diffrently
            elif command != "" and "\n" in command:
                command = command[:-1]
                current_profile_data["cmd"][command] = None
                counted_commands += 1
        self.log("Gathered {} Commands!".format(counted_commands),"info")
        self.refresh_command_list()
        self.Profiles.save()
            
    #Debbugin only

    def help(self):
        window = tk.Toplevel(self)
        window.title("help")
        window.iconbitmap(self.hallicon_icon)
        l1 = tk.Text(window,font=("consolas", 12), bg="#333333",fg="#eeeeee")
        l1.insert(tk.END,text_3)
        l1["state"]=tk.DISABLED
        l1.pack()
        window.mainloop()

    
        
    


    

    
    
    

        

if __name__ == "__main__":
    MyMainWindow = MainWindow()
    MyMainWindow.mainloop()
    

