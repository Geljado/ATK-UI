#Subproccess launch moduel -  STDIN / STDOUT Communication

version = 2.0
last_edit = [4,1,2022]


import os, subprocess, io, time
from threading import Thread



#Subprocess Class
class Drone:
    "Class for launching subprocess of ATK"
    "WARNIG, version 2.0 ONLY"
    "This version will only hook in to games, and is NOT customizable"
    def kill(self):
        self.log("Killing ATK Subprocess", "info")
        self.process.kill()
    
    def __init__(self, game_path:str, atk_path:str=None,log=None):
        #Global Log Function
        self.log = log

        self.atk_path = atk_path or "{cwd}{sep}atk{sep}atk.js".format(sep=os.sep, cwd=os.getcwd() )
        #!!! WARNIG [-1:][0] ONLY FOR VERSION 2.0
        #THIS IS A BODGE TO GET THE EXE NAME INSTEAD OF PATH!!
        self.game_path = game_path.split(os.sep)[-1:][0]
        if not self.game_path:
            self.log("[0] No game path given","err")

    def _launch(self):
        #Run Subprocess
        self.log("Launching subprocess..","atk")
        self.run_subprocess()

        #Launch stdout readout in a thread.
        self.thread = Thread(target = self.read_stdout, args = (self.process, ))
        self.thread.daemon = True
        self.thread.start()

    def read_stdout(self,process):
        #Reads from IO sdtout
        s = io.TextIOWrapper(self.process.stdout)
        for line in s:
            #NEVER print in this function!!
            #It causes the main program to freeze; Probably due to some weird overlap.
            #Logs lines;
            if line != "":
                self.log(line)

    def write_stdin(self, msg:str):
        
        #Makes sure a \n is at the end of the string
        if msg[-1:] != "\n":
            msg += "\n"

        #Try to write; Encodes Message;
        try:
            self.process.stdin.write(msg.encode())
            self.process.stdin.flush()

        #Except there is an sysexit or Keyboard interrupt;
        except(KeyboardInterrupt, SystemExit):
            self.process.stdin.write("quit".encode())
            self.process.stdin.flush()

    def run_subprocess(self):

        #Prepare Launch String;
        MyLaunchString = 'frida -n \"{game_path}\" -l \"{atk_path}\" --no-pause -- -W'.format(
        game_path=self.game_path,
        atk_path=self.atk_path
        )

        self.log(MyLaunchString,"atk")

        #Launch Subprocess;
        self.process = subprocess.Popen(
        MyLaunchString,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
        
            




class GetGameCommands:
    
    #!!! Class still in testing; !!!
    "Auto-get Commands, experimetnal"
    def run_subprocess(self):

        #Prepare Launch String;
        MyLaunchString = 'frida -f \"{game_path}\" -l \"{atk_path}\" --no-pause -- -W'.format(
        game_path=self.game_path,
        atk_path=self.atk_path
        )

        self.log(MyLaunchString,"atk")

        #Launch Subprocess;
        self.process = subprocess.Popen(
        MyLaunchString,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
        

    def __init__(self, game_path:str, atk_path:str=None,log=None):
        #Global Log Function
        self.log = log
        
        self.atk_path = atk_path or "{cwd}{sep}atk{sep}atk.js".format(sep=os.sep, cwd=os.getcwd() ) 

        #Make sure paths arn't empty and have no " in it;
        if "" == game_path or "" == atk_path:
            self.log("[0] A path is missing.","err")
        
        if "\"" == game_path or "\"" == atk_path:
            self.log("[1] Path must not have \" in it.")

        #Create / link Variables;
        self.game_path = game_path
        self.atk_path = atk_path
        self.command_log = []

    def _launch(self):
        #Run Subprocess
        self.run_subprocess()

        #Launch stdout readout in a thread.
        self.thread = Thread(target = self.read_stdout, args = (self.process, ))
        self.thread.daemon = True
        self.thread.start()

    def read_stdout(self,process):

        #Reads from IO sdtout
        s = io.TextIOWrapper(self.process.stdout)
        for line in s:
            #NEVER print in this function!!
            #It causes the main program to freeze; Probably due to some weird overlap.
            #Logs lines;
            if line != "":
                self.command_log.append(line)

    def write_stdin(self, msg:str):
        
        #Makes sure a \n is at the end of the string
        if msg[-1:] != "\n":
            msg += "\n"

        #Try to write; Encodes Message;
        try:
            self.process.stdin.write(msg.encode())
            self.process.stdin.flush()

        #Except there is an sysexit or Keyboard interrupt;
        except(KeyboardInterrupt, SystemExit):
            self.process.stdin.write("quit".encode())
            self.process.stdin.flush()

    def _command_readout(self):
        #Launches Subprocess; Wait for game to launch properlly
        self._launch()
        time.sleep(4)

        #Dump Command names
        self.write_stdin("dumpCommandNames()")
        time.sleep(0.1)

        #Send a quit message to game; That also quits Frida automatically
        self.write_stdin("runCommand(\"exit\")")
        self.process.kill()

        #self.log("Gathered {} Commands..".format(len(self.command_log)),"info")
        #Return the log
        return self.command_log
    
