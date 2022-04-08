import time
import json
import os 
import colors as c
import front_end as fe
import system_repsonses as sr  



def get_currency_symbols(): 
    with open('currency_pair.json', 'r') as f: 
        return json.load(f)   

def get_parameters(): 
    with open('parameters.json', 'r') as f: 
        return json.load(f)

if __name__ == '__main__': 
    sys_count = 0
    setup_count = 0
    end_flag = False

    while(1): 
        try:
            #print(currency_symbol['Crypto_SYM'])
            time.sleep(1) # This has been put in place to safe gaurd the running of the program so that the json file 
                          # can be read without reading null values raising an exception error i.e. raise JSONDecodeError("Expecting value", s, err.value) from None
         
            currency_symbol = get_currency_symbols()

            sys_restart_flag = sr.get_sys_restart_flag()

         
            if currency_symbol['Real_Tend_SYM'] == "no_initialization": 
                if setup_count == 0:
                    print("Setup is yet to be complete")
                    #print("debugged")
                    setup_count = 1
               
            elif sys_restart_flag['restart'] == 'True':
                sys_restart_flag['restart'] = 'False'
                print("[Restart trading bot simulation]")

                with open('system_restart_flag.json', 'w') as f: 
                    json.dump(sys_restart_flag, f, indent = 4)
 
            else: 
                sys_exit_flag = sr.get_sys_exit_flag()
                # This has been put in place in the instance the user runs the UI and ends it without starting
                # the main2.py file running alongside it. Without this condition in place, would lock
                # the user out from being able to run the file. 
                if sys_count == 0 and sys_exit_flag['exit_trading'] == 'True': 
                    sys_exit_flag['exit_trading'] = 'False'
                    
                    with open('system_exit_flag.json', 'w') as f: 
                        json.dump(sys_exit_flag, f, indent = 4)

                elif sys_count < 1:
                    sys_count = 1

                if sys_exit_flag['exit_trading'] == 'True': 
                    sys_exit_flag['exit_trading'] = 'False' # reset immediatley back to false so we can re-run the program in the future
                    
                    with open('system_exit_flag.json', 'w') as f: 
                        json.dump(sys_exit_flag, f, indent = 4)

                    currency_pair = {
                                         "Crypto_SYM": "no_initialization",
                                         "Real_Tend_SYM": "no_initialization"
                                    }
                    
                    with open('currency_pair.json', 'w') as f: 
                        json.dump(currency_pair, f, indent = 4) # Writes crypto_symbol symbol AND real tender symbol to file    

                    sr.clearConsole()
                    print(f"{c.bcolors.HACKER_GREEN}End of trading simulation, Goodbye {c.bcolors.ENDC}$$$")
                    end_flag = True
                    exit()

                currency_symbol = get_currency_symbols()
                pair = (currency_symbol['Crypto_SYM'], currency_symbol['Real_Tend_SYM'])

                parameters = get_parameters()
                STOP_LOSS = float(parameters['STOP_LOSS'])
                PRICE_THRESHOLD = float(parameters['PRICE_THRESHOLD'])
                
                fe.FrontEnd.anaylsis(pair, STOP_LOSS, PRICE_THRESHOLD, fe.FrontEnd.time_in_seconds)
                 
                sr.clearConsole()
        
        except: 
             if end_flag != True: 
                 print(f"\n{c.bcolors.FAIL}KeyboardInterrupt {c.bcolors.ENDC}'Ctrl c' {c.bcolors.FAIL}has been entered")
                 print("User interface has adruptly ended")
                 break   
             else: 
                 break              
    
        