#추세 추종 매매

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import matplotlib.pyplot as plt
import Analyzer

mk=Analyzer.MarketDB()
df=mk.get_daily_price('NAVER','2020-01-02')

df['MA20']=df['close'].rolling(window=20).mean() #20동안의 이동평균
df['stddev']=df['close'].rolling(window=20).std() #20일 단위의 표준편차
df['upper']=df['MA20']+(df['stddev']*2)             #2*표준편차를 이동편균에 더해줘 상단 볼린저 밴드로 계산
df['lower']=df['MA20']-(df['stddev']*2)             #빼줘서 하단 볼린저 밴드 계산
df['PB']=(df['close']-df['lower'])/(df['upper']-df['lower'])    #(종가-하단밴드)/(상단밴드-하단밴드) 를 구해 %B 칼람 생성
df['TP']=(df['high']+df['low']+df['close'])/3       #고가 저가 종가 합을 3으로 나눠 중심가격 TP를 구한다
df['PMF']=0     #긍정적 현금 흐름
df['NMF']=0     #부정적 현금 흐름

for i in range(len(df.close)-1):
    
    if df.TP.values[i]<df.TP.values[i+1]:   #i번째 중심가격보다 i+1중심가격이 높으면
        df.PMF.values[i+1]=df.TP.values[i+1]*df.volume.values[i+1]  #i+1 중심가격과 거래량의 곱을 i+1긍정적인 현금흐름에 저장
        df.NMF.values[i+1]=0    #i+1부정적 현금흐름 값은 0으로 저장한다
        
    else:       #부정적 현금흐름값 저장
        df.NMF.values[i+1]=df.TP.values[i+1]*df.volume.values[i+1]
        df.PMF.values[i+1]=0

df['MFR']=df.PMF.rolling(window=10).sum()/ df.NMF.rolling(window=10).sum()
df['MFI10']=100-100/(1+df['MFR'])   #현금흐름 지표
df=df[19:]

plt.figure(figsize=(9,8))
plt.subplot(2,1,1)
plt.title('NAVER Bollinger Band(20 day,2 std) - Trend Following')
plt.plot(df.index,df['close'],color='#0000ff',label='Close')
plt.plot(df.index, df['upper'],'r--',label='Upper band')
plt.plot(df.index,df['MA20'],'k--',label='Moving average 20')
plt.plot(df.index,df['lower'],'c--',label='Lower band')
plt.fill_between(df.index,df['upper'],df['lower'],color='0.9')
for i in range(len(df.close)):
    if df.PB.values[i]>0.8 and df.MFI10.values[i]>80:
        plt.plot(df.index.values[i],df.close.values[i],'r^')
    elif df.PB.values[i]<0.2 and df.MFI10.values[i]<20:
        plt.plot(df.index.values[i],df.close.values[i],'bv')
plt.legend(loc='best')

plt.subplot(2,1,2)
plt.plot(df.index,df['PB']*100,'b',label='%B x 100')    #MFI와 비교할수 있게 %b에 100을 곱해 표현
plt.plot(df.index,df['MFI10'],'g--',label='MFI(10 day)')
plt.yticks([-20,0, 20, 40, 60, 80, 100, 120])
for i in range(len(df.close)):
    if df.PB.values[i]>0.8 and df.MFI10.values[i]>80:
        plt.plot(df.index.values[i],0,'r^')
    elif df.PB.values[i]<0.2 and df.MFI10.values[i]<20:
        plt.plot(df.index.values[i],0,'bv')
        
plt.grid(True)
plt.legend(loc='best')
plt.show();
    
