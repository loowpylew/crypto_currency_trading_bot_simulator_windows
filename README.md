# crypto_currency_trading_bot_simulator_windows

For whoever may wish to experiment with crypto currency pairs without having to invest real money, I hope you find this software useful. 

This software is effectively a Monte Carlo Machine in its own right as it predicts outcomes as a result of random intervention of variables i.e. changes in the price of a giving currecny pair (OHLC). This software encompasses a user interface (UI) along with a trading bot that works in repsonse to one another based off the users actions i.e. making deposits, changing STOP LOSS/PRICE THRSHOLD, restarting/ending the trading simulation, setting timestamp (used to POST to the KRAKEN API to recieve back historical data dating back a given period of time) and so forth. Along with these, the user can view live top 100 most volatile crypto currencies to use as indictor to gauge which crypto to experiment with. The user can also view account holdings and trades history along with a help menu that can be accessed to educate the user/use as a reminder on what various indicators mean/indicate.

To run this software, instructions are provided below on related modules/imports to download. The instructions for this trading bot will be under the assumption you will be running on your local windows machine. Hence, the repository has been named "crypto_currency_trading_bot_simulator_windows". This can be run on a remote instance, but would require you to run an instance preferably windows/Linux that supports python equal to or beyond version 3.8. Experienced installation issues with the module 'talib' which is used to produce various technical indicators on a remote Ubuntu 10 instance. For free tier options on google cloud which is the cloud service provider I have been testing the trading bot/UI on; the Ubuntu 10 free tier option does not support anything higher than python3.7.1 thus could not compile and run the trading bot successfully. Notherless, you can run an Ubuntu version which was created if you wish to use the same remote server as I did, but many of the technical indicators are not used to display their values when the trading bot is analyzing the current state of a given currency pair. The only difference in accuracy which may be experienced in respects to the trading algorithm used is that for this version, we use the expodentially weighted moving average (ewma) as opposed to the simple moving average. 

The link to my the trading bot/UI that can be run on an Ubuntu 10 remote instance using the free tier option: https://github.com/loowpylew/crypto_currency_trading_bot_simulator_Ubuntu_10

If you wish to adapt upon this software for your own personal use. You're re more than welcome to.

**### Quick pointers:** 

You will notice I have written code related to SVM (support vector machines) where I attempted to incorporate within my trading strategy this machine learning technique, but was unsuccessful giving when implemented within the backend.py file, it did not produce any results i.e. accuracy value/confidence value. Reason being is that SVM's take a short while to create a new vector space to which would be used to map out the values calculated by the indicators. Thus when testing on its own, the accuracy rate at some stages would reach 100% accuracy, but when used within a file with other related processes, it is unable to compute in time during each analyse of the anaylze method which houses our trading strategy. Thus was rendered useless. Alongside this, many of the technical indicators are not used within strategy itself as they impeded on our ability to adapt to changes on a micro scale in the change in price of a given currency pair i.e. XETH vs ZUSD. But are simply used so that you as the user can take down notes and use for your own personal use on how the indictor's change in response to the current state of the market. They can be incorporated within the trading strategy and is simply a matter of implementing the existing methods from the statistical models.py file over to the trading strategy within the backend.py file which I have personally done myself, but found this was more suitable for long term responses in relation to the change in price of a given currency pair where trading events are far less active.

**_Instructions_**

This is under the assumption you already have .git .pip3 and the latest version of python installed on your local machine. 
If you do not, instructions on how to install these can easily be found online. 

List of imports required for project: 
- pip3 install colorama
- pip3 install krakenex 
- pip3 install tabulate
- sudo apt install python3-pandas
- pip3 install pandas_datareader

*### How to install Talib on local machine (windows)**

Download Unofficial Windows Binaries for Python Extension Packages from: https://www.lfd.uci.edu/~gohlke/pythonlibs/
Select the appropriate version for your operating system i.e. for windows I would type: 
python3 -m pip install TA_Lib‑0.4.19‑cp39‑cp39‑win_amd64.whl

The general idea is that you git clone this repository, open two command prompts/terminals and naviagte to where ever you decide to save this repository on your local machine and run: 
- python main.py 
- python main2.py 

where main.py is the UI and main2.py is the trading bot.
