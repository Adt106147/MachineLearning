from finlab.data import Data
from collections import defaultdict

global allstocklist  
allstocklist = []
稅後淨利 = Data().get('本期淨利（淨損）', 1)
for i in 稅後淨利.keys():
    allstocklist.append(i)

def Buffett(data):
    
    #此策略僅兩個條件:  1.近三年平均ROE>.15  2.最近年度股東權益報酬率＞平均值(市場及產業)
    稅後淨利 = data.get('本期淨利（淨損）', 12)
    
    # 股東權益，有兩個名稱，有些公司叫做權益總計，有些叫做權益總額
    # 所以得把它們抓出來
    權益總計 = data.get('權益總計', 12)
    權益總額 = data.get('權益總額', 12)
    
    # 並且把它們合併起來    
    權益總計.fillna(權益總額, inplace=True)
    
    #條件1.ROE近三年平均
    近三年平均ROE = (((稅後淨利.iloc[-1]+稅後淨利.iloc[-2]+稅後淨利.iloc[-3]+稅後淨利.iloc[-4])/權益總計.iloc[-1])+((稅後淨利.iloc[-5]+稅後淨利.iloc[-6]+稅後淨利.iloc[-7]+稅後淨利.iloc[-8])/權益總計.iloc[-5])+((稅後淨利.iloc[-9]+稅後淨利.iloc[-10]+稅後淨利.iloc[-11]+稅後淨利.iloc[-12])/權益總計.iloc[-9]))/3
    
    condition1 = 近三年平均ROE > 0.15
    
    #存取好condition1所抓出來的股票
    results = condition1[condition1]
    
    #找出與condition1所選出的同類股
    stockindex = []
    for i in range(len(results)):
        stockindex.append(int(results.index[i]))
    
    #存取所有同類股代碼，一對多的dict
    samekind = defaultdict(list)
    for j in range(len(stockindex)):
        for i in range(len(allstocklist)):
            if(str(int(allstocklist[i])//100)==str(int(stockindex[j])//100)):
                samekind[stockindex[j]].append(allstocklist[i])
    
    #計算同類股(同行)的平均ROE，方法同上一對多的dict，方便後續比較個股與同行業平均
    totalni = defaultdict(list)
    for i in samekind.keys():
        sumroe = 0
        avgroe = 0
        for j in samekind[i]:
            sumroe = (稅後淨利[j].iloc[-1]/權益總計[j].iloc[-1])+sumroe
        avgroe = sumroe/len(samekind[i])
        totalni[i].append(avgroe)
    
    #跟同業比較後，條件符合者存入final變數最後回傳
    final = []    
    for i in range(len(stockindex)):
        if (稅後淨利[str(stockindex[i])].iloc[-1]/權益總計[str(stockindex[i])].iloc[-1])>totalni[stockindex[i]]:
            final.append(stockindex[i])
    return final 
 