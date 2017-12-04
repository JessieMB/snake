import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

def main(): 
    style.use('ggplot')
    
    #part 2: evaluating stocks
    start = dt.datetime(2016, 6, 1)
    end = dt.datetime(2017, 10, 30)
    df = web.DataReader('SWK', "yahoo", start, end)
    df.to_csv('SWK.csv')
    
    df = pd.read_csv('SWK.csv', parse_dates=True, index_col=0)
    
    #df['Adj Close'].plot()
    #df.show()
    
    #Part three: Moving averages
    #df['100ma'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()
    
    #print(df.head())
    #ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    #ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
    #ax1.plot(df.index, df['Adj Close'])
    #ax1.plot(df.index, df['100ma'])
    #ax2.bar(df.index, df['Volume'])
    
    #plt.show()    
    
    #Part four: 
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()
    print(df_ohlc.head())
    df_ohlc = df_ohlc.reset_index()
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    fig = plt.figure()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
    ax1.xaxis_date()
    
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    
    ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)
    plt.show()
    

if __name__ == "__main__":
    main()