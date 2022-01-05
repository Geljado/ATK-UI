#JSON parsing - saving and data struckture

version = 2.1
last_edit = [1,1,2022]

import json, os

class Storage:
    """
    Storage(MyFileName) or Storage(file = MyFileName)
    --> If no file is given, it acts like a substorage and doesn't create a JSON file

    Set Item
    --> addItem(key, value)
    --> Storage += key, value

    Delete Item
    --> delItem(key)
    --> Storage - key

    Get Item
    --> getItem(key)
    --> value = Storage * key

    Check for Item
    --> checkItem(key)
    --> value = Storage == key

    Get a varible or Create it if't doesn't exsist. (Default creates as False)
    --> checkGet(key, default="AnyDefaultData")
    --> value = Storage != key
    ||| To set the default with the operator make it a list / tuple
    --> value = Storage != (Key, "AnyDefaultData")

    
    """
    
    def __init__(self, file:str=None,data:dict=None,log=None):
        self.log = log
        self.data = data or {}
        self.file = file
        
        
        if not self.file:
            self.data["is_sub_storage"] = True
        else:
            #Loads or create .json file
            self.load()
            self.log("Storage {} Loaded".format(file),"info")

    def convert(self):
        #make all substorage a dict
        for key in self.data:
            if isinstance(self.data[key], Storage):
                self.data[key] = self.data[key].data
    
    def reinit(self):
        #make all dicts containing a is_sub_storage variable a Storage Object
        for key in self.data:
            if isinstance(self.data[key], dict):
                if "is_sub_storage" in self.data[key]:
                    self.data[key] = Storage(data=self.data[key])

    def save(self):
        #Function to Save / Write to file
        #Only use , to avoid Bugs!
        #self.log("Saving {}...".format(self.file),"info")
        with open(self.file, "w", encoding="utf-8") as writefile:
                #Convert Substorage
                self.convert()
                json.dump(self.data,writefile)

    def load(self):
        #Loads data that is present, otherwise creates a file with the .save() function
        if os.path.exists(self.file):
            with open(self.file, "r", encoding="utf-8") as readfile:
                self.data = json.load(readfile)
                #Reinit substorage
                self.reinit()
            #When a File Exsited, Return True
            return True
        
        else:
            #If a file wasn't found, Create one
            self.log("{} not found, recreating...".format(self.file),"info")
            self.save()
            #When a File Didn't Exsited, Return False
            #This is so that Upper programms can fill in Template Data.
            return False

    #Set, Del, and Get item functions
    def setItem(self,key,value):
        key = key.lower()
        self.data[key] = value

    def delItem(self,key):
        key = key.lower()
        del self.data[key]
    
    def getItem(self,key):
        key = key.lower()
        return self.data[key]

    def checkItem(self,key):
        key = key.lower()
        return key in self.data

    def checkGet(self,key,default=None):
        #Get's an item or Creates / Returns it as False
        key = data.lower()
        if key in self.data:
            return self.data[key]
        else:
            self.data[key] = default
            return default

    #Magic Methodes, for complictations pruposes;
    def __iadd__(self,*args):
        "Storage +=  key, data  #Set Data"
        key, value = args[0][0], args[0][1]
        key = key.lower()
        self.data[key] = value
        return self

    def __sub__(self,key):
        "Storage -  key         #Del Data"
        del self.data[key]
        
    def __mul__(self,key):
        "data = Storage * key   #Get Data"
        key = key.lower()
        return self.data[key]

    def __eq__(self,key):
        "bool = Storage == key   #Check For Data"
        key = key.lower()
        return key in self.data

    def __ne__(self,data,*args):
        #Get's an item or Creates / Returns it as False
        #Check if data is just a key, or list / tuple
        if isinstance(data,str):
            key = data.lower()
            default = False
        else:
            key = data[0].lower()
            default = data[1]
            
        if key in self.data:
            return self.data[key]
        else:
            self.data[key] = default
            return default

    #Don't ask me, forgot why this one is important :c
    def __iter__(self):
        return iter(self.data.items())


if __name__ == "__main__":
    s1 = Storage("pony.test.storage")


    Variable = s1 != "naughty"
    print(Variable)
    
    
