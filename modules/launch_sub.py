import os, subprocess, io
from threading import Thread
class SubLauncherError(SyntaxError):
    pass

version = 1.1
last_edit = [20,9,2020]

"""
[0] One of the paths for the *game.exe or *atk.js was empty.
"""

class MySubLauncher:
    version = 1.1
    last_edit = [20,9,2020]
    """
    This is the MySubLauncher class:
    - It finds paths to the atk.js and the given game (default wall-e.exe)
    - It launches Frida with the given Paths
    - It has options to set paths manually, or find a specific *atk .js / *game .exe file
    """

    def setupLaunchPaths(self, game_exe:str, atk_js:str="atk.js"):
        """Walks from the Current Working Directory, in order to find \"atk.js\" and \"game.exe\
Options:
    game_exe - the full name of the *game.exe file.
    atk_js - the full name of the *atk.js file.
"""
        if self.work_dir == "":
            MyCWD = os.getcwd()
        else:
            os.chdir(self.work_dir)
            MyCWD = self.work_dir
        
        #Walk from Current Working Directory - Unlimeted walking depth;
        for path in os.walk(MyCWD):

            #If "backup" in name of a folder / path, skip;
            if "backup" in path[0].lower():
                continue

            #Walk through files to find the  "walle.exe"
            for file in path[2]:
                
                #Skip File that is a linked File or Named / marked with "backup"
                if ".lnk" in file.lower() or "backup" in file.lower():
                    continue

                #Found Wall-E.exe
                if game_exe.lower() in file.lower():

                    #Only overwite if path is emtpy
                    if self.game_path == "":
                        print("Found {}: ".format(game_exe), path[0]+os.sep+file)
                        self.game_path = path[0]+os.sep+file
                        
                    
                #Found ATK
                if atk_js in file.lower():

                    #Only overwite if path is emtpy
                    if self.atk_path == "":
                        print("Found AKT: ", path[0]+os.sep+file)
                        self.atk_path = path[0]+os.sep+file
                        

                        
    def run_subprocess(self, hook:bool=False):
        """Set up Frida / ATK subprocess
Create stdin and stdout as PIPE
Options:
    hook - False / True | If false it creates a *game.exe procces, if true it hooks in to a running *game.exe process.
      
        """
        if hook:
            hook = "n"
        else:
            hook = "f"

        #Emily's code
        self.process = subprocess.Popen(\
        'frida -{hook} \"{game_path}\" -l \"{atk_path}\" --no-pause -- -W'.format(\
        game_path=self.game_path, atk_path=self.atk_path, hook=hook)\
        , shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
    #################################################################
    #########################__ INIT AREA __#########################
    #########################VVVVVVVVVVVVVVV#########################


    def __init__(self, atk_path:str="", game_path:str="", game_exe:str="WALL-E.exe", atk_js:str="atk.js", game_hooking:bool=False, work_dir:str="", log_length:int=100):
        """Init's paths to ATK and *game.exe if needed;\nLaunces Subprocess Function in a thread;
Options:
    game_exe - the full name of the *game.exe file.
    atk_js - the full name of the *atk.js file.

    game_path - Path to the *game.js including {os_sep}filename.js | If given a path, overwrite the automatic search.
    atk_path - Path to the *atk.js including {os_sep}filename.js | If given a path, overwrite the automatic search.
        
    game_hooking - False / True | If false it creates a *game.exe procces, if true it hooks in to a running *game.exe process.
        """.format(os_sep = os.sep)

        self.work_dir = work_dir
        self.atk_path   =   atk_path
        self.game_path  =   game_path

        #Log List
        self.log = []
        self.log_length = log_length

        #Check if paths are empty
        if atk_path == "" or game_path == "":
            #If one is, setup path
            self.setupLaunchPaths(game_exe = game_exe, atk_js = atk_js)

        
        #Launch Frida/ATK subprocess
        if self.atk_path == "" or self.game_path == "":
            raise SubLauncherError("[0] One or more Paths Missing;")
        self.run_subprocess(hook=game_hooking)
        

        #Emily's Code
        #Launch stdout readout in a thread.
        self.thread = Thread(target = self.read_stdout, args = (self.process, ))
        self.thread.daemon = True
        self.thread.start()
        #Emily's code end


    def read_stdout(self,process):
        """Automatically reads from stdout \nPrints it to console \nNeeds to be threaded, since it reads until stdout closes;"""

        #Emily's Code
        s = io.TextIOWrapper(self.process.stdout)
        for line in s:
            print(line, end='')
            #MY CODE - REMOVE
            #if line != "":
            #    self.add_to_log(line)
                

    def add_to_log(self, line:str):
        #Will add new lines to log:
        LogLen = len(self.log)

        #cuts to have the log always at the log_length given;
        if LogLen >= self.log_length:
            self.log = self.log[:( self.log_length-1 )-LogLen]
            
        self.log.append(line)
                

    def write_stdin(self, msg:str):
        """Takes a clear string and fromats it with \n, encodes it then writes it to STDIN"""
        #Messages only get written to STDIN if the are terminated with a \n
        #So we check and add it if needed.
        if msg[-1:] != "\n":
            msg += "\n"

        #Emily's code
        #Write Message to STDIN
        try:
            self.process.stdin.write(msg.encode())
            self.process.stdin.flush()
            
        except(KeyboardInterrupt, SystemExit):
            self.process.stdin.write("quit".encode())
            self.process.stdin.flush()
        #Emily's code end
            


        
if __name__ == "__main__":
    #testing if it launches atk;
    Sub = MySubLauncher(work_dir="D:\Program Files (x86)\hidden_Walle")
