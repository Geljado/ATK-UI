#Tk widgets and predefined strucktures
import tkinter as tk
#import tkinter
from tkinter import ttk


version = 2.0
last_edit = [2,1,2022]

class ListBoxBeta(tk.Frame):
    def __init__(self, master):
        "Tkinter's ListBox with some improvements"
        super().__init__(master)

        #Define & grid scrollbar
        self.scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.list_box = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=0 ,width=30)
        
        self.list_box["yscrollcommand"] = self.scroll_bar.set
        self.scroll_bar['command'] = self.list_box.yview

        #self.scroll_bar.grid(row=0, column=1, sticky=tk.N+tk.S)
        #self.list_box.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.list_box.pack(side=tk.LEFT,expand=True,fill="both")
        self.scroll_bar.pack(side=tk.RIGHT,expand=True,fill="y")
        

    def addItem(self, value):
        self.list_box.insert(tk.END,value)

    def setList(self, value:list):
        #Clears old list, and sets new one;
        self.reset()
        for item in value:
            self.addItem(item)

    def getItem(self):
        #get's selected item
        if self.list_box.size() == 0 or self.list_box.curselection() == ():
            #Error Prevention
            return
        else:
            #Get the position of selection
            my_selection = self.list_box.curselection()[0]
            return self.list_box.get(my_selection)

    def reset(self):
        self.list_box.delete(0,tk.END)

    def top(self):
        self.list_box.see(0)

    def bottom(self):
        self.list_box.see(self.list_box.size())

    def defaultSelect(self):
        self.list_box.selection_set(0)
            
        


    
if __name__ == "__main__":
    #Interactive Log Test
    lb = ListBoxBeta(None)
    lb.pack(expand=True, fill="both")
    lb.set_list(["Hey,","What's", "up","???", "Fucker?"])
    lb.goBottom()
    lb.reset()
    lb.addItem("pony")
    lb.getItem()
    
    
    
