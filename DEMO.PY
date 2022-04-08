from os import close
import krakenex # library that is used to interact with the kraken API 
import json # Used to save/parse data that will be collected 
import time # Allows us to handle various operations regarding time i.e. no. of seconds passed since the point where time begins for some event.
import datetime # Allows us to work with a date object that conatins year, month, day, hour, minute, second and microsecond.
import calendar # Used to call specific functions to prepare calendar for data formatting based off date month and year. 


# Price threshold (percentage)
# Use of 7 decimal places. This is because percentage difference between current open price and previous closing price tends to change within this range
PRICE_THRESHOLD = 0.0000002 
# Stop loss (percentage)
STOP_LOSS = 0.0000005

def get_crypto_data(pair, since): 
    # Making a call to the API 
    # The paramater passed is the type of data that we want to query 'OPEN, HIGH, LOW AND CLOSE' which are the different price points on the chart within a certain timeframe
    # Within a given time period, we want to accumulate what the open price was, the high price (Highest price), the lowest price and the closing price. 
    # The 'data' parameter passes a currency pair variable that we will be trading with and takes in a timeframe variable of somekind.  
    return api.query_public('OHLC', data = {'pair': pair, 'since': since})['result'][pair]
    # So the API will check a 60 second window for a duration of an hour. So we will get 60 different data points which will contain:
    # The timestamp (Which doesnt have any relevance in respects to the data we will be using)
    # The opening price
    # The highest price 
    # The lowest price 
    # The closing price 
    # of each minute. 

def calcMovingAverage(data): 
    total_sum = 0 
    count = 0

    for prices in data: 
        close_ = float(prices[4])
        total_sum += close_
        count += 1

    common_average = round((total_sum / count), 5)
    return common_average

def printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair): 
    print("Current open price: ", open_)
    print("Current closing price: ", close_)
    print("Moving average: ", moving_Average)
    print("If negative, means a decrease; if postive, means an increase in the price since the last sale")
    print(f'Percentage Difference is: {str(percentage_Increase)}% since last analysis, trying again...')
    # print(f'Difference is only: {str(percentage_Decrease)}% decrease trying again...')
    print("Available", pair[0], ": ", available_crypto)
    print("Available", pair[1], ": ", available_money)

def analyze(pair, since, loop_cycle): 
    data = get_crypto_data(pair[0]+pair[1], since)

    balance = get_fake_balance() 
    #balance = get_balance() uncomment when you want to trade with real money 
    last_trade = get_last_trade(pair[0]+pair[1])

    available_crypto = float(balance['ANT'])
    available_money = float(balance['USD.HOLD'])

    if available_crypto == 0 and available_money == 0: 
        print("Do not have enough funds to make a trade") 

    if loop_cycle == 1: 
        print(f"\nAnalyzing ... {loop_cycle}st data set: \n")
    elif loop_cycle == 2: 
        print(f"\nAnalyzing ... {loop_cycle}nd data set: \n")
    elif loop_cycle == 3: 
        print(f"\nAnalyzing ... {loop_cycle}rd data set: \n")
    else:
        print(f"\nAnalyzing ... {loop_cycle}th data set: \n")

    open_ = float(data[len(data) - 1][1])
    close_ = float(data[len(data) - 2][4])


    # Calculate the % difference between the current price and the close price of the previous candle
    # If the price increased, use the formula [(New Price - Old Price)/Old Price] and then multiply that number by 100.
    percentage_Increase = (open_ - close_) / (close_ * 100)

    # If the price decreased, use the formula [(Old Price - New Price)/Old Price] and multiply that number by 100. 
    percentage_Decrease = (close_ - open_) / (close_* 100)

    moving_Average = calcMovingAverage(data)

    # open_ represents 100%, so price threshold must be split into the relevant number of parts to gain a relative percentage value in relation to the open price
    percentage_threshold_equivilant = (PRICE_THRESHOLD / open_) * 100
    percentage_stop_loss_equivilant = (STOP_LOSS / open_) * 100

    #did_sell = False # Might have to remove
    
    available_crypto = float(balance['ANT'])
    available_money = float(balance['USD.HOLD'])
    
    if available_money != 0 or available_crypto != 0: 
        # If the moving average is greater than current bid price, we can expect an upwards shift in the value of the share
        if moving_Average > open_:
            if percentage_Increase > percentage_threshold_equivilant:
                if available_money != 0: 
                    print(f'Percentage increase (1st indication): {pair[0]+pair[1]}, {percentage_Increase}%')
                    # Pause for 3 seconds to ensure the increase is sustained. Isnt just a random fluctuation. But instead, an upward trend
                    time.sleep(3)
                            
                    # calculate the difference once again. We do this to ensure the upward trend remains after the 3 second period
                    data = get_crypto_data(pair[0]+pair[1], since)
                    
                    open_ = float(data[len(data) - 1][1])
                    close_ = float(data[len(data) - 2][4])
                    
                    percentage_Increase = (open_ - close_) / (close_ * 100)

                    moving_Average = calcMovingAverage(data)
                    
                    percentage_threshold_equivilant = (PRICE_THRESHOLD / open_) * 100
                    
                    if percentage_Increase > percentage_threshold_equivilant:
                        print(f'Percentage Increase (2nd Indication): {pair[0]+pair[1]}, {percentage_Increase}%')
                        print(f'{pair[0]+pair[1]} is up {str(percentage_Increase)}% increase in the last minute opening BUY position.')
                        # Buy
                        # buy(pair[0]+pair[1], available_money, close_, last_trade)

                        close_ = float(data[len(data) - 1][4])

                        fake_buy(pair, available_money, close_, last_trade)
                            
                    else: 
                        print(f'Difference is only: {str(percentage_Increase)}% increase trying again...')
                        pass
                else: 
                    printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
                    pass
                    
                # If there is a sudden decrease in value of the share, if it is equal to or falls over our stop loss then we 'sell' quickly. 
            elif percentage_Decrease >= percentage_stop_loss_equivilant:
                available_crypto = float(balance['ANT'])
                available_money = float(balance['USD.HOLD'])

                if available_crypto != 0:
                    print(f'Percentage decrease: {pair[0]+pair[1]}, {percentage_Decrease}%')
                    print(f'{pair[0]+pair[1]} is down {str(percentage_Decrease)}% , opening SELL position.')
                    # prepare the trade request
                    # sell 
                    # sell(pair, close_, last_trade)
                    
                    close_ = float(data[len(data) - 1][4])

                    fake_sell(pair, available_crypto, close_, last_trade)
                else: 
                    printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
            else: 
                printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
                pass 
                
        # If the moving average is less than the current buy price, then we can expect a downward trend to emerge hence we want to sell whilst the share is still high in value    
        elif moving_Average < open_:
            available_crypto = float(balance['ANT'])
            available_money = float(balance['USD.HOLD'])
            if percentage_Decrease >= percentage_stop_loss_equivilant :
                if available_crypto != 0: 
                    print(f'Percentage Decrease (1st indication) : {pair[0]+pair[1]}, {percentage_Decrease}%')
                    time.sleep(4) # Pause for 4 seconds to ensure the decrease is sustained. Isnt just a random fluctuation. But instead, the begining of a downward trend
                                # We have more leverage in respects to the amount of time we can wait when the trend is going upwards as we will only be gaining profit
                                # Whereas the longer we leave time to ensure a downward trend, the more we will lose if the trend is in fact going down. 
                                # The risk associated with this is that if we do sell, and it was only a temporary fluctuation in the price, we would'nt have lost money, 
                                # but we would have lost a chance to increase our profit. 
                
                    # calculate the difference once again. We do this to ensure the downward trend remains after the 4 second period
                    data = get_crypto_data(pair[0]+pair[1], since)

                    open_ = float(data[len(data) - 1][1])
                    close_ = float(data[len(data) - 2][4])

                    percentage_Decrease = (close_ - open_) / (close_ * 100)

                    moving_Average = calcMovingAverage(data)

                    percentage_stop_loss_equivilant = (STOP_LOSS / open_) * 100

                    if percentage_Decrease >= percentage_stop_loss_equivilant:
                        print(f'Percentage Decrease (2nd Indication): {pair[0]+pair[1]}, {percentage_Decrease}%')
                        print(f'{pair[0]+pair[1]} is up {str(percentage_Decrease)}% decrease in the last 5 minutes opening SELL position.')
                    
                        # prepare the trade request

                        # sell 
                        # sell(pair, close_, last_trade)

                        close_ = float(data[len(data) - 1][4])


                        fake_sell(pair, available_crypto, close_, last_trade)
            
                    else: 
                        print(f'Difference is only: {str(percentage_Decrease)}% decrease trying again...')
                        pass 
                else: 
                    printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
                    pass
                    
            elif percentage_Increase > percentage_threshold_equivilant :
                available_crypto = float(balance['ANT'])
                available_money = float(balance['USD.HOLD'])

                if available_money != 0: 
                    print(f'Percentage increase (1st indication) : {pair[0]+pair[1]}, {percentage_Increase}%')
                    # Pause for 8 seconds to ensure the increase is sustained. Isnt just a random fluctuation. But instead, an upward trend
                    time.sleep(3)
                
                    # calculate the difference once again. We do this to ensure the upward trend remains after the 8 second period
                    data = get_crypto_data(pair[0]+pair[1], since)

                    open_ = float(data[len(data) - 1][1])
                    close_ = float(data[len(data) - 2][4])

                    percentage_Increase = (open_ - close_) / (close_* 100)

                    moving_Average = calcMovingAverage(data)

                    percentage_threshold_equivilant = (PRICE_THRESHOLD / open_) * 100

                    if percentage_Increase > percentage_threshold_equivilant:
                        print(f'Percentage Increase (2nd Indication): {pair[0]+pair[1]}, {percentage_Increase}%')
                        print(f'{pair[0]+pair[1]} is up {str(percentage_Increase)}% increase in the last 5 minutes opening BUY position.')
                        # prepare the trade request
                        # Buy
                        # buy(pair[0]+pair[1], available_money, close_, last_trade)

                        close_ = float(data[len(data) - 1][4])

                        fake_buy(pair, available_money, close_, last_trade)
                        
                    else:
                        print(f'Difference is only: {str(percentage_Increase)}% increase trying again...')
                        pass 
                else: 
                    printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
                    pass 
            else:
                printCurrentState(open_, close_, moving_Average, percentage_Increase, percentage_Decrease, available_crypto, available_money, pair)
                pass    
        else:
            print("Price is eqaul to moving average")
            pass # This is in the very unlikely case where the price is exactly equal to the moving average

    else: 
        print("Do not have enough funds to make a trade") 
        pass 


    
   
    
   
#def buy(pair, currency_type_amount, close_, last_trade): 
    #trades_history = {}
    #api.query_private('order', data) # have to find out how to make trade request 

#def sell(pair, close_, last_trade):

def fake_update_balance(pair, currency_type_amount, close_, was_sold): # if sold = true, if it was bought = false 
    balance = get_fake_balance()
    prev_balance = float(balance['USD.HOLD'])
    new_balance = 0
    if was_sold: 
        #If was sold, we will aquire a certain amount of USD based on the current price of Etherium, but if was bought, we loose our USD, but gain a given amount of Etherium based on  its current value in USD
        new_balance = prev_balance + (currency_type_amount * close_) # We times the value of crypto by the closing price to recieve the correct amount of USD back. 
        balance[pair[0]] = "0.000" # deletes old balance from balance.json 
    else: 
        new_balance = prev_balance - currency_type_amount
        balance[pair[0]] = str(float(currency_type_amount)/close_) # We divide the amount of pounds we have by the closing price of etherium to see how much etherium we have bought
    
    balance['USD.HOLD'] = str(new_balance) # updates new balance

    with open('balance.json', 'w') as f: # Writes new balance to file
        json.dump(balance, f, indent = 4)

def fake_buy(pair, currency_type_amount, close_, last_trade): 
    trades_history = get_fake_trades_history() 
    last_trade['price'] = str(close_)
    last_trade['type'] = 'buy'
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

def fake_sell(pair, currency_type_amount, close_, last_trade):
    trades_history = get_fake_trades_history() 
    last_trade['price'] = str(close_)
    last_trade['type'] = 'sell'
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
        if trade['pair'] == pair and trade['type'] == 'buy': 
            last_trade = trade
    
    return last_trade 


def get_fake_trades_history(): 
    with open('tradeshistory.json', 'r') as f: 
        return json.load(f)

def get_trades_history(): 
    start_date = datetime.datetime(2021, 8, 3) # YY-MM-DD
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

if __name__ == '__main__': 
    api = krakenex.API() # instatiation of krakenex library/connects to the kraken API 
    api.load_key('kraken.key') # The loadkey function allows us to load our API keys and access the data specific to the account made on kraken
                               # Here, we input the .KEY file as a parameter within the load_key function that stores both the API KEY and private key 
    pair = ("ANT", "USD") # Currency pair
    since = str(int(time.time() -  3600)) # Requires edit, uses 3600 seconds which is equivilant to an hour whereas I want to know the buy sell operations from the past day 
    
    loop_cycle = 1
    
    while True: 
        analyze(pair, since, loop_cycle)
        loop_cycle += 1 
        time.sleep(1) # Anything faster than this will cause the API to produce Key Error: 'result' to prevent DDOS attack/manipulation of the direction in the market. 
        if loop_cycle == 9: # First rate limit will be reached when loop hits 9th gathering of trades history (OHLC), 
                            # 60 different data points. 'while' loop occurs 9 times thus 60 data points * 9 = 540 new opening and closing prices every time we loop through data 

            print("\nRegenerating rate limit points for starter account:\n")
            countdown(46)  # This is placed here once we exceed our rate limit of 15 points due to API Endpoint requests i.e. TradesHistory(+2), Balance(+1)
                           # Each second passed gives a reduction of -0.33 points thus (1 request per second * TradesHistory increases counter by 2 each time, 
                           # thus on the 9th request of OHLC data, we go above our counter limit and hit 18 points). 15 points/-0.33 == 54.54 seconds thus, 
                           # I have rounded to 46 seconds as the countdown function uses the divmod() function which requires a whole number of seconds/minutes. 
                           # Divide the remaining no. of points by 0.33 to get no.of seconds you have to wait to set rate limit back to 0. 
            loop_cycle = 1
            
    
    
    
    
    # Tests that were conducted: 
    # Comprised of testing result of various methods by outputing inot string format using json.dumps()
    # keyerro: 'result' 

    # since = str(int(time.time() - 86,400)) # This is a timestamp of 86400 seconds which equates to a day. 
    #print(json.dumps(get_crypto_data(pair[0]+pair[1], since), indent=4)) # json.dumps will convert the python object into a string. The indent parameter is used to to indent each line by 4 spaces, this makes the data that we accumulate tidy and easier to read.
    #print(get_balance())
    #print(json.dumps(get_trades_history(), indent=4))
    #print(json.dumps(get_fake_balance(), indent=4))
    #print(json.dumps(get_fake_trades_history(), indent=4))
    #print(json.dumps(get_crypto_data(pair[0]+pair[1], since), indent=4))
    #print(json.dumps(get_fake_trades_history(), indent=4))

    """print(f"{get_crypto_data(pair[0]+pair[1], since)}")

    key = 'result'

    if key in get_crypto_data(pair[0]+pair[1], since): 
        print(f"'{key}' exists")
    else: 
        print(f"'{key}' does not exist")"""
    
        
    #https://support.kraken.com/hc/en-us/articles/206548367-What-is-the-API-call-rate-limit-

    #https://support.kraken.com/hc/en-us/articles/360045239571-Trading-rate-limits

    #First rate limit will be reached when loop hits 9th gathering of trades history: 2(counter increase)*9(iteration)-0.33(Counter decrease per second)*(No.of seconds you are willing to wait to reduce counter)
