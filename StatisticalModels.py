import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import talib
from sklearn.preprocessing import StandardScaler
from sklearn import svm

def calcPercentageIncrease(open_, close_): 
    # Calculate the % difference between the current price and the close price of the previous candle
    # If the price increased, use the formula [(New Price - Old Price)/Old Price] and then multiply that number by 100.
    percentage_Increase = (open_ - close_) / (close_ * 100)
    return percentage_Increase
 
def calcPercentageDecrease(open_, close_): 
    # If the price decreased, use the formula [(Old Price - New Price)/Old Price] and multiply that number by 100. 
    percentage_Decrease = (close_ - open_) / (close_* 100)
    return percentage_Decrease

def calcSimpleMovingAverage(data): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    close_ = pd.to_numeric(dataset[4])
    ma = close_.rolling(2, min_periods=1).mean()
    return ma[len(ma) - 1] # returns most recent ma

def calcStandardDeviation(data): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    close_ = pd.to_numeric(dataset[4])
    std = close_.rolling(window=2).std().fillna(method='bfill').fillna(method='ffill')
    return std[len(std) - 1] # returns most recent std
    
# Places more weight on most recent averages in repsects to intervals between the TIMESTAMP set. 
def exponentially_weighted_moving_average(data, time_in_seconds): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    close_ = pd.to_numeric(dataset[4])
    # 86400 equivilant to 1 day. Windows/spans will only accept 1 day as lowest input
    if time_in_seconds > 86400: 
       no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
       ewma = close_.ewm(span=12 + no_of_days).mean() # span with periods in days. 
    else:
       ewma = close_.ewm(span=12).mean() 

    return ewma[len(ewma) - 1] # returns most recent ewma

def calcBollingerBands(data, crypto_symbol, real_tender):
    # Whenever the asset crosses the upper boundary, it is time to sell, and similarly, when the asset crosses the lower boundary, it is time to buy.
    # https://blog.finxter.com/bollinger-bands-algorithm-python-binance-api-for-crypto-trading/
    # https://codingandfun.com/bollinger-bands-pyt/

    # converts the API response dictionary into a Pandas DataFrame using the Pandas from_dict() method
    pricesOfCrypto = pd.DataFrame.from_dict(data)
    #pricesOfCrypto = pricesOfCrypto.set_index(0) # is the timestamp column

    #print(pricesOfCrypto)

    pricesOfCrypto.insert(7, 8, pricesOfCrypto[4].rolling(2, min_periods=1).mean()) # where 8 is 'mean' 
    pricesOfCrypto.insert(8, 9, pricesOfCrypto[4].rolling(2, min_periods=1).std()) # where 9 is 'std (standard deviation)'

    upperbound = pricesOfCrypto[8] + (pricesOfCrypto[9] * 2)
    lowerbound = pricesOfCrypto[8] - (pricesOfCrypto[9] * 2)

    pricesOfCrypto.insert(9, 10, upperbound) # where 10 is the upperbound 
    pricesOfCrypto.insert(10, 11, lowerbound) # and 11 is the lower bound

    #pricesOfCrypto[[4, 8, 10, 11]].plot(figsize=(10,6))
    
    #plt.grid(True)
    #plt.title(crypto_symbol + "vs" + real_tender + "Bollinger Bands")
    #plt.axis('tight')
    #plt.xlabel('no. of data point (60 closing prices per hour)')
    #plt.ylabel('Price')
    #plt.savefig('ANTvsUSD.png')
    #plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)


    #print(pricesOfCrypto.iloc[0:, 0:1])
    #print(pricesOfCrypto.iloc[0:, 4:5])
    #print(len(pricesOfCrypto) - 2)
    #print(pricesOfCrypto)

    #Dateframe requires iloc to be used so we can specify index within the data 

    #print(pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 10:11]) 
    #print(pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 9:10]) 

    # i is short for indexed 
    iupperbound = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 9:10] # upperbound value in relation to previous closing price [58:59, 9:10]
    ilowerbound = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 10:11] # lowerbound value in relation to previous closing price [58:59, 10:11]
    ipreviousclose = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 4:5] # [0: previous close, 4:5 (close column)]

    #print(ilowerbound)
    #print(iupperbound)
    #print(ipreviousclose)
    #print(ipreviousclose[4][58])
    #print(ipreviousclose[4][58])
    #print(ipreviousclose[4][58])

    # disecting values stored within the frame from 3 dimensions to 1. Where the three dimensions are the rows, columns and the value itself. 
    arrayify = []

    # Length may change due to unknown increase in the number of rows within the frame after each regernetaion of counters, hence we have not used i.e. [10][58] row. 
    # Future proofing in the instance the issue cannot be resolved. Does not affect the outcome when triggering conditions to place buy/sell events. 
    # Specifying index will range from 0 - 2 when wanting to perform logical comparison between previous closing price and upper/lower bounds. 
    arrayify.append(iupperbound[10][len(pricesOfCrypto) - 2]) # index 0 of array is 'upperbound' 
    arrayify.append(ilowerbound[11][len(pricesOfCrypto) - 2]) # index 1 of array is 'ilowerbound' 
    arrayify.append(ipreviousclose[4][len(pricesOfCrypto) - 2]) # index 2 is 'previous closing price of array) 

    #print(arrayify)

    if float(arrayify[2]) < float(arrayify[0]) and float(arrayify[2]) > calcSimpleMovingAverage(data): # previous close less than upperbound and greater than mean 
        return 0
    elif float(arrayify[2]) > float(arrayify[1]) and float(arrayify[2]) < calcSimpleMovingAverage(data): # previous close greater than lowerbound and less than mean 
        return 1
    elif float(arrayify[2]) > float(arrayify[0]): # close greater than upperbound
        return 2
    elif float(arrayify[2]) < float(arrayify[1]): # close less than lowerbound
        return 3

def store_upper_and_lower_bounds(data):
    # converts the API response dictionary into a Pandas DataFrame using the Pandas from_dict() method

    pricesOfCrypto = pd.DataFrame.from_dict(data)
    #pricesOfCrypto = pricesOfCrypto.set_index(0) # is the timestamp column

    #print(pricesOfCrypto)

    pricesOfCrypto.insert(7, 8, pricesOfCrypto[4].rolling(2, min_periods=1).mean()) # where 8 is 'mean' 
    pricesOfCrypto.insert(8, 9, pricesOfCrypto[4].rolling(2, min_periods=1).std()) #where 9 is 'std (standard deviation)'

    upperbound = pricesOfCrypto[8] + (pricesOfCrypto[9] * 2)
    lowerbound = pricesOfCrypto[8] - (pricesOfCrypto[9] * 2)

    pricesOfCrypto.insert(9, 10, upperbound) # where 10 is the upperbound 
    pricesOfCrypto.insert(10, 11, lowerbound) # and 11 is the lower bound

    iupperbound = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 9:10] # upperbound value in relation to previous closing price [58:59, 9:10]
    ilowerbound = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 10:11] # lowerbound value in relation to previous closing price [58:59, 10:11]
    ipreviousclose = pricesOfCrypto.iloc[len(pricesOfCrypto) - 2:len(pricesOfCrypto) - 1, 4:5] # [0: previous close, 4:5 (close column)]

        # disecting values stored within the frame from 3 dimensions to 1. Where the three dimensions are the rows, columns and the value itself. 
    arrayify = []

    upperbound_formatted = "{:.5f}".format(iupperbound[10][len(pricesOfCrypto) - 2])
    lowerbound_formatted = "{:.5f}".format(ilowerbound[11][len(pricesOfCrypto) - 2])
    
    # Length may change due to unknown increase in the number of rows within the frame after each regernetaion of counters, hence we have not used i.e. [10][58] row. 
    # Future proofing in the instance the issue cannot be resolved. Does not affect the outcome when triggering conditions to place buy/sell events. 
    # Specifying index will range from 0 - 2 when wanting to perform logical comparison between previous closing price and upper/lower bounds. 
    arrayify.append(str(upperbound_formatted)) # index 0 of array is 'upperbound' 
    arrayify.append(str(lowerbound_formatted)) # index 1 of array is 'lowerbound' 
    arrayify.append(str(ipreviousclose[4][len(pricesOfCrypto) - 2])) # index 2 is 'previous closing price of array) 
    
    #time.sleep(0.5) # Put in place to prevent 'float' object from being non-subscriptable

    return arrayify

 
# RSI is an oscillator indicator, with a range between 0 to 100.
# When markets have reached an oversold condition it may indicate 
# that the move has reached an exhaustion point and a reversal could
# be at hand. If the RSI reading is below 20 and rising then 
# is a potential signal to see the market reverse and start trading higher.

# On the other hand, when we see situations where the market has rallied and the RSI has
# reached above 80 and then starts to fall, we may see a situation where the market could 
# reverse and head lower.
def relative_strength_index(data, time_in_seconds): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    close_ = pd.to_numeric(dataset[4])
    # 1209600 equivilant to 14 days. Windows/spans will only accept 1 day as minumum input   
    if time_in_seconds > 1209600: 
        no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
        rsi = talib.RSI(close_.values, timeperiod = no_of_days) # recommended to set to 14 days 
    else: 
         rsi = talib.RSI(close_.values, timeperiod = 14) # recommended to set to 14 days 
         #rsi = rsi.fillna(method='bfill').fillna(method='ffill')
    
    return rsi[len(rsi) - 1] # returns most recent strength index

# Momentum Indicator as well as an Oscillator, between -100 and 0
# reading above -20 is usually considered overbought.
# reading below -80 is usually considered oversold.
# tells us where the current price is relative to the highest high over the last TIMESTAMP period
def williams_perecntile_R(data, time_in_seconds): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])
    # 1209600 equivilant to 10 days. Windows/spans will only accept 1 day as minumum input 
    if time_in_seconds > 604800: 
        no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
        williams_percentile_R = talib.WILLR(high_.values, low_.values, close_.values, no_of_days)
    else: 
        williams_percentile_R = talib.WILLR(high_.values, low_.values, close_.values, 7) # recommended to set to 7 days
    
    return williams_percentile_R[len(williams_percentile_R) - 1] # returns most recent williams%R value

# Parabolic Stop and Reverse indicator is used to identify the trend direction of a particular asset.
# If return value greater than close, means upward trend emerging 
# If return value less than close, means downward trend emerging. 
# May use the sum of previous closes - previous SARS to ensure isnt just random fluctuation. 
def parabolic_SAR(data): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() 
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    parabolic_sar = talib.SAR(np.array(high_), np.array(low_), 0.2, 0.2)
    return parabolic_sar[len(parabolic_sar) - 1]

# ADX(Average Directional Index)
# used to determine the strength of a particular trend.
# The trend has strength when ADX is above 25; the trend 
# is weak or the price is trendless when ADX is below 20, according to Wilder (the person who devised the equation)
def ADX(data): 
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() 
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])
    adx = talib.ADX(np.array(high_), np.array(low_), np.array(close_), 10)
    return adx[len(adx) - 1]

# Technical Indicators used as Features to predict reliance of indicators used in trading strategy. 
def calc_indicators(data, time_in_seconds): 
    #[open, high, low, close]
    #dataset[[1, 2, 3, 4]]  
    dataset = pd.DataFrame.from_dict(data)
    #dataset = dataset.dropna() # removes rows containing null values 

    dataset = dataset.dropna()

    open_ = pd.to_numeric(dataset[1])
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])
    
    # The first thing to notice is that by default rolling looks for n-1 prior rows of data to aggregate,
    # where n is the window size. If that condition is not met, it will return NaN for the window. This is
    # what's happening at the first row. In the fourth and fifth row, it's because one of the values in the sum is NaN.

    # If you would like to avoid returning NaN, you could pass min_periods=1 to the method which reduces the minimum 
    # required number of valid observations in the window to 1 instead of 2
 
    dataset['H-L'] = high_ - low_
    dataset['O-C'] = open_ - close_
    dataset['ma'] = close_.rolling(2, min_periods=1).mean()
    dataset['std'] = close_.rolling(window=2).std().fillna(method='bfill').fillna(method='ffill')
    # 86400 equivilant to 1 day. Windows/spans will only accept 1 day as lowest input
    if time_in_seconds > 86400: 
       no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
       dataset['EWMA_12'] = close_.ewm(span=12 + no_of_days).mean() # span with periods in days. 
    else:
        dataset['EWMA_12'] = close_.ewm(span=12).mean() 
    # 1209600 equivilant to 14 days. Windows/spans will only accept 1 day as minumum input   
    if time_in_seconds > 1209600: 
        no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
        dataset['RSI'] = talib.RSI(close_.values, timeperiod = no_of_days) # recommended to set to 14 days 
        dataset['RSI'] = dataset['RSI'].fillna(method='bfill').fillna(method='ffill')
    else: 
        dataset['RSI'] = talib.RSI(close_.values, timeperiod = 14) # recommended to set to 14 days 
        dataset['RSI'] = dataset['RSI'].fillna(method='bfill').fillna(method='ffill')
    # 1209600 equivilant to 10 days. Windows/spans will only accept 1 day as minumum input 
    if time_in_seconds > 604800: 
        no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
        dataset['Williams %R'] = talib.WILLR(high_.values, low_.values, close_.values, no_of_days)
        dataset['Williams %R'] = dataset['Williams %R'].fillna(method='bfill').fillna(method='ffill')
    else: 
        dataset['Williams %R'] = talib.WILLR(high_.values, low_.values, close_.values, 7) # recommended to set to 7 days
        dataset['Williams %R'] = dataset['Williams %R'].fillna(method='bfill').fillna(method='ffill')

    dataset['SAR'] = talib.SAR(np.array(high_), np.array(low_), 0.2, 0.2)
    dataset['SAR'] = dataset['SAR'].fillna(method='bfill').fillna(method='ffill')

    if time_in_seconds > 864000: 
        no_of_days= int(int(time_in_seconds) / (24 * time_in_seconds)) # rounds to the closest whole number
        dataset['ADX'] = talib.ADX(np.array(high_), np.array(low_), np.array(close_), 10)
        dataset['ADX'] = dataset['ADX'].fillna(method='bfill').fillna(method='ffill')
    else: 
        dataset['ADX'] = talib.ADX(np.array(high_), np.array(low_), np.array(close_), 10)
        dataset['ADX'] = dataset['ADX'].fillna(method='bfill').fillna(method='ffill')

    dataset['Price_Rise'] = np.where(close_.shift(-1) > close_, 1, 0)

    upperbound = dataset['ma'] + (dataset['std'] * 2)
    lowerbound = dataset['ma'] - (dataset['std'] * 2)

    dataset['Upperbound'] = upperbound
    dataset['Lowerbound'] = lowerbound

    #print(dataset)

    return dataset

def SVM_preparation(data, time_in_seconds): 
    
    dataset = calc_indicators(data, time_in_seconds)

    dataset = dataset.astype(str) # converts entire dataframe back to string so can be processed by clf.fit()
                                  # within the Kernel functions
    dataset = dataset.convert_dtypes() # coerce all dtypes of your dataframe to a better fit.

    dataset = dataset.dropna()
    X = dataset.iloc[:, 8:18] # From H-L column to Price_Rise column 
    y = dataset.iloc[:, 18]
   
    split = int(len(dataset)*0.8)
    X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]
    
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    return X_train, X_test, y_train, y_test

def svm_linear(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'linear')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    return confidence 
    
 
def svm_poly(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'poly')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    return confidence
 

def svm_rbf(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'rbf')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    return confidence


def graph_representations_of_indicators(data, time_in_seconds): 

    dataset = calc_indicators(data, time_in_seconds)
    
    open_ = pd.to_numeric(dataset[1])
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])

    # High vs Low in relation to Close
    close_.plot(figsize=(10,6))
    low_.plot()
    high_.plot() 
    plt.grid(True)
    plt.title("High Price vs Low Price")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/High_VS_Low_in_relation_to_Close.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Open vs Close
    open_, close_.plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Open price vs Closing price")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/Open_vs_Close.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # High - Low in relation to Close
    dataset['H-L'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("High - Low in relation to Close")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/High-Low_in_relation_to_Close.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Open - Close in relation to Close
    dataset[['O-C']].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Open Price vs Close Price")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/Open-Close_in_relation_to_Close.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # OHLC all in one graph 
    open_, high_, low_, close_.plot(figsize=(10,6))
    plt.grid(True)
    plt.title("OHLC")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/OHLC.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Moving Average 
    dataset['ma'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Moving Average")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/ma.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Standard Deviation
    dataset['std'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Standard deviation")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/std.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Expodential weighted moving average 
    dataset['EWMA_12'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Expodential weighted moving average")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/EWMA.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Moving Average VS Expodential weighted moving average
    dataset['ma'].plot(figsize=(10,6))
    dataset['EWMA_12'].plot()
    plt.grid(True)
    plt.title("ma_vs_EWMA")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/ma_vs_EWMA.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # RSI
    dataset['RSI'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("RSI")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Oscillator range')
    plt.savefig('graphical_representations/RSI.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Williams %R
    dataset['Williams %R'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Williams %R")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Momentum Oscillation range')
    plt.savefig('graphical_representations/Williams_%R.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # SAR 
    dataset['SAR'].plot(figsize=(10,6))
    open_.plot()
    plt.grid(True)
    plt.title("Parabolic SAR")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/Parabolic_SAR.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # ADX
    dataset['ADX'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("ADX - Average Directional Index")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Strength Trend')
    plt.savefig('graphical_representations/ADX.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Price Rise 
    dataset['Price_Rise'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("Price Rise")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/Price_Rise.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # Upper bound VS Lower Bound along with the mean price
    close_.plot(figsize=(10,6))
    dataset[['ma', 'Upperbound', 'Lowerbound']].plot()
    plt.grid(True)
    plt.title("Bollinger Bands")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/Bollinger_Bands.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)

    # All indicators in one graph 
    open_, high_, low_, close_.plot(figsize=(10,6))
    dataset[['H-L', 'O-C', 'ma', 'EWMA_12', 'std', 'RSI', 'SAR', 'ADX', 'Williams %R', 'Price_Rise', 'Upperbound', 'Lowerbound', ]].plot()
    plt.grid(True)
    plt.title("All indicators in one")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/All_indicators.png')
    plt.close() # Reduce the number of plts opened. Reduce memory usage (kbytes)