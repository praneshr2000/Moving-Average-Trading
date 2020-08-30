import pandas as pd
import yfinance as yahoo
import numpy as np
import matplotlib.pyplot as plt

userInput = input("What stock data would you like to see?")
stockName = yahoo.Ticker(userInput)

df = pd.DataFrame(stockName.history(period="10Y"))

df['Days'] = np.nan
for i in range(len(df)):
    df['Days'][i] = i
    
df['50SMA'] = np.nan
for i in range(49, len(df['Open'])):
    avg = 0;
    for j in range(50):
        avg += df['Close'][i - j]
    avg = avg / 50.0
    df['50SMA'][i] = avg

df['200SMA'] = np.nan
for i in range(199, len(df['Open'])):
    avg = 0;
    for j in range(200):
        avg += df['Close'][i - j]
    avg = avg / 200.0
    df['200SMA'][i] = avg

df['Difference'] = np.nan
for i in range(199, len(df['Open'])):
    
    df['Difference'][i] = df['50SMA'][i] - df['200SMA'][i]              

startSignal = []
startDate = []
endSignal = []
endDate = []

startSignalIndex = []
endSignalIndex = []
buySellIndication = []
count = 0

for i in range(199, len(df['Open']) - 1):
    if (df['Difference'][i] == 0):
        if (count % 2 == 0):
            startSignalIndex.append(i)
            if (df['Difference'][i] < 0 and df['Difference'][i + 1] > 0):
                buySellIndication.append(1)
            else:
                buySellIndication.append(0)
        else:
            endSignalIndex.append(i)
        count += 1
    elif (df['Difference'][i] < 0 and df['Difference'][i + 1] > 0):
        if (count % 2 == 0):
            startSignalIndex.append(i)
            if (df['Difference'][i] < 0 and df['Difference'][i + 1] > 0):
                buySellIndication.append(1)
            else:
                buySellIndication.append(0)
        else:
            endSignalIndex.append(i)
        count += 1
    elif (df['Difference'][i] > 0 and df['Difference'][i + 1] < 0):
        if (count % 2 == 0):
            startSignalIndex.append(i)
            if (df['Difference'][i] < 0 and df['Difference'][i + 1] > 0):
                buySellIndication.append(1)
            else:
                buySellIndication.append(0)
        else:
            endSignalIndex.append(i)
        count += 1
        
plt.plot(df['Days'], df['Close'], alpha = 0.5, label = userInput.upper())
plt.plot(df['Days'], df['50SMA'], alpha = 0.5, label = '50SMA')
plt.plot(df['Days'], df['200SMA'], alpha = 0.5, label = '200SMA')

    
for i in range(min(len(startSignalIndex), len(endSignalIndex))):
    startPrice = df['Close'][startSignalIndex[i]]
    endPrice = df['Close'][endSignalIndex[i]]
    sDate = startSignalIndex[i]
    eDate = endSignalIndex[i]

    if (buySellIndication[i] == 1):
        plt.scatter(sDate, startPrice, label = 'Buy Point', marker = 'D', color = 'green')
        plt.scatter(eDate, endPrice, label = 'Sell Point', marker = 'D', color = 'red')
        if (i == 0):
            plt.legend()
    else:
        plt.scatter(sDate, startPrice, label = 'Sell Point', marker = 'D', color = 'red')
        plt.scatter(eDate, endPrice, label = 'Buy Point', marker = 'D', color = 'green')
        if (i == 0):
            plt.legend()

plt.show()


