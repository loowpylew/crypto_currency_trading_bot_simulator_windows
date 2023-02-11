from os import close
import StatisticalModels as sms
import krakenex # library that is used to interact with the kraken API 
import json # Used to save/parse data that will be collected 
import time # Allows us to handle various operations regarding time i.e. no. of seconds passed since the point where time begins for some event.
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import datetime as dt
import pandas_datareader.data as web
import talib
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from collections import Counter

def get_crypto_data(pair, since, api): 
    return api.query_public('OHLC', data = {'pair': pair, 'since': since})['result'][pair]


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
    

def graph_representations_of_indicators(data, time_in_seconds): 

    dataset = calc_indicators(data, time_in_seconds)

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

    # High - Low in relation to Close
    dataset['H-L'].plot(figsize=(10,6))
    plt.grid(True)
    plt.title("High - Low in relation to Close")
    plt.axis('tight')
    plt.xlabel('no. of data point (60 closing prices per hour)')
    plt.ylabel('Price')
    plt.savefig('graphical_representations/High-Low_in_relation_to_Close.png')
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


def svm_linear(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'linear')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:', confidence)
    predictions = clf.predict(X_test)
    print(predictions)
    print('predicted class counts:',Counter(predictions))
 
 
def svm_poly(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'poly')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
 

def svm_rbf(data, time_in_seconds):
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'rbf')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
    
def svm_test_return(data, time_in_seconds): 
    X_train, X_test, y_train, y_test = SVM_preparation(data, time_in_seconds)
    clf = svm.SVC(kernel = 'rbf')
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    return confidence


if __name__ == '__main__': 
    
    api = krakenex.API() # instatiation of krakenex library/connects to the kraken API 
    api.load_key('kraken.key') # The loadkey function allows us to load our API keys and access the data specific to the account made on kraken
                               # Here, we input the .KEY file as a parameter within the load_key function that stores both the API KEY and private key 
    pair = ("ANT", "USD") # Currency pair
    since = str(int(time.time() -  3600)) # Requires edit, uses 3600 seconds which is equivilant to an hour whereas I want to know the buy sell operations from the past day 
    time_in_seconds = 3600
    #data = get_crypto_data(pair[0]+pair[1], since)

    #close_ = float(data[len(data) - 2][4])

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

    #print(sms.store_upper_and_lower_bounds(data))
    #print(sms.calcBollingerBands(data, pair[0], pair[1]))
    
    """data = get_crypto_data(pair[0]+pair[1], since)

    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    open_ = pd.to_numeric(dataset[1])
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])
    williams_perentile_R = talib.WILLR(high_.values, low_.values, close_.values, 7)
    #print(williams_perentile_R)

    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    open_ = pd.to_numeric(dataset[1])
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    close_ = pd.to_numeric(dataset[4])
    rsi = talib.RSI(close_.values, timeperiod = 14)
   # print(rsi[len(rsi) - 1: len(rsi)])

   
    dataset = pd.DataFrame.from_dict(data)
    dataset = dataset.dropna() # removes rows containing null values 
    high_ = pd.to_numeric(dataset[2])
    low_ = pd.to_numeric(dataset[3])
    parabolic_sar = talib.SAR(np.array(high_), np.array(low_), 0.2, 0.2)
    #print(parabolic_sar[len(parabolic_sar) - 1: len(parabolic_sar)])
    #print(parabolic_sar)
    #print("\n")
    #print(dataset[4])

    #graph_representations_of_indicators(data, time_in_seconds)"""

    while(1):
        for i in range(8):
            data = get_crypto_data(pair[0]+pair[1], since, api)
            #dataset = pd.DataFrame.from_dict(data)
            """dataset = dataset.dropna() # removes rows containing null values 
            
            print(1)
            svm_linear(dataset, time_in_seconds)  
            dataset = pd.DataFrame.from_dict(data)
            dataset = dataset.dropna() # removes rows containing null values 
           
            print(2)
            svm_poly(dataset, time_in_seconds)
            dataset = pd.DataFrame.from_dict(data)
            dataset = dataset.dropna() # removes rows containing null values 
            
            print(3)
            svm_rbf(dataset, time_in_seconds)"""

            open_ = float(data[len(data) - 1][1]) # most recent opening price
            close_ = float(data[len(data) - 2][4]) # previous closing price    

            price_difference = open_ - close_
            #print(len(data)) #Not too sure why downloads +1 data point after 9 analyzed data sets which is the point at which a regeneration of counters occurs 
            #before next consecutive run of data.    

            """if sms.svm_linear(data, time_in_seconds) >= 0.7 or sms.svm_poly(data, time_in_seconds) >= 0.7 or sms.svm_rbf(data, time_in_seconds) >= 0.7:
                print("True")
            else: 
                print("[Accuracy rate of technical indicators is not above 70%]")
                print("-------------------------------------------------------------------------")
                print(f" Linear Prediction: {sms.svm_rbf(data, time_in_seconds)} out of '1'")
                print(f" Polynormal Prediction: {sms.svm_rbf(data, time_in_seconds)} out of 0-1")
                print(f" RBF Prediction: {sms.svm_rbf(data, time_in_seconds)} out of 0-1")   
                print(" Cannot use technical indicators in relation to current state of")
                print(f"{pair[0] + pair[1]} until this condition is met")
                print("------------------------------------------------------------------------\n")"""

               
            #print("Percentage Decrease: ", sms.calcPercentageDecrease(data, time_in_seconds))
            #print("Percentage Increase: ", sms.calcPercentageIncrease(data, time_in_seconds))
            print("MA: ", sms.calcSimpleMovingAverage(data))
            print("EWMA: ", sms.exponentially_weighted_moving_average(data, time_in_seconds))
            print("Standard Deviation: ", sms.calcStandardDeviation(data))
            #print("Boolinger Bands: ", sms.calcBollingerBands(data, ))
            #print("upper_lower: ", sms.store_upper_and_lower_bounds(data,))
            print("RSI: ", sms.relative_strength_index(data, time_in_seconds))
            print("ADX: ", sms.ADX(data))
            print("Parabolic SAR", sms.parabolic_SAR(data))
            print("williams %R: ", sms.williams_perecntile_R(data, time_in_seconds))
                
        
            if i == 7:
                print("sleeping")
                time.sleep(46) 

