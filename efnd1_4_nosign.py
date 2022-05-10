#!/usr/bin/python3
"""
1. Install python 3+
2. Run "pip install coinex.py discord-webhook datetime numpy pandas bcolors" in cmd
5. Now run the script
"""
# Required library installation
from coinex.coinex import CoinEx
import requests
import json
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime
from discord_webhook import DiscordWebhook
import sys

# Personal keys are censored, script wont work unless you make your own.

# Get your webhook url by going to your discord channel settings and creating a webhook
webhookurl = 'https://discord.com/api/webhooks/85003019**********/wto3Ogn_UnDfrKGnFCxaryLjkktwVcNLo_B4MPFT5NDAEQM7********************'

# Get your CoinEx key by going to https://www.coinex.com/apikey and creating an api
public='2D883BBEEEEF428FBB931A********************' # Public key for CoinEx access
SecretKey='78FE1D7534B3814990725BC97E6F1DEE146125********************' # Private key for CoinEx access

coinex = CoinEx(public, SecretKey)

webhook1 = DiscordWebhook(url= webhookurl, content='Started the trading bot!')
webhook2 = DiscordWebhook(url= webhookurl, content='COINEX ERROR')
webhook3 = DiscordWebhook(url= webhookurl, content='I sold DOGE!')
webhook4 = DiscordWebhook(url= webhookurl, content='Skipped doge sell (Insufficient doge)')
webhook5 = DiscordWebhook(url= webhookurl, content='I bought DOGE!')
webhook6 = DiscordWebhook(url= webhookurl, content='Skipped doge buy (Insufficient usdt)')
webhook7 = DiscordWebhook(url= webhookurl, content='ERROR1')
webhook8 = DiscordWebhook(url= webhookurl, content='ERROR2')
webhook9 = DiscordWebhook(url= webhookurl, content='OTHER ERROR')


# Commands to run webhooks and run errors. None take place
"""
webhook1.execute() #Started the trading bot!
webhook2.execute() #COINEX ERROR
webhook3.execute() #I sold DOGE!
webhook4.execute() #Skipped doge sell (Insufficient doge)
webhook5.execute() #I bought DOGE!
webhook6.execute() #Skipped DOGE buy (Insufficient usdt)
webhook7.execute() #ERROR1
webhook8.execute() #ERROR2
webhook9.execute() #OTHER ERROR

assert (sys.version_info[0] == 3), "Python version must be 3"

print(colors.HEADER + "COINEX ERROR" + colors.ENDC)
print(colors.OKBLUE + "COINEX ERROR" + colors.ENDC)
print(colors.OKCYAN + "COINEX ERROR" + colors.ENDC)
print(colors.OKGREEN + "COINEX ERROR" + colors.ENDC)
print(colors.WARNING + "COINEX ERROR" + colors.ENDC)
print(colors.FAIL + "COINEX ERROR" + colors.ENDC)
print(colors.ENDC + "COINEX ERROR" + colors.ENDC)
print(colors.BOLD + "COINEX ERROR" + colors.ENDC)
print(colors.UNDERLINE + "COINEX ERROR" + colors.ENDC)
"""

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

FLAG_DOGEUSDT = True ## maybe make this a real thing in the future??? output is cluttered rn.


def get_doge_price_last(): # latest price
    doge_price_last=ticker_doge['last']
    return doge_price_last

def get_doge_price_high(): # highest price
    doge_price_high=ticker_doge['high']
    return doge_price_high

def get_doge_price_low(): # lowest price
    doge_price_low=ticker_doge['low']
    return doge_price_low

def get_least_amount_doge(): # Find the lowest amount that doge is able to be traded at
    market=requests.get('https://www.coinex.com/res/market/') # Access URL
    market=json.loads(market.text) # Make json visible
    data=market['data']
    marketdata=data['market_info']
    marketinfo=marketdata['DOGEUSDT']
    doge_least_amount=marketinfo['least_amount']
    return doge_least_amount

def get_maker_fee_doge(): # Find the required coinex trade fee percentage for doge
    market=requests.get('https://www.coinex.com/res/market/') # Access URL
    market=json.loads(market.text) # Make json visible
    data=market['data']
    marketdata=data['market_info']
    marketinfo=marketdata['DOGEUSDT']
    doge_maker_fee=marketinfo['maker_fee_rate']
    return doge_maker_fee

min_doge_sell=get_least_amount_doge()
doge_maker_fee=get_maker_fee_doge()
doge_maker_fee_float = float(doge_maker_fee)

count = 0 # Start loop counter
coinexerrorcount = 0
dogebuyskipcount = 0
dogesellskipcount = 0
dogetradecount=0
other_exceptioncount = 0
exception1count = 0
coinexerror = False
one_float = float(1) # define the number one as a float

print()
print(doge_maker_fee)
print(colors.OKGREEN + "Started the trading bot!" + colors.ENDC)
webhook1.execute() #Started the trading bot!

#run loop forever:
while True:
    try:
        print()
        count += 1 # variable will increment by 1 every loop iteration
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.")
        print("Ran at", current_time, "Loop has run", count, "times.")

        # Get current prices. This often produces an error, so it runs again on error
        try:
            balance=coinex.balance_info()
        except:
            coinexerror = True

        while coinexerror:
            try:
                balance=coinex.balance_info()
            except:
                coinexerrorcount += 1
                coinexerrorcount_str = str(coinexerrorcount)
                print(colors.WARNING + "COINEX ERROR (" + coinexerrorcount_str + ")" + colors.ENDC)
                if coinexerrorcount > 360:
                    try:
                        webhook2.execute() #COINEX ERROR
                    except:
                        print(colors.WARNING + "NETWORK ERROR" + colors.ENDC)
                time.sleep(30)
            else:
                coinexerrorcount = 0
                coinexerror = False

        if FLAG_DOGEUSDT:
            tick_doge=requests.get('https://api.coinex.com/v1/market/ticker?market=DOGEUSDT')
            tick_doge=json.loads(tick_doge.text)
            data_doge=tick_doge['data']
            ticker_doge=data_doge['ticker']
            doge_price_last=get_doge_price_last()
            dogehigh=get_doge_price_high()
            dogelow=get_doge_price_low()
            usdt=balance['USDT']
            doge=balance['DOGE']
            usdtbal=usdt['available']
            dogebal=doge['available']
            min_doge_sell_float=float(min_doge_sell)
            dogehigh_float=float(dogehigh)
            dogelow_float=float(dogelow)
            doge_price_last_float=float(doge_price_last)
            dogebalfloat = float(dogebal)
            min_doge_sell_float = float(min_doge_sell)

        if count == 1:
            if FLAG_DOGEUSDT:
                dogecapture_float=float(get_doge_price_last())

        if dogebuyskipcount >= 7200:
            dogecapture_float=float(get_doge_price_last())

        if dogesellskipcount >= 7200:
            dogecapture_float=float(get_doge_price_last())

        dogetrade_float=20 #trades this number of DOGE everytime ## make this a number grabbed from api
        tradenumber=3 #tradenumber * makerfee = percentage to make a trade
        multiplier1=1.2

        if FLAG_DOGEUSDT:
            dogetrade_float_1_2=float(dogetrade_float * multiplier1)
            usdtbalfloat = float(usdtbal) #usdt balance
            usdtbaltodoge=(usdtbalfloat / float(doge_price_last)) #amount of doge able to be purchased with usdt balance
            usdtbaltodoge_float=float(usdtbaltodoge)
            usdtbaltodoge_float1_2=float(usdtbaltodoge_float * multiplier1)
            dogetrade_buy_float=float(float(doge_price_last) * dogetrade_float)

        #tradenumber=((usdtbaltodoge_float + dogebalfloat) / dogetrade_float)

        if FLAG_DOGEUSDT:
            print(usdtbaltodoge_float, "usdtbaltodoge_float", dogetrade_float_1_2, "dogetrade_float_1_2")
            print(dogebalfloat, "dogebalfloat |", usdtbalfloat, "usdtbalfloat")

        if FLAG_DOGEUSDT:
            print(dogecapture_float, "dogecapture |", doge_price_last, "(doge per usdt) |", (1 - (dogecapture_float / doge_price_last_float)), "% doge |", doge_maker_fee, "doge fee |")

        if FLAG_DOGEUSDT:
            try:
                # Check the status of your doge order
                orderdoge=coinex.order_pending('DOGEUSDT')
                # Check if there is a doge order
                if orderdoge['has_next']:
                    print("There are orders left")

                else:
                    if dogecapture_float < (doge_price_last_float * (one_float - (doge_maker_fee_float * tradenumber))): #price of doge is less than or equal to lowest price in 24 hours
                        if dogebalfloat > dogetrade_float_1_2: #doge amount is more than minimum buy
                            coinex.order_market('DOGEUSDT', 'sell', dogetrade_float) # Place a sell order for doge
                            dogetradecount -= 1
                            dogetradecount_str = str(dogetradecount)
                            print(colors.OKGREEN + "I sold DOGE! (bot2) (" + dogetradecount_str + ")" + colors.ENDC)
                            webhook3.execute() #I sold DOGE!
                            dogecapture_float=float(doge_price_last_float)
                            dogesellskipcount = 0
                        else:
                            print(colors.OKBLUE + "Skipped doge sell (Insufficient usdt)" + colors.ENDC)
                            dogesellskipcount += 1
                            if dogesellskipcount < 5:
                                webhook4.execute() #Skipped doge sell (Insufficient doge)

                    if dogecapture_float > (doge_price_last_float * (one_float + (doge_maker_fee_float * tradenumber))): # Make sure that the gain is more than the coinex fee
                        if usdtbaltodoge_float > dogetrade_float_1_2: #usdt amount is more than minimum buy
                            coinex.order_market('DOGEUSDT', 'buy', dogetrade_buy_float) # Place a buy order for doge
                            dogetradecount += 1
                            dogetradecount_str = str(dogetradecount)
                            print(colors.OKGREEN + "I bought DOGE! (bot2) (" + dogetradecount_str + ")" + colors.ENDC)
                            webhook5.execute() #I bought DOGE!
                            dogecapture_float=float(doge_price_last_float)
                            dogebuyskipcount = 0
                        else:
                            print(colors.OKBLUE + "Skipped doge buy (Insufficient usdt)" + colors.ENDC)
                            dogebuyskipcount += 1
                            if dogebuyskipcount < 5:
                                webhook6.execute() #Skipped doge buy (Insufficient usdt)

            except Exception as exception1:
                if exception1count > 1:
                    webhook8.execute() #ERROR2
                print(exception1)
                exception1count += 1
                print(colors.FAIL + "ERROR2" + colors.ENDC)
            else:
                exception1count = 0

    except Exception as other_exception:
        if other_exceptioncount > 1:
            try:
                webhook9.execute() #OTHER ERROR
            except:
                print(colors.FAIL + "DISCORD ERROR" + colors.ENDC)
        print(other_exception)
        other_exceptioncount += 1
        print(colors.FAIL + "OTHER ERROR" + colors.ENDC)
    else:
        other_exceptioncount = 0

    time.sleep(60) #loop SHOULD restart every 60, but the process takes about a second.
