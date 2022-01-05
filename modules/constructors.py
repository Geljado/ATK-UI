#Standart Libary Imports
import tkinter as tk
from tkinter import ttk

#Modules Import
try:
    #from main
    from modules.widgets import ListBoxBeta
    #This can cause issues v
    from data.text import text_errors, purple_text
except:
    #local
    print("FATAL ERROR")
    from widgets import ListBoxBeta

class ControlPanel(tk.Frame):
    "Constructor of the main interface"
    def __init__(self, master):

        super().__init__(master)

        self.FrameLeft = tk.Frame(self)
        self.FrameLeft.pack(expand=True, fill="both", side=tk.LEFT)
        
        self.FrameRight = tk.Frame(self)
        self.FrameRight.pack(expand=True, fill="both", side=tk.RIGHT)



        self.command_list_label = tk.LabelFrame(self.FrameLeft,text="Command List")
        self.command_list_label.pack(padx=5, pady=5, fill="both")
        
        self.command_list = ListBoxBeta(self.command_list_label)
        self.command_list.pack(padx=2,pady=2)



        self.search_label = tk.LabelFrame(self.FrameLeft,text="Search")
        self.search_label.pack(padx=5, pady=5, fill="both")
        
        self.search_entry = tk.Entry(self.search_label)
        self.search_entry_text = tk.StringVar()
        self.search_entry["textvariable"] = self.search_entry_text
        self.search_entry.pack(pady=3,padx=6, expand=True,fill="x")



        self.variable_label = tk.LabelFrame(self.FrameLeft,text="Variable /- Execute")
        self.variable_label.pack(padx=5, pady=5, fill="both")
        
        self.variable_entry = tk.Entry(self.variable_label)
        self.variable_entry_text = tk.StringVar()
        self.variable_entry["textvariable"] = self.variable_entry_text
        self.variable_entry.pack(pady=3,padx=6, expand=True,fill="x")
        
        self.execute_button = tk.Button(self.variable_label,text="Game Execute")
        self.execute_button.pack(pady=2)



        self.atk_label = tk.LabelFrame(self.FrameLeft,text="ATK /- Console ")
        self.atk_label.pack(padx=5, pady=5, fill="both")

        self.atk_entry = tk.Entry(self.atk_label)
        self.atk_entry_text = tk.StringVar()
        self.atk_entry["textvariable"] = self.atk_entry_text
        self.atk_entry.pack(pady=3,padx=6, expand=True,fill="x")
        
        self.atk_execute_button = tk.Button(self.atk_label,text="Console Execute")
        self.atk_execute_button.pack(pady=2)



        self.log_text = tk.Text(self.FrameRight,width=75,height=22,bg="#191d1f",fg="#eeeeee",font=("consolas", 12))
        self.log_text.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.log_text["state"]=tk.DISABLED
        #ScrollBar
        self.log_text_scroll = tk.Scrollbar(self.FrameRight, orient=tk.VERTICAL)
        self.log_text_scroll.grid(row=0, column=1, sticky=tk.N+tk.S)
        #Scrolling function
        self.log_text["yscrollcommand"] = self.log_text_scroll.set
        self.log_text_scroll['command'] = self.log_text.yview

        self.log_text.tag_config('info', foreground="#00aaff")
        self.log_text.tag_config('atk', foreground="#dfdf20")
        self.log_text.tag_config('err', foreground="#df2020")
        self.log_text.tag_config('f_purple', foreground="#d52bd5")
        l1 = ["#2b2fd5","#6e2ecf","#972dc8","#ac2cc3"]
        [self.log_text.tag_config("f_purple_{}".format(i), foreground=l1[i]) for i in range(4) ]
        self.col_gradient_static =tuple(["f_purple_{}".format(i) for i in range(4)] )
        
    def log(self, msg:str, flag:str=None):
        #Writes to the log. Takes flags such as "info" and "err"
        if msg[-1:] != "\n":
            msg += "\n"
        checker = lambda keyword, string: keyword in string
        
        if any([checker(keyword, msg) for keyword in text_errors]) and flag == None: 
            flag = "err"

        
            
        self.log_text["state"] = tk.NORMAL
        if flag == "info":
            self.log_text.insert(tk.END, "[")
            self.log_text.insert(tk.END, "Info", flag)
            self.log_text.insert(tk.END, "]  ")
        if flag == "err":
            self.log_text.insert(tk.END, "[")
            self.log_text.insert(tk.END, "Error", flag)
            self.log_text.insert(tk.END, "] ")
        if flag == "atk":
            self.log_text.insert(tk.END, "[")
            self.log_text.insert(tk.END, "ATK", flag)
            self.log_text.insert(tk.END, "]   ")
        self.log_text.insert(tk.END, msg, flag)
        #self.log_text.insert(tk.END, "\n")

        #playing around
        if any([checker(keyword, msg) for keyword in purple_text]) and flag == None:
            current_line = int(float(self.log_text.index(tk.END)))
            a, b = current_line-2.0, current_line-2+.12
            self.log_text.tag_add("f_purple", a, b)
            #self.atk_gradient_list = list(self.atk_gradient_list_static)
            self.col_gradient = list(self.col_gradient_static)

        if "   . . . ." in msg:
            pop = self.col_gradient.pop()
            current_line = int(float(self.log_text.index(tk.END)))
            a, b = current_line-2.0, current_line-2+.12
            self.log_text.tag_add(pop, a, b)
       
            
            """
            This system of definition is so fucking retarted, I need to document it here real quick.

            The floats stand for line:character
            When you want to colourize only a character section of one line, let's say 10 characters from 0-10,
            then you need to create variable a with which is CurrentLine-2 (the .0 must be the beginning of the next line or smth)
            Then B is a lot more tricky:
            First you say that B is also Current_line-2 and the + the offset of characters in rest-float.
            Tho carefull, fool, out ten characters can not be expressed with n.10 cause it's float.
            Which means 0.1 == 0.10 == 0.100; So in order to define the 10th char, you need to write  0.11.

            ...
            Why don't they just use a tuple with two values or smth?
            I mean, the fucking tag_add function even accepts strings..
            So FUCK YOU! FUCK YOU FOR STEALING AN HOUR OF MY GOD DAMN LIFE
            """
        self.log_text["state"] = tk.DISABLED
        self.log_text.see(tk.END)

        

    def setList(self,command_list:list=None):
        self.command_list.setList(command_list or [])

    def getItem(self):
        return self.command_list.setList.getItem()

    def set_commands(self,command_list):
        self.EnterButton["command"] = command_list[0]
        self.MyATKEnter["command"] = command_list[1]
        self.MyATKRelauncher["command"] = command_list[2]

    def top(self):
        self.command_list.top()
    def bottom(self):
        self.command_list.bottom()
if __name__ == "__main__":
    pass
    """quit()
    c = ControlPanel(None)
    c.log("gekjgnijrweoifiw")
    c.log("nhzö654lslöfdmkö","info")
    c.log("gblödfm.-q1bsada","err")
    c.log("hlgfdgfdhztzo-.p","atk")
    c.pack()"""
    
