import Analyzer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

mk=Analyzer.MarketDB()
stocks=['삼성전자','SK하이닉스','현대자동차','NAVER']
df=pd.DataFrame()
for s in stocks:
    df[s]=mk.get_daily_price(s,'2019-01-01','2022-01-23')['close']
print(df)

daily_ret=df.pct_change()       #일간 수익률
annual_ret=daily_ret.mean()*252 #연간 수익률
daily_cov=daily_ret.cov()       #일간 리스크
annual_cov=daily_cov*252        #연간 리스크

port_ret=[]
port_risk=[]
port_weights=[]
sharpe_ratio=[]

for _ in range(20000):
    weights=np.random.random(len(stocks))
    weights /= np.sum(weights)
    
    returns=np.dot(weights,annual_ret)  #랜덤하게 생성한 종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오 전체수익률을 구한다
    risk=np.sqrt(np.dot(weights.T,np.dot(annual_cov,weights)))  
    #종목별 연간 공분산과 종목별 비중 배열을 곱한뒤 이를다시 종목별 비중의 전치로 곱한다. 이렇게 구한결과값의 제곱근을 구하면 포폴전체의 리스크를 구할수 있다
    
    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk)
    
portfolio ={'Returns':port_ret,'Risk':port_risk,'Sharpe':sharpe_ratio}
for i,s in enumerate(stocks):
    portfolio[s]=[weight[i] for weight in port_weights]
df=pd.DataFrame(portfolio)
df=df[['Returns','Risk','Sharpe']+[s for s in stocks]]

max_sharpe=df.loc[df['Sharpe']==df['Sharpe'].max()]
min_risk=df.loc[df['Risk']==df['Risk'].min()]
print(max_sharpe)
print(min_risk)

df.plot.scatter(x='Risk',y='Returns',c='Sharpe',cmap='viridis',edgecolors='k',figsize=(11,7),grid=True)
plt.scatter(x=max_sharpe['Risk'],y=max_sharpe['Returns'],c='r',marker='*',s=300)
plt.scatter(x=min_risk['Risk'],y=min_risk['Returns'],c='r',marker='X',s=200)
plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()

    
    