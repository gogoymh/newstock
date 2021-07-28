'''
from marcap import marcap_data


target_year = '2021'
target_month = '06'
target_day = '30'

#date = "%s-%s-%s" % (target_year, target_month, target_day)
#print(date)
df = marcap_data('2021-01-21', '2021-06-30')
if df.empty:
    print("%s-%s-%s Dataframe is empty." % (target_year, target_month, target_day))
else:
    print(df[-10:])

import FinanceDataReader as fdr

# Samsung(005930), 2000-01-01 ~ 2019-12-31
df = fdr.DataReader('005930', '2020-01-01', '2021-06-30')
if df.empty:
    print("%s-%s-%s Dataframe is empty." % (target_year, target_month, target_day))
else:
    print(df[-10:])

import pandas as pd

save_path = "/home/DATA/ymh/s_modeling/redata"
symbols = pd.read_csv("/home/DATA/ymh/s_modeling/data/data_2822_20210608.csv", encoding='utf-8')
symbols = symbols.rename(columns={"단축코드":"Code", "시장구분":"Market"})
symbols = pd.concat([symbols['Code'], symbols['Market']], axis=1)
symbols = symbols[symbols.Market != 'KONEX']
len_stocks = len(symbols) # 종목의 총 개수

#print(symbols)
for i in range(10):
    print(symbols.iloc[i,0])


import FinanceDataReader as fdr

# Samsung(005930), 2000-01-01 ~ 2019-12-31
df = fdr.DataReader('005930', '2020-01-01', '2021-06-30')
print(df.iloc[-3:,0].mean())

import pandas as pd

save_path = "/home/DATA/ymh/s_modeling/redata"
symbols = pd.read_csv("/home/DATA/ymh/s_modeling/data/data_2822_20210608.csv", encoding='utf-8')
symbols = symbols.rename(columns={"단축코드":"Code", "시장구분":"Market"})
symbols = pd.concat([symbols['Code'], symbols['Market']], axis=1)
symbols = symbols[symbols.Market != 'KONEX']
len_stocks = len(symbols) # 종목의 총 개수

print(len_stocks)
'''
'''
import FinanceDataReader as fdr

# Samsung(005930), 2000-01-01 ~ 2019-12-31
target_year, target_month, target_day = '2021', '07', '02'
df = fdr.DataReader('005930', '2014-01-01', '%s-%s-%s' % (target_year, target_month, target_day))

print(df.loc[df.index.values[-10]])
'''

#if str(df.index.values[-1])[:10] != '%s-%s-%s' % (target_year, target_month, target_day):
#    print("%s-%s-%s Dataframe is empty." % (target_year, target_month, target_day))


#target_year, target_month, target_day = '2021', '07', '02'
#df = df.loc["%s-%s-%s" % (target_year, target_month, target_day)]

#if df.empty:
#    print("%s-%s-%s Dataframe is empty." % (target_year, target_month, target_day))
#else:
#    print(df)



import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import os
from tqdm import tqdm


save_path = "/home/DATA/ymh/s_modeling/redata4"

symbols = pd.read_csv("/home/DATA/ymh/s_modeling/data/data_0430_20210721.csv", encoding='cp949')
symbols = symbols.rename(columns={"단축코드":"Code", "시장구분":"Market"})
symbols = pd.concat([symbols['Code'], symbols['Market']], axis=1)
symbols = symbols[symbols.Market != 'KONEX']
len_stocks = len(symbols) # 종목의 총 개수


df = fdr.DataReader('005930', '2018-01-01', '2021-07-21')
dates = df.index.values
len_dates = len(dates)


standard_date = 13
standard_date += 1

total = 0
cnt = 0
does = 0
mean_profit = 0 

for i in tqdm(range(len_stocks)):
    download_required = True
    while download_required:
        try:
            df_tmp = fdr.DataReader(symbols.iloc[i,0], '2018-01-01', '2021-07-21')
            download_required = False
        except:
            print('%s download error occured. Restart.' % symbols.iloc[i,0])
            download_required = True
    
    for j in range(len_dates-standard_date):
        year = str(dates[j])[:4]
        month = str(dates[j])[5:7]
        day = str(dates[j])[8:10]
        
        newday_path = os.path.join(save_path, year, month, day)
        os.makedirs(newday_path, exist_ok=True)
        
        df_specific = df_tmp.loc[:dates[j+standard_date-1]]

        #onedata = np.zeros((35,1))
                        
        if df_specific.empty:
            pass
        else:
            if len(df_specific) < standard_date:
                pass
            else:
                '''
                onedata[0,0] = df_specific.iloc[-(1+3),0] # Open
                onedata[1,0] = df_specific.iloc[-(1+3),1] # High
                onedata[2,0] = df_specific.iloc[-(1+3),2] # Low
                onedata[3,0] = df_specific.iloc[-(1+3),3] # Close
                onedata[4,0] = df_specific.iloc[-(1+3),4] # Volume
                        
                onedata[5,0] = df_specific.iloc[-(3+3):,0].mean() # 3일 Open 단순 평균
                onedata[6,0] = df_specific.iloc[-(3+3):,1].mean() # 3일 High 단순 평균
                onedata[7,0] = df_specific.iloc[-(3+3):,2].mean() # 3일 Low 단순 평균
                onedata[8,0] = df_specific.iloc[-(3+3):,3].mean() # 3일 Close 단순 평균
                onedata[9,0] = df_specific.iloc[-(3+3):,4].mean() # 3일 Volume 단순 평균
                    
                onedata[10,0] = df_specific.iloc[-(5+3):,0].mean() # 5일 Open 단순 평균
                onedata[11,0] = df_specific.iloc[-(5+3):,1].mean() # 5일 High 단순 평균
                onedata[12,0] = df_specific.iloc[-(5+3):,2].mean() # 5일 Low 단순 평균
                onedata[13,0] = df_specific.iloc[-(5+3):,3].mean() # 5일 Close 단순 평균
                onedata[14,0] = df_specific.iloc[-(5+3):,4].mean() # 5일 Volume 단순 평균
                    
                onedata[15,0] = df_specific.iloc[-(10+3):,0].mean() # 10일 Open 단순 평균
                onedata[16,0] = df_specific.iloc[-(10+3):,1].mean() # 10일 High 단순 평균
                onedata[17,0] = df_specific.iloc[-(10+3):,2].mean() # 10일 Low 단순 평균
                onedata[18,0] = df_specific.iloc[-(10+3):,3].mean() # 10일 Close 단순 평균
                onedata[19,0] = df_specific.iloc[-(10+3):,4].mean() # 10일 Volume 단순 평균
                    
                onedata[20,0] = df_specific.iloc[-(20+3):,0].mean() # 20일 Open 단순 평균
                onedata[21,0] = df_specific.iloc[-(20+3):,1].mean() # 20일 High 단순 평균
                onedata[22,0] = df_specific.iloc[-(20+3):,2].mean() # 20일 Low 단순 평균
                onedata[23,0] = df_specific.iloc[-(20+3):,3].mean() # 20일 Close 단순 평균
                onedata[24,0] = df_specific.iloc[-(20+3):,4].mean() # 20일 Volume 단순 평균
                        
                onedata[25,0] = df_specific.iloc[-(60+3):,0].mean() # 60일 Open 단순 평균
                onedata[26,0] = df_specific.iloc[-(60+3):,1].mean() # 60일 High 단순 평균
                onedata[27,0] = df_specific.iloc[-(60+3):,2].mean() # 60일 Low 단순 평균
                onedata[28,0] = df_specific.iloc[-(60+3):,3].mean() # 60일 Close 단순 평균
                onedata[29,0] = df_specific.iloc[-(60+3):,4].mean() # 60일 Volume 단순 평균
                    
                onedata[30,0] = df_specific.iloc[-(120+3):,0].mean() # 120일 Open 단순 평균
                onedata[31,0] = df_specific.iloc[-(120+3):,1].mean() # 120일 High 단순 평균
                onedata[32,0] = df_specific.iloc[-(120+3):,2].mean() # 120일 Low 단순 평균
                onedata[33,0] = df_specific.iloc[-(120+3):,3].mean() # 120일 Close 단순 평균
                onedata[34,0] = df_specific.iloc[-(120+3):,4].mean() # 120일 Volume 단순 평균
                '''
                total += 1
                
                past10 = df_specific.iloc[-9:-4,3].mean()
                day10 = df_specific.iloc[-4,3]
                
                if past10 * 1.1 <= day10:
                    cnt += 1
                    
                    Open = df_specific.iloc[-3,0] # Open
                    High = df_specific.iloc[-3:,1].max() # High
                    Close = df_specific.iloc[-1,3] # Close
                    
                    if Open == 0:
                        continue
                    
                    if Open < High:
                        onedata = df_specific.iloc[-9:-3,:].to_numpy()
                        
                        maximum = ((High-Open)/Open)*100
                        if maximum < 2:
                            profit = ((Close-Open)/Open)*100
                            buy = 0
                        else:
                            profit = 2
                            does += 1
                            buy = 1
                        
                        mean_profit += profit
                        
                        profit = ((High-Open)/Open)*100
                        loss = ((Close-Open)/Open)*100
                        name = os.path.join(newday_path,"input_%s_%d_%f_%f_" % (symbols.iloc[i,0], buy, profit, loss))
                        np.save(name, onedata)
            
                        f = open("/home/DATA/ymh/s_modeling/redata4/names.txt",'a')
                        name = str(name) + ".npy\n"
                        f.write(name)
                        f.close()
                
                
                '''
                Open1 = df_specific.iloc[-(1+2),0] # Open
                #Open2 = df_specific.iloc[-(1+1),0] # Open
                #Open3 = df_specific.iloc[-(1+0),0] # Open
                
                High1 = df_specific.iloc[-(1+2),1] # High
                High2 = df_specific.iloc[-(1+1),1] # High
                High3 = df_specific.iloc[-(1+0),1] # High
                    
                Close1 = df_specific.iloc[-(1+2),3] # Close
                Close2 = df_specific.iloc[-(1+1),3] # Close
                Close3 = df_specific.iloc[-(1+0),3] # Close
                
                if Open1 != 0:
                    profit11 = ((High1-Open1)/Open1)*100
                    profit21 = ((High2-Open1)/Open1)*100
                    profit31 = ((High3-Open1)/Open1)*100
                    loss11 = ((Close1-Open1)/Open1)*100
                    loss21 = ((Close2-Open1)/Open1)*100
                    loss31 = ((Close3-Open1)/Open1)*100
                    
                    if profit11 >= 5:
                        buy = 1
                        profit = profit11
                        loss = loss11
                    elif profit21 >= 5:
                        buy = 1
                        profit = profit21
                        loss = loss21
                    elif profit31 >= 5:
                        buy = 1
                        profit = profit31
                        loss = loss31
                    else:
                        buy = 0
                        profit = max(profit11, profit21, profit31)
                        loss = loss31
                else:
                    buy = 0
                    profit = 0
                    loss = 0
                '''
                
                '''
                    
                else:
                    profit11 = 0
                    profit21 = 0
                    profit31 = 0
                    loss11 = 0
                    loss21 = 0
                    loss31 = 0
                    
                if Open2 != 0:
                    profit22 = ((High2-Open2)/Open2)*100
                    profit32 = ((High3-Open2)/Open2)*100
                    loss22 = ((Close2-Open2)/Open2)*100
                    loss32 = ((Close2-Open2)/Open2)*100
                else:
                    profit22 = 0
                    profit32 = 0
                    loss22 = 0
                    loss32 = 0
                    
                if Open3 != 0:
                    profit33 = ((High3-Open3)/Open3)*100
                    loss33 = ((Close3-Open3)/Open3)*100
                else:
                    profit33 = 0
                    loss33 = 0
                    
                
                profits = np.array([profit11, profit21, profit31, profit22, profit32, profit33])
                
                if np.argmax(profits) == 0:
                    if profit11 >= 2:
                        buy = 1
                    else:
                        buy = 0
                    profit = profit11
                    loss = loss11
                elif np.argmax(profits) == 1:
                    if profit21 >= 4:
                        buy = 2
                    else:
                        buy = 0
                    profit = profit21
                    loss = loss21
                elif np.argmax(profits) == 2:
                    if profit31 >= 6:
                        buy = 3
                    else:
                        buy = 0
                    profit = profit31
                    loss = loss31
                else:
                    buy = 0
                    profit = max(profit11, profit21, profit31)
                    loss = loss31
                '''
                
                
                
                '''
                name = os.path.join(newday_path,"input_%s_%d_%f_%f_" % (symbols.iloc[i,0], buy, profit, loss))
                np.save(name, onedata)
            
                f = open("/home/DATA/ymh/s_modeling/redata2/names.txt",'a')
                name = str(name) + ".npy\n"
                f.write(name)
                f.close()
                '''


print(total)
print(cnt)
print(does)

mean_profit /= does

print(mean_profit)




























