import krakenex
import json # Used to save/parse data that will be collected 
import time # Allows us to handle various operations regarding time i.e. no. of seconds passed since the point where time begins for some event.
import datetime # Allows us to work with a date object that conatins year, month, day, hour, minute, second and microsecond.
import calendar # Used to call specific functions to prepare calendar for data formatting based off date month and year. 
import colorama 

import StatisticalModels as sms
import colors as c

colorama.init()

def get_crypto_data(pair, since, api): 
    # Making a call to the API 
    # The paramater passed is the type of data that we want to query 'OPEN, HIGH, LOW AND CLOSE' which are the different price points on the chart within a certain timeframe
    # Within a given time period, we want to accumulate what the open price was, the high price (Highest price), the lowest price and the closing price. 
    # The 'data' parameter passes a currency pair variable that we will be trading with and takes in a timeframe variable of somekind.  
    #print(pair)
    try:
        return api.query_public('OHLC', data = {'pair': pair, 'since': since})['result'][pair]
    except: 
        #print(pair)
        api = krakenex.API() # instatiation of krakenex library to re-connect to the kraken API 
                             # in case of unexepcted connection failure. 
        api.load_key('kraken.key')
        return api.query_public('OHLC', data = {'pair': pair, 'since': since})['result'][pair]

    # So the API will check a 60 second window for a duration of an hour. So we will get 60 different data points which will contain:
    # The timestamp (Which doesnt have any relevance in respects to the data we will be using)
    # The opening price
    # The highest price 
    # The lowest price 
    # The closing price 
    # of each minute.     

def printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r): 
    print(f"{c.bcolors.HACKER_GREEN}Current open price: {c.bcolors.ENDC}", open_)
    print(f"{c.bcolors.HACKER_GREEN}Previous closing price: {c.bcolors.ENDC}", close_)
    print(f"{c.bcolors.HACKER_GREEN}Simple moving average: {c.bcolors.ENDC}", simple_Moving_Average)
    print(f"{c.bcolors.HACKER_GREEN}EWMA: {c.bcolors.ENDC}", simple_Moving_Average)
    print(f"{c.bcolors.HACKER_GREEN}Standard Deviation: {c.bcolors.ENDC}", standard_deviation)
    print(f"{c.bcolors.HACKER_GREEN}Bollinger Bands: [{c.bcolors.ENDC}upperbounds{c.bcolors.HACKER_GREEN}]: {c.bcolors.ENDC}" + bollinger_bands[0] + f" {c.bcolors.HACKER_GREEN}[{c.bcolors.ENDC}lowerbounds{c.bcolors.HACKER_GREEN}]: {c.bcolors.ENDC}" + bollinger_bands[1])
    print(f"{c.bcolors.HACKER_GREEN}Parabolic SAR: ", Parabolic_SAR)
    print(f"{c.bcolors.HACKER_GREEN}RSI: {c.bcolors.ENDC}", RSI)
    print(f"{c.bcolors.HACKER_GREEN}ADX: {c.bcolors.ENDC}", ADX)
    print(f"{c.bcolors.HACKER_GREEN}Williams %R: {c.bcolors.ENDC}", williams_r)
    print(f"{c.bcolors.HACKER_GREEN}If negative, means a decrease; if postive, means an increase in the price since the last sale")
    print(f"{c.bcolors.HACKER_GREEN}Percentage Difference is: {c.bcolors.ENDC}{str(percentage_Increase)}%{c.bcolors.HACKER_GREEN} since last analysis, trying again...")


def analyze(pair, since, PRICE_THRESHOLD, STOP_LOSS, api, loop_cycle, time_in_seconds): 
    # https://www.codegrepper.com/code-examples/python/colorama+bug+when+trying+to+change+colour+rapidly+python
    data = get_crypto_data(pair[0]+pair[1], since, api)    

    balance = get_fake_balance() 
    #balance = get_balance() uncomment when you want to trade with real money 
    last_trade = get_last_trade(pair[0]+pair[1])     

    if loop_cycle == 1: 
        print(f"{c.bcolors.HACKER_GREEN}\nAnalyzing ... {c.bcolors.ENDC}{loop_cycle}st{c.bcolors.HACKER_GREEN} data set: \n{c.bcolors.ENDC}")
    elif loop_cycle == 2: 
        print(f"\n{c.bcolors.HACKER_GREEN}Analyzing ... {c.bcolors.ENDC}{loop_cycle}nd{c.bcolors.HACKER_GREEN} data set: \n{c.bcolors.ENDC}")
    elif loop_cycle == 3: 
        print(f"\n{c.bcolors.HACKER_GREEN}Analyzing ... {c.bcolors.ENDC}{loop_cycle}rd{c.bcolors.HACKER_GREEN} data set: \n{c.bcolors.ENDC}")
    else:
        print(f"\n{c.bcolors.HACKER_GREEN}Analyzing ... {c.bcolors.ENDC}{loop_cycle}th{c.bcolors.HACKER_GREEN} data set: \n{c.bcolors.ENDC}")    

    open_ = float(data[len(data) - 1][1]) # most recent opening price
    close_ = float(data[len(data) - 2][4]) # previous closing price    

    price_difference = open_ - close_
    #print(len(data)) #Not too sure why downloads +1 data point after 9 analyzed data sets which is the point at which a regeneration of counters occurs 
    #before next consecutive run of data.    

    percentage_Increase = sms.calcPercentageIncrease(open_, close_)   
    percentage_Decrease = sms.calcPercentageDecrease(open_, close_)    
    simple_Moving_Average = sms.calcSimpleMovingAverage(data)    
    EWMA = sms.exponentially_weighted_moving_average(data, time_in_seconds)
    standard_deviation = sms.calcStandardDeviation(data)
    bollinger_bands = sms.store_upper_and_lower_bounds(data)
    RSI = sms.relative_strength_index(data, time_in_seconds)
    ADX = sms.ADX(data)
    Parabolic_SAR = sms.parabolic_SAR(data)
    williams_r = sms.williams_perecntile_R(data, time_in_seconds)
    
    #Used to create graphs of trading environemnt from however long back the timestamp has been set
    #sms.graph_representations_of_indicators(data, time_in_seconds)

    # open_ represents 100%, so price threshold must be split into the relevant number of parts to gain a relative percentage value in relation to the open price
    # We convert STOP_LOSS AND PERCENTAGE_THRESHOLD into a percentage value in relation to the open price so we can comapare them with the percentage increase/decrease
    # since the previous closing price. Effectively a form of normalization. 

    percentage_threshold_equivilant = (PRICE_THRESHOLD / open_) * 100
    percentage_stop_loss_equivilant = (STOP_LOSS / open_) * 100    

    available_crypto = float(balance[pair[0]])
    available_money = float(balance[pair[1]])
    
    # Trading strategy (# Psudeocode): 
    # General rule of thumb, you want your PERCENTAGE INCREASE to be larger than your STOP LOSS
    # This is so that when you SELL on an increase, this compenesates for any losses aquired due 
    # to a sudden decrease in the price of a given token. 
    # ----------------------------------------------------------------------
    # First comparisons accounts for sudden change in price
    # ----------------------------------------------------------------------
    # Current open > moving average 
      # and if previous close > lowerbound and < mean [return 1] 
       # and if percentage increase > price threshold equivilant - [we sell]
       #suggests sudden increase in the price of the token 

    # Current open < moving average
      # and if previous close < upperbound and greater than mean - [we buy]
      #and if percentage decrease > percentage stop loss equivilant
      #suggests sudden decrease in the price of the token
    # ----------------------------------------------------------------------
    # Second comparisons accounts for micro changes in the price 
    # ----------------------------------------------------------------------
    # Current open > moving average 
        # and if previous close < upperbound and > mean 
          # and percentage_Increase > percentage_threshold_equivilant - [we sell]
          # else if percentage_Decrease >= percentage_stop_loss_equivilant - [we buy] 
          # accounts for changes above the mean and below the upperbound
    
    # Current open < moving average 
        # and previous close > lowerbound < mean 
          # and percentage_Increase > percentage threshold equivilant - [we sell]
          # else if percentage_Decrease >= percentage stop_loss equivilant - [we buy]
          # accounts for changes below the mean and above ther lowerbound
    # --------------------------------------------------------------------------------
    # Third comparisons compare whether previous closing prices within bollinger bands
    # --------------------------------------------------------------------------------
       # close greater than or equal to upperbound
       # [we sell]
       # close less than or equal to lowerbound 
       # [we buy]
    # --------------------------------------------------------------------------------
    #  Fourth comparisons compare conditions when open is equal to moving average
    # --------------------------------------------------------------------------------
    # Moving average equal to open 
      # and open is equal to previous close 
      # output current state of market

    # Moving average equal to open 
      # and open is not equal to previous close
      # Depenedant on the change in the price of the token will result in either a buy or a sale event
    # --------------------------------------------------------------------------------
    #  Last condition produces a warning error in the case a condition falls out of 
    #  scope of current logic of trading strategy
    # --------------------------------------------------------------------------------
    
    if  open_ > EWMA and sms.calcBollingerBands(data, pair[0], pair[1]) == 1: 
        print("[open_ > EWMA")
        print(" Previous close > lowerbound < mean]  \n")
        sell_On_Increase(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, available_money, available_crypto, last_trade, time_in_seconds)
    elif open_ < EWMA and sms.calcBollingerBands(data, pair[0], pair[1]) == 0:
        print("[open_ < EWMA")
        print(" Previous < than upperbound > mean] \n")
        buy_On_Decrease(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, STOP_LOSS, available_money, last_trade, time_in_seconds)
    elif open_ < EWMA and sms.calcBollingerBands(data, pair[0], pair[1]) == 1:
        print("[open_ < EWMA")
        print(" Previous close > lowerbound < mean] \n")
        combinational_buy_sell(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, STOP_LOSS, available_money, available_crypto, last_trade, time_in_seconds)   
    elif open_ > EWMA and sms.calcBollingerBands(data, pair[0], pair[1]) == 0:
        print("[open_ > EWMA")
        print(" Previous < than upperbound > mean]  \n")
        combinational_buy_sell(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, STOP_LOSS, available_money, available_crypto, last_trade, time_in_seconds)
    elif sms.calcBollingerBands(data, pair[0], pair[1]) == 2: 
        print("[Close greater than upperbound]")
        fake_sell(pair, available_crypto, close_, last_trade)
    elif sms.calcBollingerBands(data, pair[0], pair[1]) == 3:
        print("[Close less than lowerbound]") 
        fake_buy(pair, available_money, close_, last_trade)
    elif open_ == EWMA and open_ == close_:
        print("[EWMA == open")
        print(" open_ == previous close")
        print(" No change in price since previous anaylsis]")
        printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)
    elif open_ == EWMA and open_ != close_:
        print("[EWMA == open")
        print(" Open != close]") 
        combinational_buy_sell(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, STOP_LOSS, available_money, available_crypto, last_trade, time_in_seconds)
    elif open_ != EWMA and open_ == close_: 
        print("[EWMA != open")
        print(" Open == close]")
        print(" No change in price since previous anaylsis]")
        printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)
    else: 
        print(f"{c.bcolors.WARNING}[Unknown condition outside the scope of trading strategy has been triggered]{c.bcolors.ENDC}")
        printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)
              
    return loop_cycle
    

def sell_On_Increase(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, available_money, available_crypto, last_trade, time_in_seconds):
    if available_crypto != 0: 
        #if percentage_Increase > percentage_threshold_equivilant:
        if price_difference > PRICE_THRESHOLD:
            print(f'{c.bcolors.HACKER_GREEN}Percentage increase {c.bcolors.ENDC}(1st indication): {pair[0]+pair[1]}, {percentage_Increase}%')
            # Pause for 3 seconds to ensure the increase is sustained. Isnt just a random fluctuation. But instead, an upward trend
            time.sleep(3)
                    
            # calculate the difference once again. We do this to ensure the upward trend remains after the 3 second period

            loop_cycle += 1 # This has been put in place to account for the counter increase upon re-downloading trading data. Price of crypto tends to remain constant thus the number of loops
                            # before regeneration has been set to '9', but this only takes into the account that the analyze method calls for data once per loop cycle. 
                            # Thus we skip a loop cycle in the instance the the pirce of a token has increase/decreased to prevent denied access to request for data which otherwise cause a runtime error.

            data = get_crypto_data(pair[0]+pair[1], since, api) 
            
            open_ = float(data[len(data) - 1][1])
            close_ = float(data[len(data) - 2][4])    

            percentage_Increase = sms.calcPercentageIncrease(open_, close_)

            EWMA = sms.exponentially_weighted_moving_average(data, time_in_seconds) 

            price_difference = open_ - close_

            #if percentage_Increase > percentage_threshold_equivilant:
            if price_difference > PRICE_THRESHOLD:
                print(f'{c.bcolors.HACKER_GREEN}Percentage Increase {c.bcolors.ENDC}(2nd Indication): {pair[0]+pair[1]}, {percentage_Increase}%')
                print(f'{pair[0]+pair[1]} is up {str(percentage_Increase)}% increase in the last minute, opening SELL position.')
                
                close_ = float(data[len(data) - 1][4])

                # prepare the trade request

                # sell 
                # sell(pair, close_, last_trade)
                 
                fake_sell(pair, available_crypto, close_, last_trade)    
            else: 
                print(f'Difference is only: {str(percentage_Increase)}% increase trying again...')
        else: 
            printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)
    else: 
        printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)


def buy_On_Decrease(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, STOP_LOSS, available_money, last_trade, time_in_seconds):
    if available_money != 0:
        #if percentage_Decrease < percentage_stop_loss_equivilant :
        if price_difference < STOP_LOSS:
            print(f'Percentage Decrease (1st indication) : {pair[0]+pair[1]}, {percentage_Decrease}%')
            time.sleep(3) # Pause for 3 seconds to ensure the decrease is sustained. Isnt just a random fluctuation. But instead, the beginning of a downward trend
                          # We have more leverage in respects to the amount of time we can wait when the trend is going upwards as we will only be gaining profit
                          # Whereas the longer we leave time to ensure a downward trend, the more we will lose if the trend is in fact going down. 
                          # The risk associated with this is that if we do sell, and it was only a temporary fluctuation in the price, we would'nt have lost money, 
                          # but we would have lost a chance to increase our profit. 
                
            # calculate the difference once again. We do this to ensure the downward trend remains after the 3 second period
            loop_cycle += 1
            data = get_crypto_data(pair[0]+pair[1], since, api)    

            open_ = float(data[len(data) - 1][1])
            close_ = float(data[len(data) - 2][4])    

            percentage_Increase = sms.calcPercentageIncrease(open_, close_)

            percentage_Decrease = sms.calcPercentageDecrease(open_, close_) 

            EWMA = sms.exponentially_weighted_moving_average(data, time_in_seconds)    

            price_difference = open_ - close_

            #if percentage_Decrease < percentage_stop_loss_equivilant:
            if price_difference < STOP_LOSS:
                print(f'Percentage Decrease (2nd Indication): {pair[0]+pair[1]}, {percentage_Decrease}%')
                print(f'{pair[0]+pair[1]} is up {str(percentage_Decrease)}% decrease in the last 5 minutes opening SELL position.')
            
                close_ = float(data[len(data) - 1][4])   
                
                # prepare the trade request

                # Buy 
                # buy(pair[0]+pair[1], available_money, close_, last_trade) 

                fake_buy(pair, available_money, close_, last_trade)
            
            else: 
                print(f'Difference is only: {str(percentage_Decrease)}% decrease trying again...')
        else: 
            printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)
    else: 
        printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)


def combinational_buy_sell(pair, since, api, open_, close_, loop_cycle, simple_Moving_Average, price_difference, percentage_Increase, percentage_Decrease, standard_deviation, bollinger_bands, EWMA, Parabolic_SAR, RSI, ADX, williams_r, PRICE_THRESHOLD, STOP_LOSS, available_money, available_crypto, last_trade, time_in_seconds): 
    if available_crypto != 0: 
        #if percentage_Increase > percentage_threshold_equivilant:
        if price_difference > PRICE_THRESHOLD:
            print(f'Percentage increase (1st indication): {pair[0]+pair[1]}, {percentage_Increase}%')
            # Pause for 3 seconds to ensure the increase is sustained. Isnt just a random fluctuation. But instead, an upward trend
            time.sleep(3)
            
            loop_cycle += 1

            # calculate the difference once again. We do this to ensure the upward trend remains after the 3 second period
            data = get_crypto_data(pair[0]+pair[1], since, api)
            
            open_ = float(data[len(data) - 1][1])
            close_ = float(data[len(data) - 2][4])    

            percentage_Increase = sms.calcPercentageIncrease(open_, close_)

            percentage_Decrease = sms.calcPercentageDecrease(open_, close_) 

            EWMA = sms.exponentially_weighted_moving_average(data, time_in_seconds)
 

            price_difference = open_ - close_

            #if percentage_Increase > percentage_threshold_equivilant:
            if price_difference > PRICE_THRESHOLD:
                print(f'Percentage Increase (2nd Indication): {pair[0]+pair[1]}, {percentage_Increase}%')
                print(f'{pair[0]+pair[1]} is up {str(percentage_Increase)}% increase in the last minute, opening SELL position.')
                
                close_ = float(data[len(data) - 1][4])

                # prepare the trade request

                # sell 
                # sell(pair, close_, last_trade)
                 
                fake_sell(pair, available_crypto, close_, last_trade)
                    
            else: 
                print(f'Difference is only: {str(percentage_Increase)}% increase trying again...')
        else: 
            printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)

    elif available_money != 0: 
        #if percentage_Decrease < percentage_stop_loss_equivilant :
        if price_difference < STOP_LOSS:
            print(f'Percentage Decrease (1st indication) : {pair[0]+pair[1]}, {percentage_Decrease}%')
            time.sleep(3) # Pause for 3 seconds to ensure the decrease is sustained. Isnt just a random fluctuation. But instead, the begining of a downward trend
                          # We have more leverage in respects to the amount of time we can wait when the trend is going upwards as we will only be gaining profit
                          # Whereas the longer we leave time to ensure a downward trend, the more we will lose if the trend is in fact going down. 
                          # The risk associated with this is that if we do sell, and it was only a temporary fluctuation in the price, we would'nt have lost money, 
                          # but we would have lost a chance to increase our profit. 
                
            # calculate the difference once again. We do this to ensure the downward trend remains after the 4 second period

            loop_cycle += 1

            data = get_crypto_data(pair[0]+pair[1], since, api)    

            open_ = float(data[len(data) - 1][1])
            close_ = float(data[len(data) - 2][4])    

            percentage_Increase = sms.calcPercentageIncrease(open_, close_)

            percentage_Decrease = sms.calcPercentageDecrease(open_, close_) 

            EWMA = sms.exponentially_weighted_moving_average(data, time_in_seconds)  

            price_difference = open_ - close_

            #if percentage_Decrease < percentage_stop_loss_equivilant:
            if price_difference < STOP_LOSS: 
                print(f'Percentage Decrease (2nd Indication): {pair[0]+pair[1]}, {percentage_Decrease}%')
                print(f'{pair[0]+pair[1]} is up {str(percentage_Decrease)}% decrease in the last 5 minutes opening SELL position.')
            
                close_ = float(data[len(data) - 1][4])   
                
                # prepare the trade request

                # Buy 
                # buy(pair[0]+pair[1], available_money, close_, last_trade) 

                fake_buy(pair, available_money, close_, last_trade)
            
            else: 
                print(f'Difference is only: {str(percentage_Decrease)}% decrease trying again...')
        else: 
            printCurrentState(open_, close_, simple_Moving_Average, standard_deviation, bollinger_bands, percentage_Increase, EWMA, Parabolic_SAR, RSI, ADX, williams_r)


def fake_update_balance(pair, currency_type_amount, close_, was_sold): # if sold = true, if it was bought = false 
    balance = get_fake_balance()
    prev_balance = float(balance[pair[1]])
    new_balance = 0
    if was_sold: 
        #If was sold, we will aquire a certain amount of USD based on the current price of Etherium, but if was bought, we loose our USD, but gain a given amount of Etherium based on  its current value in USD
        new_balance = prev_balance + (currency_type_amount * close_) # We times the value of crypto by the closing price to recieve the correct amount of USD back. 
        balance[pair[0]] = "0.000" # deletes old balance from balance.json 
    else: 
        new_balance = prev_balance - currency_type_amount
        balance[pair[0]] = str(float(balance[pair[0]]) + float(currency_type_amount / close_)) # We divide the amount of pounds we have by the closing price of a given token to see how much of the token we have bought
    
    balance[pair[1]] = str(new_balance) # updates new balance    

    with open('balance.json', 'w') as f: # Writes new balance to file
        json.dump(balance, f, indent = 4)    


#def buy(pair, currency_type_amount, close_, last_trade): 
    #trades_history = {}
    #api.query_private('order', data) # have to find out how to make trade request     

   
def fake_buy(pair, currency_type_amount, close_, last_trade): 
    trades_history = get_fake_trades_history() 
    last_trade['pair'] = str(pair[0] + pair[1])
    last_trade['price'] = str(close_)
    last_trade['type'] = 'buy'
    last_trade['ordertype'] = 'limit'
    last_trade['cost'] = currency_type_amount
    last_trade['time'] = datetime.datetime.now().timestamp()
    last_trade['vol'] = str(float(currency_type_amount)/close_) # Calculates how much crypto was actually bought i.e. market prices show the amount it cost for 1 Eutherium
                                                                # Whereas we will only buy based off the amount we have (limit order)
    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade # Here, we are adding a new trade    

    print("\n")
    print("Currency pair: ", last_trade['pair'])
    print("Price: ", last_trade['price'])
    print("Type: ", last_trade['type'])
    print("Cost: ", last_trade['cost'])
    print(f"Time of {last_trade['type']}:", last_trade['time'])
    print("Vol: ", last_trade['vol'])
    print("\n")    

    with open('tradeshistory.json', 'w') as f: 
        json.dump(trades_history, f, indent = 4)
        fake_update_balance(pair, currency_type_amount, close_, False)    

#def sell(pair, close_, last_trade): 

def fake_sell(pair, currency_type_amount, close_, last_trade):
    trades_history = get_fake_trades_history() 
    last_trade['pair'] = str(pair[0] + pair[1])
    last_trade['price'] = str(close_)
    last_trade['type'] = 'sell'
    last_trade['ordertype'] = 'limit'
    last_trade['cost'] = str(float(last_trade['vol'])*close_) # Calculates the the cost in pounds if we sell 
    last_trade['time'] = datetime.datetime.now().timestamp()    

    trades_history['result']['trades'][str(datetime.datetime.now().timestamp())] = last_trade    

    print("\n")
    print("Currency pair: ", last_trade['pair'])
    print("Price: ", last_trade['price'])
    print("Type: ", last_trade['type'])
    print("Cost: ", last_trade['cost'])
    print(f"Time of {last_trade['type']}:", last_trade['time'])
    print("Vol: ", last_trade['vol'])
    print("\n")    

    with open('tradeshistory.json', 'w') as f: 
        json.dump(trades_history, f, indent = 4)
        fake_update_balance(pair, currency_type_amount, close_, True)    


#def get_balance(): 
    #return api.query_private('Balance') #['result'] remove comment once you have money in your account as produces an error message    

def get_fake_balance(): 
    with open('balance.json', 'r') as f: 
        return json.load(f)    


def get_last_trade(pair): 
    trades_history = get_fake_trades_history()['result']['trades']
    #trades_history = get_trades_history()
    
    last_trade = {}    

    for trade in trades_history: 
        trade = trades_history[trade]
        #if trade['pair'] == pair and trade['type'] == 'buy' or trade['pair'] == pair and trade['type'] == 'deposit': 
        last_trade = trade
    
    return last_trade     


def get_fake_trades_history(): 
    with open('tradeshistory.json', 'r') as f: 
        return json.load(f)    

def get_currency_symbols(): 
    with open('currency_pair.json', 'r') as f: 
        return json.load(f)   

def get_trades_history(api): 
    start_date = datetime.datetime(2022, 2, 17) # YY-MM-DD
    end_date = datetime.datetime.today() 
    return api.query_private('TradesHistory', req(start_date, end_date, 1))['result']['trades'] # Gets all our trading history from a certain start date, to a certain end date.     

def date_nix(str_date):
    return calendar.timegm(str_date.timetuple()) # Formats dates in a way in which the API processes them. i.e. Different formatting methods i.e. the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds    

def req(start, end, ofs):
    req_data = {
        'type': 'all', # Type of trade. So 'all' implies all positions 
        'trades': 'true', # Includes trades related to position in output 
        'start': str(date_nix(start)), # Starting unix timestamp or trade tx ID of results (Exclusive)
        'end': str(date_nix(end)), # Ending unix timestamp or trade tx ID of results (Inclusive)
        'ofs': str(ofs) # Result offset for pagination 
    }
    return req_data
