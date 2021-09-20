import tkinter as tk

version = 1.0
last_edit = [20,9,2020]

class InteractiveLog(tk.Frame):
    def __init__(self, master, sendItemTo=None, SendToFunction=True, ErrorFitler:bool=True, ReadoutButton:bool=True):
        """An iteractive list, with a readout, or printout button"""

        super().__init__(master)

        self.sendItemTo = sendItemTo
        self.SendToFunction = SendToFunction
        self.ErrorFitler = ErrorFitler

        #define Item Counter
        self.ItemCounter = 0
        
        #Define & grid scrollbar
        self.MyScrollBar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.MyScrollBar.grid(row=0, column=1, sticky=tk.N+tk.S)

        #Define & grid listbox / itemlist
        self.MyItemList = tk.Listbox(self,exportselection=False,width=30)
        self.MyItemList["yscrollcommand"] = self.MyScrollBar.set
        self.MyItemList.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.MyScrollBar['command'] = self.MyItemList.yview

        if ReadoutButton:
            #Define & grid readout button
            self.MyReturnItemButton = tk.Button(self)
            self.MyReturnItemButton["text"] = "Print Command"
            self.MyReturnItemButton["command"] = self.get_item
            self.MyReturnItemButton.grid()

    def add_item(self, item:str):
        #Increases counter & Adds Item to the list

        #Simple error filter
        if self.ErrorFitler:
            if "error" in item.lower():
                return

        #Count ID up, add item to list
        self.ItemCounter += 1
        self.MyItemList.insert(self.ItemCounter,item)
        
        #Goes to last added item
        self.MyItemList.see(self.ItemCounter)
        
    def add_list(self, item_list:list):
        #Adds a whole ist on top;
        for item in item_list:
            self.add_item(item)

    def set_list(self, item_list:list):
        #Clears old list, and sets new one;
        self.clear_list()
        for item in item_list:
            self.add_item(item)

    def get_item_basic(self):
        #Get's item selected by user:
        MySelectedItem = self.MyItemList.curselection()
        #Checks that list is not empty
        if len(MySelectedItem) > 0:
            MySelectedItem = MySelectedItem[0]
            return self.MyItemList.get(MySelectedItem)
        else:
            #If list is empty, returns empty string
            return ""

    def get_item(self,return_item:bool=False):
        #Get's item selected by user:
        MySelectedItem = self.MyItemList.curselection()
        #Checks that list is not empty
        if len(MySelectedItem) > 0:
            MySelectedItem = MySelectedItem[0]
            item = self.MyItemList.get(MySelectedItem)
        else:
            #If list is empty, returns empty string
            return ""

        #Check what to do with Item
        #print
        if self.sendItemTo == None and not return_item:
            print(item)
        #Launch with given function
        elif self.sendItemTo != None and self.SendToFunction:
            self.sendItemTo(item)
        #Set Given Value to Item
        elif self.sendItemTo != None and not self.SendToFunction:
            self.sendItemTo = item

        else:
            return item

    def clear_list(self):
        #clears list
        while self.MyItemList.size() != 0:
            self.MyItemList.delete(0)
        self.ItemCounter = 0

    def go_top(self):
        self.MyItemList.see(0)
            

def FuzzySearch(item_list:list, search_term:str):

    temp_list = []

    for letter in search_term.lower():
        for item in item_list:
            if letter in item.lower():
                temp_list.append(item)
                
        item_list = temp_list
        temp_list = []

    item_list.sort()

    return item_list

def FuzzySearchTier(item_list:list, search_term:str, join:bool=False):

    temp_list = []

    #tier list; tier one has first search letter in it;
    tier1, tier2, tier3 = [], [], []

    for letter in search_term.lower():
        for item in item_list:
            if letter in item.lower():
                temp_list.append(item)
                
        item_list = temp_list
        temp_list = []

    #Sorting based on first letter
    for item in item_list:
        if search_term.lower() in item.lower() and item[:1].lower() == search_term[:1].lower():
            tier1.append(item)
        elif item[:1].lower() == search_term[:1].lower() or search_term.lower() in item.lower():
            tier2.append(item)
        else:
            tier3.append(item)

    #Sorting for consistent results
    tier1.sort()
    tier2.sort()
    tier3.sort()

    #check if join; Joining lists
    if join:
        #reuse of variable, don't get confused
        item_list = []
        for item in tier1:
            item_list.append(item)
        for item in tier2:
            item_list.append(item)
        for item in tier3:
            item_list.append(item)
        return item_list
    else:
        return tier1,tier2,tier3

def MakeCommand(string:str):
    return "runCommand(\"{}\");\n".format(string)
        
    
if __name__ == "__main__":
    #Interactive Log Test
    IL = InteractiveLog(None)
    IL.add_item("a")
    IL.add_item("b")
    IL.add_item("c")
    IL.add_item("d")
    IL.add_item("Error 20")
    IL.pack()
    print(IL.MyItemList.size())
    
    
