from time import *
import time # Allows us to handle various operations regarding time i.e. no. of seconds passed since the point where time begins for some event.
import datetime
import os 
import krakenex # library that is used to interact with the kraken API 
import json # Used to save/parse data that will be collected 
import colorama 
from tabulate import tabulate

import backend as bend
import StatisticalModels as sms
import data_output
import colors as c
import system_repsonses as sr

colorama.init()

class FrontEnd: 
    # Price threshold (percentage)
    # Use of 7 decimal places. This is because percentage difference between current open price and previous closing price tends to change within this range
    PRICE_THRESHOLD = 0 # 0.0000006 is the amount ive been using to set how much the price has to increase before a buy/sell event occurs
    # Stop loss (percentage)
    STOP_LOSS = 0 # 0.0000004 is the amount ive been using to set how much the price has to decrease before a buy/sell event occurs
    
    api = krakenex.API() # instatiation of krakenex library/connects to the kraken API 

    time_in_seconds = 3600 # default time to set by. User can change at a later date 

    max_timeStamp = str(int(time.time()))
    
    since = str(int(time.time() -  time_in_seconds)) # Requires edit, uses 3600 seconds which is equivilant to an hour whereas I want to know the buy sell operations from the past day
    
    arrayify_pair = [[],[]]  # Array to hold currency pair
    
    pair = ()

    crypto_currency_amount = 0
    real_tender_amount = 0
    
    loop_cycle = 1

    deposit_count = 0

    def setup(): 

        currency_pair = {
             "Crypto_SYM": "no_initialization",
             "Real_Tend_SYM": "no_initialization"
        }

        with open('currency_pair.json', 'w') as f: 
            json.dump(currency_pair, f, indent = 4) # Writes crypto_symbol symbol AND real tender symbol to file

        file_path = 'kraken.key'
        # check size of file is zero
        if os.stat(file_path).st_size == 0:
            print(f"{c.bcolors.HACKER_GREEN}Please enter your public key for your account: {c.bcolors.ENDC}\n", end='')
            public_key = input()
            print(f"{c.bcolors.HACKER_GREEN}Please enter your private key for your account:  {c.bcolors.ENDC}\n", end='')
            private_key = input()
            with open('kraken.key', 'w') as f: # Writes new keys to key file
                f.write(public_key)
                f.write("\n")
                f.write(private_key)
                print("\n")
        
        if FrontEnd.arrayify_pair == [[],[]]:
            # This has been put in place to reset trades history on call to restart the trading simulation
            # The first time the UI is run, nothing would have been deposited thus, this condition prevents 
            # the redundant assignment and use of a method call. 
            if FrontEnd.deposit_count > 0: 
                FrontEnd.deposit_count = 0  
                FrontEnd.reset_trades_history()

            print(f"{c.bcolors.HACKER_GREEN}Please enter key pair value you wish to trade with (i.e. {c.bcolors.ENDC}ANT{c.bcolors.HACKER_GREEN}, {c.bcolors.ENDC}USD{c.bcolors.HACKER_GREEN})")
            print(f"To view assert pairs you can trade with, press {c.bcolors.ENDC}'1'{c.bcolors.HACKER_GREEN}, otherwise press {c.bcolors.ENDC}'2' {c.bcolors.HACKER_GREEN}to continue: {c.bcolors.ENDC}")
            while(1):
                val = input()
                if(val == "1"):
                    data_output.get_asset_pairs_compatiability_finder()
                    print(f"{c.bcolors.WARNING}Enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to proceed to enter currency pair to trade with:{c.bcolors.ENDC}\n", end='')
                    val = input()
                    while(True):
                        if val != 'q':
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to enter currency pair to trade with:{c.bcolors.ENDC}")
                            val = input()
                        else:
                            break
                    break
                elif(val == "2"):
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter {c.bcolors.ENDC}'1'{c.bcolors.WARNING} to view asset pairs, otherwise press {c.bcolors.ENDC}'2' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")
                    
            FrontEnd.processing_currency_pair()

            
                    
            #print(arrayify_pair[1])
            #print(arrayify_pair)
            FrontEnd.pair = (FrontEnd.arrayify_pair[0], FrontEnd.arrayify_pair[1])
            #print(pair)
            print(f"{c.bcolors.HACKER_GREEN}Please enter the amount you wish to trade with (i.e. vol of crypto: {c.bcolors.ENDC}76.3941940413 {c.bcolors.HACKER_GREEN}, Amount of USD: {c.bcolors.ENDC}1000.0{c.bcolors.HACKER_GREEN})\n")

            print(f"Crypto Currency amount {c.bcolors.ENDC}[" + FrontEnd.arrayify_pair[0] + f"] {c.bcolors.HACKER_GREEN}:  {c.bcolors.ENDC}", end='')
            while(1): 
                val = input()
                try: 
                    to_float = float(val)
                    if to_float < 0:
                        print(f"{c.bcolors.WARNING}Please enter a number greater than 0:{c.bcolors.ENDC}")
                    else:
                        FrontEnd.crypto_currency_amount = to_float
                        break 
                except ValueError:
                    print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='')        

            print(f"{c.bcolors.HACKER_GREEN}Real Tender amount {c.bcolors.ENDC}[" + FrontEnd.arrayify_pair[1] + f"]{c.bcolors.HACKER_GREEN}:  {c.bcolors.ENDC}", end='')
            while(1): 
                val = input()
                try: 
                    to_float = float(val)
                    if to_float < 0:
                        print(f"{c.bcolors.WARNING}Please enter a number greater than 0:{c.bcolors.ENDC}")
                    else:
                        FrontEnd.real_tender_amount = to_float
                        break 
                except ValueError:
                    print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='') 

            balance = {
              str(FrontEnd.arrayify_pair[0]): str(FrontEnd.crypto_currency_amount),
              str(FrontEnd.arrayify_pair[1]): str(FrontEnd.real_tender_amount)
            }

            with open('balance.json', 'w') as f:
                json.dump(balance, f, indent = 4) # Writes new balance to file
            
            FrontEnd.deposit(FrontEnd.arrayify_pair[0] + FrontEnd.arrayify_pair[1], FrontEnd.crypto_currency_amount, FrontEnd.real_tender_amount)

            print(f"\n{c.bcolors.HACKER_GREEN}Set {c.bcolors.ENDC}STOP_LOSS/PRICE THRESHOLD {c.bcolors.HACKER_GREEN}based off change in in price of crypto in relation to real tender.")
            print(f"Type up the currency pair on Google to find live feed i.e. ")
            print(f"STOP LOSS: {c.bcolors.ENDC}-0.00000004, {c.bcolors.HACKER_GREEN}PRICE THRESHOLD: {c.bcolors.ENDC}0.00000008")
            print(f"\n{c.bcolors.HACKER_GREEN}Please enter 'STOP_LOSS':{c.bcolors.ENDC} ", end='')
            while(1):
                val = input() 
                try: 
                    to_float = float(val)
                    FrontEnd.STOP_LOSS = to_float
                    break 
                except ValueError:
                    print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='')        

            print(f"{c.bcolors.HACKER_GREEN}Please enter 'PRICE_THRESHOLD':{c.bcolors.ENDC} ", end='') 
            while(1):
                val = input() 
                try: 
                    to_float = float(val)
                    FrontEnd.PRICE_THRESHOLD = to_float
                    break 
                except ValueError:
                    print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='')        
            
            # We are creating a key value pair here so that when the anaylze function runs, within main2, we can specify the a given index of the dictionary by refering to 
            # the json file to pass the crypto and real tender symbols over to the get 'get_crypto_data' function. This is not possible without the json file as we will
            # be runnign the anaylze function within a seperate command shell so thatbothe the user interface and the analyze function can run interupted of one another. 
            currency_pair = {
              "Crypto_SYM": str(FrontEnd.arrayify_pair[0]),
              "Real_Tend_SYM": str(FrontEnd.arrayify_pair[1])
            }

            parameters = { 
                "STOP_LOSS": str(FrontEnd.STOP_LOSS) , 
                "PRICE_THRESHOLD":  str(FrontEnd.PRICE_THRESHOLD) 
            }

            with open('currency_pair.json', 'w') as f: 
                json.dump(currency_pair, f, indent = 4) # Writes crypto_symbol symbol AND real tender symbol to file

            with open('parameters.json', 'w') as f: 
                json.dump(parameters, f, indent = 4) 

            FrontEnd.api.load_key('kraken.key') # The loadkey function allows us to load our API keys and access the data specific to the account made on kraken
                                                # Here, we input the .KEY file as a parameter within the load_key function that stores both the API KEY and private
            
            sr.clearConsole()

    
    
    def anaylsis(pair, stop_loss, price_threshold, time_in_seconds):
        #pair = ("ANT", "USD") # Currency pair
        #print(FrontEnd.pair)
        #since = str(int(time.time() -  3600)) # Requires edit, uses 3600 seconds which is equivilant to an hour whereas I want to know the buy sell operations from the past day 
        #loop_cycle = 1
            
        balance = bend.get_fake_balance() 
         
        available_crypto = float(balance[pair[0]])
        available_money = float(balance[pair[1]])    
        count = 0
        while available_crypto == 0 and available_money == 0: 
            if count != 1: 
                print(f"{c.bcolors.WARNING}-------------------------------------WARNING-------------------------------------------")
                print("\n                  [Do not have enough funds to make a trade]")
                print("                     [Trading bot has paused in the meantime]")
                print("       [Please update account holdings via option '3' within the user interface]")
                print(f"\n--------------------------------------------------------------------------------------{c.bcolors.ENDC}")
                count = 1

            # exit trade has been placed here in the instance no funds have been placed and the UI is running
            # where we want to exit, the main2.py file will be paused withi the while loop above, 
            # thus we have created the set of conditions below to allow the user to exit the trading sim UI and bot
            sys_exit_flag = sr.get_sys_exit_flag()

            if sys_exit_flag['exit_trading'] == 'True': 
                sys_exit_flag['exit_trading'] = 'False' # reset immediatley back to false so we can re-run the program in the future
                
                with open('system_exit_flag.json', 'w') as f: 
                    json.dump(sys_exit_flag, f, indent = 4)

                sr.clearConsole()
                print("End of trading simulation, Goodbye $$$")
                exit()

                
            time.sleep(1)  # This has been put in place to safe gaurd the running of the program so that the json file 
                           # can be read without reading null values raising an exception error i.e. raise JSONDecodeError("Expecting value", s, err.value) from None
            balance = bend.get_fake_balance()
            available_crypto = float(balance[pair[0]])
            available_money = float(balance[pair[1]])
         
        while(FrontEnd.loop_cycle != 9):
            bend.analyze(pair, FrontEnd.since, price_threshold, stop_loss, FrontEnd.api, FrontEnd.loop_cycle, FrontEnd.time_in_seconds)
            #print(Tbs.loop_cycle)
            FrontEnd.loop_cycle += 1 
            time.sleep(1) # Anything faster than this will cause the API to produce Key Error: 'result' to prevent DDOS attack/manipulation of the direction in the market.           
                          # First rate limit will be reached when loop hits 9th gathering of trades history (OHLC), 
                          # 60 different data points. 'while' loop occurs 9 times thus 60 data points * 9 = 540 opening and closing prices are downloaded before every regenertion 
         
        print(f"\n{c.bcolors.HACKER_GREEN}Regenerating rate limit points for starter account:\n {c.bcolors.ENDC}")
        #await asyncio.sleep(46)
        FrontEnd.countdown(46)  # This is placed here once we exceed our rate limit of 15 points due to API Endpoint requests i.e. TradesHistory(+2), Balance(+1)
                       # Each second passed gives a reduction of -0.33 points thus (1 request per second * TradesHistory increases counter by 2 each time, 
                       # thus on the 9th request of OHLC data, we go above our counter limit and hit 18 points). 15 points/-0.33 == 54.54 seconds thus, 
                       # I have rounded to 46 seconds as the countdown function uses the divmod() function which requires a whole number of seconds/minutes. 
                       # Divide the remaining no. of points by 0.33 to get no.of seconds you have to wait to set rate limit back to 0. 
        FrontEnd.loop_cycle = 1
    

    
    def user_interface(): 
        print(f"\n{c.bcolors.ENDC}1. {c.bcolors.HACKER_GREEN}View account holdings")
        print(f"{c.bcolors.ENDC}2. {c.bcolors.HACKER_GREEN}View trades history")
        print(f"{c.bcolors.ENDC}3. {c.bcolors.HACKER_GREEN}Update account holdings")
        print(f"{c.bcolors.ENDC}4. {c.bcolors.HACKER_GREEN}Manipulate 'STOP LOSS' value")
        print(f"{c.bcolors.ENDC}5. {c.bcolors.HACKER_GREEN}Manipulate 'PROFIT MARGIN' value")
        print(f"{c.bcolors.ENDC}6. {c.bcolors.HACKER_GREEN}Set UNIX timestamp ")
        print(f"{c.bcolors.ENDC}7. {c.bcolors.HACKER_GREEN}View live ranking of top 100 most volatile crypto currencies (past 24hrs)")
        print(f"{c.bcolors.ENDC}8. {c.bcolors.HACKER_GREEN}Restart trading simulation")
        print(f"{c.bcolors.ENDC}9. {c.bcolors.HACKER_GREEN}End trading simulation")
        print(f"{c.bcolors.ENDC}10. {c.bcolors.HACKER_GREEN}Help menu")
        print(f"{c.bcolors.WARNING}Enter value betwen {c.bcolors.ENDC}1 - 10 {c.bcolors.WARNING}accordingly:{c.bcolors.ENDC}\n", end="")
        choice = input()

        # output account holdings 
        if choice == "1": 
             balance = bend.get_fake_balance()
             available_crypto = float(balance[FrontEnd.pair[0]])
             available_money = float(balance[FrontEnd.pair[1]])
             print(f"{c.bcolors.HACKER_GREEN}Available {c.bcolors.ENDC}[" + FrontEnd.pair[0] + f"]{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}" + str(available_crypto))
             print(f"{c.bcolors.HACKER_GREEN}Available {c.bcolors.ENDC}[" + FrontEnd.pair[1] + f"]{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}" + str(available_money))
             print(f"{c.bcolors.WARNING}Press '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return to options menu:{c.bcolors.ENDC}\n", end='')
             val = input()
             while(True):
                if val != 'q':
                    print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to options menu:{c.bcolors.ENDC}\n", end='')
                    val = input()
                else: 
                    break
    
             sr.clearConsole() 


        # output trades history 
        if choice == "2": 
            sr.clearConsole()

            trades_history = bend.get_fake_trades_history()['result']['trades']
            count = 0
            for trade in trades_history: 
                trade = trades_history[trade]
                #print('\033[91m' + 'some red text') # test to see if outputs in command prompt, was only working in visual studio terminal 
                                                     # before trying to re-install colorama i.e. 
                                                     # pip install colorama 
                                                     # Requirement already satisfied: colorama in c:\users\lewis\appdata\roaming\python\python38\site-packages (0.4.3)
                                                     # so included coloroma.init() method for windows. Will produce no unusual ouput on linuxmac machines. 
                                                     # coloroma.init() makes colour codes within bcolors method work in windows

                #print(c.bcolors.BOLD + "BOLD" + c.bcolors.ENDC)
                #print(c.bcolors.FAIL + "FAIL" + c.bcolors.ENDC)
                #print(c.bcolors.HACKER_GREEN + "HACKER_GREEN" + c.bcolors.ENDC)
                #print(c.bcolors.HEADER + "HEADER" + c.bcolors.ENDC)
                #print(c.bcolors.OKBLUE + "OKBLUE" + c.bcolors.ENDC)
                #print(c.bcolors.OKCYAN + "OKCYAN" + c.bcolors.ENDC)
                #print(c.bcolors.UNDERLINE + "UNDERLINE" + c.bcolors.ENDC)
                #print(c.bcolors.WARNING + "WARNING" + c.bcolors.ENDC)
                
                if trade['type'] != 'deposit': 
                    count += 1
                    print(f"\n{c.bcolors.HACKER_GREEN}Number of trade: {c.bcolors.ENDC}", count) 
                    print(f"{c.bcolors.HACKER_GREEN}Currency pair: {c.bcolors.ENDC}", trade['pair'])
                    print(f"{c.bcolors.HACKER_GREEN}Price: {c.bcolors.ENDC}", trade['price'])
                    print(f"{c.bcolors.HACKER_GREEN}Type: {c.bcolors.ENDC}", trade['type'])
                    print(f"{c.bcolors.HACKER_GREEN}Cost: {c.bcolors.ENDC}", trade['cost'])
                    print(f"{c.bcolors.HACKER_GREEN}Time of {trade['type']}: {c.bcolors.ENDC}", trade['time'])
                    print(f"{c.bcolors.HACKER_GREEN}Vol: {c.bcolors.ENDC}", trade['vol']) 
                else: 
                    print(f"\n{c.bcolors.HACKER_GREEN}$$${c.bcolors.ENDC}[{c.bcolors.HACKER_GREEN}DEPOSIT{c.bcolors.ENDC}-{c.bcolors.HACKER_GREEN}REQUEST{c.bcolors.ENDC}]{c.bcolors.HACKER_GREEN}$$${c.bcolors.ENDC}") 
                    print(f"{c.bcolors.HACKER_GREEN}Currency pair: {c.bcolors.ENDC}", trade['pair'])
                    print(f"{c.bcolors.HACKER_GREEN}Price: {c.bcolors.ENDC}", trade['price'])
                    print(f"{c.bcolors.HACKER_GREEN}Type: {c.bcolors.ENDC}", trade['type'])
                    print(f"{c.bcolors.HACKER_GREEN}Cost: {c.bcolors.ENDC}", trade['cost'])
                    print(f"{c.bcolors.HACKER_GREEN}Time of {trade['type']}: {c.bcolors.ENDC}", trade['time'])
                    print(f"{c.bcolors.HACKER_GREEN}Vol: {c.bcolors.ENDC}", trade['vol']) 


            print(f"{c.bcolors.WARNING}Press '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return to options menu:{c.bcolors.ENDC}\n", end='')
            val = input()
            while(True):
                if val != 'q':
                    print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to options menu{c.bcolors.ENDC}")
                    val = input()
                else: 
                    break
           
            sr.clearConsole() 


        # update account holdings 
        if choice == "3":
            sr.clearConsole()
            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to continue enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}")
            val = ""
            while(1):
                if val == 'exit': 
                    break
                val = input()
                if val == 'y': 
                    print(f"{c.bcolors.HACKER_GREEN}Input new crypto curreny amount [{c.bcolors.ENDC}{FrontEnd.arrayify_pair[0]}{c.bcolors.HACKER_GREEN}]: {c.bcolors.ENDC}", end='')
                    while(1): 
                        val = input()
                        try: 
                            to_float = float(val)
                            if to_float < 0:
                                print(f"{c.bcolors.WARNING}Please enter a number greater than 0{c.bcolors.ENDC}")
                            else:
                                crypto_amount = to_float
                                old_crypto_currency_amount = FrontEnd.crypto_currency_amount
                                FrontEnd.crypto_currency_amount = old_crypto_currency_amount + crypto_amount
                                break  
                        except ValueError:
                            print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='')        
                   
                    print(f"{c.bcolors.HACKER_GREEN}Input new real Tender amount [{c.bcolors.ENDC}" + FrontEnd.arrayify_pair[1] + f"{c.bcolors.HACKER_GREEN}]: {c.bcolors.ENDC}", end='')
                    while(1): 
                         val = input()
                         try: 
                             to_float = float(val)
                             if to_float < 0:
                                 print(f"{c.bcolors.WARNING}Please enter a number greater than 0: {c.bcolors.ENDC}", end='')
                             else:
                                 real_tender_amount = to_float
                                 old_real_tender_amount = FrontEnd.real_tender_amount
                                 FrontEnd.real_tender_amount = old_real_tender_amount + real_tender_amount
                   
                                 balance = {
                                     str(FrontEnd.arrayify_pair[0]): str(FrontEnd.crypto_currency_amount),
                                     str(FrontEnd.arrayify_pair[1]): str(FrontEnd.real_tender_amount)
                                     }
                   
                                 with open('balance.json', 'w') as f:
                                     json.dump(balance, f, indent = 4) # Writes new balance to file
                                 val = "exit"
                                 break 
                         except ValueError:
                             print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='')
                     
                    FrontEnd.deposit(FrontEnd.arrayify_pair[0] + FrontEnd.arrayify_pair[1], crypto_amount, real_tender_amount)
                            
                            
                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y'{c.bcolors.WARNING} or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")
           
            sr.clearConsole()

        # Manipulate 'STOP LOSS' value"
        if choice == "4": 
            sr.clearConsole()
            print(f"\n{c.bcolors.HACKER_GREEN}Current STOP_LOSS value:{c.bcolors.ENDC} {FrontEnd.STOP_LOSS}")
            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to continue enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}")
            val = ""
            while(1):
                if val == 'exit': 
                    break
                val = input()
                if val == 'y': 
                    print(f"\n{c.bcolors.HACKER_GREEN}General rule of thumb, you want your PROFIT MARGIN to be larger than your STOP LOSS")
                    print(f"{c.bcolors.HACKER_GREEN}Input new value: {c.bcolors.ENDC}")
                    while(1): 
                        val = input()
                        try: 
                            to_float = float(val)
                            
                            FrontEnd.STOP_LOSS = to_float

                            val = FrontEnd.getParameters()
                            
                            val['STOP_LOSS'] = str(FrontEnd.STOP_LOSS)
                            
                            with open('parameters.json', 'w') as f: 
                                json.dump(val, f, indent = 4) 

                            val = "exit"

                            break 
                        except ValueError:
                            print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}", end='') 

                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y' {c.bcolors.WARNING}or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")
                     
            sr.clearConsole()

        # Manipulate 'PROFIT MARGIN' value
        if choice == "5": 
            sr.clearConsole()
            print(f"{c.bcolors.HACKER_GREEN}Current PRICE THRESHOLD value:{c.bcolors.ENDC} {FrontEnd.PRICE_THRESHOLD}")
            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to continue enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}")
            val = ""
            while(1):
                if val == 'exit': 
                    break
                val = input()
                if val == 'y': 
                    print(f"{c.bcolors.HACKER_GREEN}General rule of thumb, you want your PROFIT MARGIN to be larger than your STOP LOSS")
                    print(f"{c.bcolors.HACKER_GREEN}Input new value:{c.bcolors.ENDC} ")
                    while(1): 
                        val = input()
                        try: 
                            to_float = float(val)
                            FrontEnd.PRICE_THRESHOLD = to_float

                            val = FrontEnd.getParameters()
                            
                            val['PRICE_THRESHOLD'] = str(FrontEnd.PRICE_THRESHOLD)
                            
                            with open('parameters.json', 'w') as f: 
                                json.dump(val, f, indent = 4)
                            
                            val = "exit"
                            
                            break
                        except ValueError:
                            print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}")
                            pass
                    
                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y' {c.bcolors.WARNING}or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")
            
            sr.clearConsole()

        # Set UNIX timestamp
        if choice == "6":
            sr.clearConsole()
            print(f"{c.bcolors.HACKER_GREEN}Current UNIX timestamp: {c.bcolors.ENDC}" + str(FrontEnd.since))
            print(f"{c.bcolors.HACKER_GREEN}Current epoch: {c.bcolors.ENDC}" + str(FrontEnd.time_in_seconds))
            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to continue enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}: {c.bcolors.ENDC}")
            val = ""
            while(1):
                if val == 'exit': 
                    break
                val = input()
                if val == 'y': 
                    print(f"{c.bcolors.HACKER_GREEN}General rule of thumb, you want your PROFIT MARGIN to be larger than your STOP LOSS")
                    print(f"{c.bcolors.HACKER_GREEN}Input new value:{c.bcolors.ENDC} ")
                    while(1): 
                        if val == "exit":
                            break
                        
                        print(f"{c.bcolors.FAIL}\nRestriction: {c.bcolors.HACKER_GREEN} Min value: ({c.bcolors.ENDC}3600 {c.bcolors.HACKER_GREEN}sec == {c.bcolors.ENDC}1 {c.bcolors.HACKER_GREEN}hr)")
                        print(f"\n{c.bcolors.HACKER_GREEN}Before entering a new epoch value; if you would like to")
                        print("calculate no. of seconds into minutes, hours, days and")
                        print(f"months, enter {c.bcolors.ENDC}'y', {c.bcolors.HACKER_GREEN}otherwise enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}:{c.bcolors.ENDC} ")
                        flag = False
                        while(1):
                            if flag != True:
                                val = input()
                                if val == 'y':
                                    print(f"\n{c.bcolors.HACKER_GREEN}Enter no. of seconds:{c.bcolors.ENDC} ")
                                    while(1):
                                        if val != 'q':
                                            val = input()
                                            try: 
                                                while(1): 
                                                    to_float = float(val)
                                                    if to_float >= 3600: 
                                                        in_months = to_float / 2629746
                                                        in_days = to_float / (24 * 3600)
                                                        in_hours = (to_float % (24 * 3600)) / 3600 
                                                        in_minutes = (to_float % (24 * 3600 * 3600)) / 60 

                                                        print(f"\n{c.bcolors.HACKER_GREEN}Number in months: {c.bcolors.ENDC}", in_months)
                                                        print(f"{c.bcolors.HACKER_GREEN}Number in days: {c.bcolors.ENDC}", in_days)
                                                        print(f"{c.bcolors.HACKER_GREEN}Number in hours: {c.bcolors.ENDC}", in_hours)
                                                        print(f"{c.bcolors.HACKER_GREEN}Number in minutes: {c.bcolors.ENDC}", in_minutes)
                                                        break
                                                    else:  
                                                        print(f"{c.bcolors.WARNING}Please enter an acceptable no. of seconds: {c.bcolors.ENDC}")
                                                        val = input()

                                                print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to continue: {c.bcolors.ENDC}")
                                                while(1):
                                                    val = input()
                                                    if val != 'q':
                                                        print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to continue{c.bcolors.ENDC}")
                                                    else: 
                                                        break
                                            except: 
                                                print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}")
                                        else:
                                            flag = True
                                            break

                                elif val == 'n': 
                                    break 
                                else: 
                                    print(f"{c.bcolors.WARNING}Please enter {c.bcolors.ENDC}'y'{c.bcolors.WARNING} or {c.bcolors.ENDC}'n'{c.bcolors.WARNING}: {c.bcolors.ENDC}")
                            else: 
                                break
                                    
                        print(f"{c.bcolors.HACKER_GREEN}\nSet new epoch: {c.bcolors.ENDC}")
                        while(1):
                            try: 
                                val = input()
                                to_float = float(val)
                                if(to_float >= 3600):
                                    FrontEnd.since = str(int(time.time() - to_float))
                                    FrontEnd.time_in_seconds = to_float
                                    
                                    val = "exit"
                                    print(val)
                                    break 
                                else: 
                                    print(f"{c.bcolors.WARNING}Please enter an acceptable no. of seconds: {c.bcolors.ENDC}")
                            except ValueError:
                                print(f"{c.bcolors.WARNING}Please enter a number: {c.bcolors.ENDC}")
                         
                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                     print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y' {c.bcolors.WARNING}or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")
            
            sr.clearConsole()
        
        # View live ranking of 100 top most volatile crypto currencies (past 24hrs)
        if choice == "7": 
            sr.clearConsole()

            data_output.get_live_top_100_ranking_crypto_currencies()
            print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to return to options menu: {c.bcolors.ENDC}")
            while(1): 
                val = input()
                if val == 'q': 
                     sr.clearConsole()
                     break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter {c.bcolors.ENDC}'q' {c.bcolors.WARNING}to return to options menu: {c.bcolors.ENDC}")

        # Restart trading simulation
        if choice == "8": 
            sr.clearConsole()

            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to end the restart the trading simulator")
            print(f"{c.bcolors.HACKER_GREEN}enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}:{c.bcolors.ENDC} ")
            while(1):
                val = input()
                if val == 'y': 
                    FrontEnd.arrayify_pair = [[],[]] # Initially evaluted as empty to allow setup to proceed 
            
                    print("Restarting trading simulation\n")
                    
                    FrontEnd.setup()

                    sys_restart_flag = sr.get_sys_restart_flag()
                    sys_restart_flag['restart'] = 'True'

                    with open('system_restart_flag.json', 'w') as f: 
                        json.dump(sys_restart_flag, f, indent = 4)
                    
                    break     
                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y'{c.bcolors.WARNING} or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")

        # End trading simulation
        if choice == "9": 
            sr.clearConsole()
            print(f"{c.bcolors.HACKER_GREEN}If you're sure you want to end the trading simulator")
            print(f"{c.bcolors.HACKER_GREEN}enter {c.bcolors.ENDC}'y'{c.bcolors.HACKER_GREEN}, otherwise, enter {c.bcolors.ENDC}'n'{c.bcolors.HACKER_GREEN}:{c.bcolors.ENDC} ")
            while(1):
                val = input()
                if val == 'y': 
                    sr.clearConsole()
                    sys_exit_flag = sr.get_sys_exit_flag()
                    sys_exit_flag['exit_UI'] = 'True'

                    with open('system_exit_flag.json', 'w') as f: 
                        json.dump(sys_exit_flag, f, indent = 4)

                    exit()
                elif val == 'n':
                    sr.clearConsole()
                    break
                else: 
                    print(f"{c.bcolors.WARNING}Please enter either {c.bcolors.ENDC}'y'{c.bcolors.WARNING} or {c.bcolors.ENDC}'n' {c.bcolors.WARNING}to continue: {c.bcolors.ENDC}")

        # Help menu
        if choice == "10": 
            sr.clearConsole()

            while(1):
                print("Help menu:")
                print(f"1. {c.bcolors.HACKER_GREEN}Setting PRICE THRESHOLD{c.bcolors.ENDC}")
                print(f"2. {c.bcolors.HACKER_GREEN}Setting STOP LOSS{c.bcolors.ENDC}")
                print(f"3. {c.bcolors.HACKER_GREEN}Setting currency pair{c.bcolors.ENDC}")
                print(f"4. {c.bcolors.HACKER_GREEN}Setting UNIX timestamp{c.bcolors.ENDC}")
                print(f"5. {c.bcolors.HACKER_GREEN}Current open price{c.bcolors.ENDC}")
                print(f"6. {c.bcolors.HACKER_GREEN}Previous closing price{c.bcolors.ENDC}")
                print(f"7. {c.bcolors.HACKER_GREEN}Simple Moving Average{c.bcolors.ENDC}")
                print(f"8. {c.bcolors.HACKER_GREEN}EWMA{c.bcolors.ENDC}")
                print(f"9. {c.bcolors.HACKER_GREEN}Standard Deviation{c.bcolors.ENDC}")
                print(f"10. {c.bcolors.HACKER_GREEN}Bollinger Bands{c.bcolors.ENDC}")
                print(f"11. {c.bcolors.HACKER_GREEN}Parabolic SAR{c.bcolors.ENDC}")
                print(f"12. {c.bcolors.HACKER_GREEN}RSI(relative Strength Index){c.bcolors.ENDC}")
                print(f"13. {c.bcolors.HACKER_GREEN}ADX(Average Directional Index){c.bcolors.ENDC}")
                print(f"14. {c.bcolors.HACKER_GREEN}Williams %R{c.bcolors.ENDC}")
                print(f"15. {c.bcolors.HACKER_GREEN}Percentage Difference{c.bcolors.ENDC}")
                print(f"q. {c.bcolors.HACKER_GREEN}Exit{c.bcolors.ENDC}")
                print(f"{c.bcolors.HACKER_GREEN}Input the corresponding value for further information: {c.bcolors.ENDC}")
                val = input()
            
                if val == "1":
                    print("\nIt is best advised to set the price threshold at a larger value than the stop")
                    print("loss. This is so that you can componsate for any prior dramatic shift (decrease)")
                    print("in the price of a given token once the price has increased again. If the price ")
                    print("increases aboveour price threshold; we use the price threshold to compare against") 
                    print("the difference between the current opening price, and the prior closing price.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "2":
                    print("It is best advised to set the stop loss at a lower value than the price")
                    print("threshold. This is because the stop loss is comapared against the resultant")
                    print("(difference) of opening price minus the closing price which will always evaluate")
                    print("to a negative value. The price of a token would not operate within a negative") 
                    print("range as this would mean the value of a token would be worth a negative value.") 
                    print("Thus, an increase that still remained within this qaurtile would still evaluate to")
                    print("the token being negative rendering it worthless.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                
                elif val == "3": 
                    print("It is advised to change account holdings, STOP LOSS and PRICE THRESHOLD before")
                    print("proceeding to change the currency pair you wish to trade with. If you do not")
                    print(", this will result in the previous parameters being applied to the old currency")
                    print("pair, where there will be a high likelihood that they do not correlate within") 
                    print("the bounds of the new pair, thus produce inaccurate results")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                
                elif val == "4": 
                    print("There are two standard representations of time. One is the number of seconds")
                    print("since the Epoch, in UTC (a.k.a. GMT). It may be an integer or a floating point")
                    print("number (to represent fractions of seconds). The Epoch is system-defined; on")
                    print("Unix , it is generally January 1st , 1970. By specifying a time in seconds,")
                    print("you are setting how far back in time you wish to download historical open,")
                    print("highs, lows and closes (OHLC) of trading data. The further back you go, the")
                    print("more accuate the buy/sell events will be. The trade off is that dependant on")
                    print("how far back you decide to download; will affect the runtime of other parts")
                    print("of the trading bot given the synchous nature at which the api allows us to ") 
                    print("download (OHLC) data, which in turn will affect the reponse time of the trading") 
                    print("bot in respects to analysing the current state of the given currency pair you")
                    print("decide to trade with to placing buy/sell events accuratley")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help menu:{c.bcolors.ENDC}")

                elif val == "5":
                    print("Current open price speaks for itself and represents the most recent open price")
                    print("of the data downloaded within the past 1hr (3600) seconds by default. This can")
                    print("be changed of course by setting the TIMESTAMP to number of seconds at which")
                    print("you wish to download historical data.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "6":
                    print("We use the previous closing price so that we can measure the difference between")
                    print("itself and the current open price. Given the trading bot has been designed to")
                    print("adjust to micro changes in the change in price of a given currecny pair, we can")
                    print("measure the difference between epoches (interval at which we download data over") 
                    print("a given period of time (by default, every minute for the past hour); thus, based")
                    print("on the difference, this is one way we can determine there has been a change in")
                    print("price.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                elif val == "7":
                    print("The simple moving average (SMA) calculates the average of a selected range of")
                    print("prices, usually closing prices, by the number of periods in that range. This")
                    print("technical indicator can aid in determining if an asset price will continue or")
                    print("if it will reverse a bull or bear trend.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                elif val == "8":
                    print("Places a greater weight and significance on the most recent data points within")
                    print("the historical data downloaded. Like all moving averages, this technical")
                    print("indicator is used to produce buy and sell signals based on crossovers and")
                    print("divergences from the historical average.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "9":
                    print("Standard deviation is the statistical measure of market volatility, measuring")
                    print("how widely prices are dispersed from the average price. If prices trade in a")
                    print("narrow trading range, the standard deviation will return a low value that")
                    print("indicates low volatility.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "10":
                    print("Bollinger Bands are envelopes plotted at a standard deviation level above and")
                    print("below a simple moving average of the price. Because the distance of the bands") 
                    print("is based on standard deviation, they adjust to volatility swings in the")
                    print("underlying price. Bollinger Bands use 2 parameters, Period and Standard")
                    print("Deviations, StdDev.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "11":
                    print("The parabolic SAR is a technical indicator used to determine the price direction")
                    print("of an asset, as well as draw attention to when the price direction is changing.")
                    print("Sometimes known as the 'stop and reversal system', the parabolic SAR was")
                    print("developed by J. Welles Wilder Jr., creator of the relative strength index (RSI).")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "12":
                    print("RSI is an oscillator indicator, with a range between 0 to 100. When markets")
                    print("have reached an oversold condition it may indicate that the move has reached")
                    print("an exhaustion point and a reversal couldbe at hand. If the RSI reading is")
                    print("below 20 and rising then is a potential signal to see the market reverse and")
                    print("start trading higher. On the other hand, when we see situations where the ")
                    print("market has rallied and the RSI has reached above 80 and then starts to fall,")
                    print("we may see a situation where the market could reverse and head lower.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                elif val == "13":
                    print("Used to determine the strength of a particular trend. The trend has strength") 
                    print("when ADX is above 25; the trend has strength when ADX is above 25; the trend")
                    print("is weak or the price is trendless when ADX is below 20, according to Wilder")
                    print("(the person who devised the equation")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                elif val == "14":
                    print("Williams %R, or just %R, is a technical analysis oscillator showing the current")
                    print("closing price in relation to the high and low of the past N days. A reading above") 
                    print("-20 is usually considered overbought. A reading below -80 is usually considered")
                    print("oversold.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")

                elif val == "15": 
                    print("Used to calculate the degree of change in price of the current open price in") 
                    print("relation to the closing price over a specific period of time using simple")
                    print("arithmetic. This metric is useful to investors, who use it to compare stocks with")
                    print("different price movements.")
                    print(f"\n{c.bcolors.HACKER_GREEN}Enter {c.bcolors.ENDC}'q' {c.bcolors.HACKER_GREEN}to exit back help options menu: {c.bcolors.ENDC}")
                    while(1):
                        val = input()
                        if val == 'q': 
                            sr.clearConsole()
                            break 
                        else:
                            print(f"{c.bcolors.WARNING}Please enter '{c.bcolors.ENDC}q{c.bcolors.WARNING}' to return back to help options menu:{c.bcolors.ENDC}")
                elif val == "q": 
                    sr.clearConsole()
                    break
                else: 
                     sr.clearConsole()
        else: 
            sr.clearConsole()


    def countdown(t):
        while t > -1:
            if t == -1: 
                 print(timer, end=" ")
                 print("\n")
                 break
            else: 
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                print(timer, end="\r") # '\r' allows to override the current line of the terminal emulator 
                time.sleep(1)
                t -= 1 


    def get_compatible_crypto_symbols_with_real_tender(): 
        with open('compatible_crypto_symbols_with_real_tender.json', 'r') as f: 
            return json.load(f)    


    def get_compatible_crypto_symbols_with_Z_tender(): 
        with open('compatible_crypto_symbols_with_Z_tender.json', 'r') as f: 
            return json.load(f)


    def getParameters(): 
        with open('parameters.json', 'r') as f: 
            return json.load(f)  


    def allowable_currency_pairs(): 
        with open('allowable_currency_pairs.json', 'r') as f: 
            return json.load(f)    
    
    def reset_trades_history(): 
        trades_history = bend.get_fake_trades_history()

        trades_history = {
                             "error": [],
                             "result": {
                                 "trades": {
                                     "DEPOSIT-REQUEST[1]": {
                                         "ordertxid": "OQCLML-BW3P3-BUCMWZ",
                                         "postxid": "TKH2SE-M7IF5-CFI7LT",
                                         "pair": "",
                                         "time": "",
                                         "type": "",
                                         "ordertype": "",
                                         "price": "",
                                         "cost": "",
                                         "fee": "0.00000",
                                         "vol": "",
                                         "margin": "0.00000",
                                         "misc": ""
                                     }
                                 },
                                 "count": 1
                             }
                         }

        with open('tradeshistory.json', 'w') as f: 
            json.dump(trades_history, f, indent = 4)
        


    def processing_currency_pair():           
            print(f"{c.bcolors.HACKER_GREEN}Crypto Currency: {c.bcolors.ENDC}", end='')
            FrontEnd.arrayify_pair[0] = input()
            crypto_sym_real_tend = FrontEnd.get_compatible_crypto_symbols_with_real_tender()
            Z_sym_real_tend = FrontEnd.get_compatible_crypto_symbols_with_Z_tender()
            #print(len(crypto_sym_real_tend))
            val = True
            while(val):
                counter = 0
                Z_counter = 0
                for crypto_token in crypto_sym_real_tend:
                    if FrontEnd.arrayify_pair[0] == crypto_sym_real_tend[crypto_token]: 
                        val = False 
                    elif FrontEnd.arrayify_pair[0] != crypto_sym_real_tend[crypto_token]:
                        counter += 1
               
                for crypto_token in Z_sym_real_tend: 
                   if FrontEnd.arrayify_pair[0] == Z_sym_real_tend[crypto_token]: 
                       val = False 
                   elif FrontEnd.arrayify_pair[0] != Z_sym_real_tend[crypto_token]:
                       Z_counter += 1
                
                sum_of_counters = counter + Z_counter
                full_len = len(crypto_sym_real_tend) + len(Z_sym_real_tend)
                if sum_of_counters == full_len: 
                    print(f"{c.bcolors.WARNING}Please enter a valid token symbol: {c.bcolors.ENDC}")
                    FrontEnd.arrayify_pair[0] = input()    

            #(arrayify_pair[0]) 
            print(f"{c.bcolors.HACKER_GREEN}Real Tender: {c.bcolors.ENDC}", end='')
            FrontEnd.arrayify_pair[1] = input()
            sym_real_tend = ["USD", "EUR", "CAD", "JPY", "GBP", "CHF", "AUD", "ZUSD", "ZEUR", "ZCAD", "ZJPY", "ZGBP", "ZCHF", "ZAUD"]
            val = True
            while(val):
                counter = 0
                for i in range(len(sym_real_tend)):
                    if FrontEnd.arrayify_pair[1] == sym_real_tend[i]: 
                        val = False 
                    elif FrontEnd.arrayify_pair[1] != sym_real_tend[i]:
                        counter += 1
               
                if counter == len(sym_real_tend): 
                    print(f"{c.bcolors.WARNING}Please enter a valid token symbol: {c.bcolors.ENDC}")
                    FrontEnd.arrayify_pair[1] = input()
            
            allowable_currency_pair = FrontEnd.allowable_currency_pairs()
            
            val = True
            while(val): 
                for token in allowable_currency_pair['USD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'USD': 
                        val = False; 
                    else: 
                        #print('usd')
                        continue 
                for token in allowable_currency_pair['EUR']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'EUR': 
                        val = False; 
                    else: 
                        #print('eur')
                        continue
                for token in allowable_currency_pair['CAD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'CAD': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['JPY']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'JPY': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['GBP']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'GBP': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['CHF']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'CHF': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['AUD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'AUD': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['ZUSD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZUSD': 
                        val = False; 
                    else: 
                        #print('usd')
                        continue 
                for token in allowable_currency_pair['ZEUR']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZEUR': 
                        val = False; 
                    else: 
                        #print('eur')
                        continue
                for token in allowable_currency_pair['ZCAD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZCAD': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['ZJPY']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZJPY': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['ZGBP']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZGBP': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['ZCHF']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZCHF': 
                        val = False; 
                    else: 
                        continue
                for token in allowable_currency_pair['ZAUD']:
                    if token == FrontEnd.arrayify_pair[0] and FrontEnd.arrayify_pair[1] == 'ZAUD': 
                        val = False; 
                    else: 
                        continue
                if val != False:  
                    print("Please re-enter valid currency pair")
                    FrontEnd.processing_currency_pair()    
    

    def deposit(pair, crypto_amount, real_tender_amount):
        FrontEnd.deposit_count += 1 
        trades_history = bend.get_fake_trades_history()['result']['trades']
        count = 0
        
        last_trade = {}
        
        for trade in trades_history: 
            count += 1
            trade = trades_history[trade]
            last_trade = trade
        
        last_trade["ordertxid"] = 'OQCLML-BW3P3-BUCMWZ'
        last_trade["postxid"] = 'TKH2SE-M7IF5-CFI7LT'
        last_trade['pair'] = str(pair)
        last_trade["time"] = datetime.datetime.now().timestamp() 
        last_trade['type'] = 'deposit'
        last_trade["ordertype"] = ''
        last_trade["price"] = ''
        last_trade['cost'] = str(real_tender_amount)
        last_trade["fee"] = '0.00000'
        last_trade['vol'] = str(crypto_amount)
        last_trade["margin"] = '0.00000'
        last_trade["misc"] = ''
        
        trades_history = bend.get_fake_trades_history()    

        trades_history['result']['trades']['DEPOSIT-REQUEST' + str([FrontEnd.deposit_count])] = last_trade 
        
            
        with open('tradeshistory.json', 'w') as f: 
            json.dump(trades_history, f, indent = 4)    