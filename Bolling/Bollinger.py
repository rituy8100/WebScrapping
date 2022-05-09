import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import matplotlib.pyplot as plt
import Analyzer

mk=Analyzer.MarketDB()
df=mk.get_daily_price('NAVER','2021-01-02')

df['MA20']=df['close'].rolling(window=20).mean()
df['stddev']=df['close'].rolling(window=20).std()
df['upper']=df['MA20']+(df['stddev']*2)
df['lower']=df['MA20']-(df['stddev']*2)
df=df[19:]

plt.figure(figsize=(9,5))
plt.plot(df.index,df['close'],color='#0000ff',label='Close')
plt.plot(df.index,df['upper'],'r--',label='Upper band')
plt.plot(df.index,df['MA20'],'k--',label='Moving Average 20')
plt.plot(df.index,df['lower'],'c--',label='lower band')
plt.fill_between(df.index,df['upper'],df['lower'],color='0.9')
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.show()
