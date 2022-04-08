from time import *
import colorama
import front_end as fe
import colors as c
import json
import system_repsonses as sr

colorama.init()

if __name__ == '__main__':
    try: 
        fe.FrontEnd.setup()
    except: 
        print(f"\n{c.bcolors.FAIL}KeyboardInterrupt {c.bcolors.ENDC}'Ctrl c' {c.bcolors.FAIL}has been entered")
        print("User setup has adruptly ended")
        exit()
    while(1):
        try:
            fe.FrontEnd.user_interface()
        except: 
            fe.FrontEnd.reset_trades_history() # In the instance the user ends the execution
                                               # of the user interface using the keyboard interupt 'ctrl c'. 
                                               # When the user decides to run UI again, this will allow for 
                                               # the removal of all trades history to prevent the previous simulations 
                                               # trade history from still being logged. 
            sys_exit_flag = sr.get_sys_exit_flag()
            sys_restart_flag = sr.get_sys_restart_flag()

            if sr.get_sys_exit_flag()['exit_UI'] == 'True':
                sys_exit_flag['exit_UI'] = 'False'
                sys_exit_flag['exit_trading'] = 'True'
                
                with open('system_exit_flag.json', 'w') as f: 
                    json.dump(sys_exit_flag, f, indent = 4)

                sr.clearConsole()
                print(F"{c.bcolors.HACKER_GREEN}Once rate limit points for starter account have regenerated, trading bot will end{c.bcolors.ENDC}")
                print(f"{c.bcolors.HACKER_GREEN}End of trading simulation UI, Goodbye {c.bcolors.ENDC}$$$") 
                break
            else: 
               print(f"\n{c.bcolors.FAIL}KeyboardInterrupt {c.bcolors.ENDC}'Ctrl c' {c.bcolors.FAIL}has been entered")
               print("User interface has adruptly ended")
               break                          
       
#https://www.youtube.com/watch?v=2FUupSx3ftw
#sudo code: 
#run two seperate programs at the same time 
#write values created in function to text file 
#run anaylysis function once values from text file have been written

#To install pip for remote server: https://phoenixnap.com/kb/install-pip-windows
            

    
            
    
    
    

        