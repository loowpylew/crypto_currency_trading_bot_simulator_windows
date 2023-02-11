import os 
import json

def clearConsole(): 
        command = 'clear'
        if os.name in ('nt', 'dos'): 
            command = 'cls'
        os.system(command)    

def get_sys_exit_flag(): 
    with open('system_exit_flag.json', 'r') as f: 
        return json.load(f)  

def get_sys_restart_flag():
    with open('system_restart_flag.json', 'r') as f: 
        return json.load(f)  