#import subprocess
from datetime import datetime
from pytz import timezone
import time
import os
import pandas as pd
import numpy as np
import gc
import FinanceDataReader as fdr
from tqdm import tqdm

if __name__ == "__main__":
    save_path = "/home/DATA/ymh/s_modeling/redata"
    symbols = pd.read_csv("/home/DATA/ymh/s_modeling/data/data_0430_20210721.csv", encoding='cp949')
    symbols = symbols.rename(columns={"단축코드":"Code", "시장구분":"Market"})
    symbols = pd.concat([symbols['Code'], symbols['Market']], axis=1)
    symbols = symbols[symbols.Market != 'KONEX']
    len_stocks = len(symbols) # 종목의 총 개수
    
    df = fdr.DataReader('005930', '2018-01-01', '2021-07-21')
    dates = df.index.values
    len_dates = len(dates)
    
    standard_date = 8
    standard_date += 1

    total = 0
    cnt = 0
    does = 0
    mean_profit = 0
    cum_recom = 0
    cum_correct = 0
    
    for i in range(len_dates-3):
        
        target_year = str(dates[i+3])[:4]
        target_month = str(dates[i+3])[5:7]
        target_day = str(dates[i+3])[8:10]
        
        recommand_dict = {}
        result_dict = {}
        
        for j in tqdm(range(len_stocks)):
            
            download_required = True
            while download_required:
                try:
                    df_tmp = fdr.DataReader(symbols.iloc[j,0], '2017-12-01', '%s-%s-%s' % (target_year, target_month, target_day))
                    download_required = False
                except:
                    print('%s download error occured. Restart.' % symbols.iloc[i,0])
                    download_required = True
            
            if df_tmp.empty:
                pass
            else:
                if len(df_tmp) < standard_date:
                    pass
                else:
                    total += 1
                
                    past10 = df_tmp.iloc[-9:-4,3].mean()
                    #past10 = df_tmp.iloc[-5,3]
                    day10 = df_tmp.iloc[-4,3]
                
                    if past10 * 1.2 <= day10:
                        cnt += 1
                        
                        Open = df_tmp.iloc[-3,0] # Open
                        High = df_tmp.iloc[-3:,1].max() # High
                        Close = df_tmp.iloc[-1,3] # Close
                    
                        if Open == 0:
                            continue
                        else:
                            recommand_dict[symbols.iloc[j,0]] = df_tmp.iloc[-4,3] * df_tmp.iloc[-4,4]
                    
                        if Open < High:
                            
                            maximum = ((High-Open)/Open)*100
                            if maximum < 2:
                                result_dict[symbols.iloc[j,0]] = maximum
                            else:
                                result_dict[symbols.iloc[j,0]] = 1
                        
                            #mean_profit += profit
                        
                        else:
                            result_dict[symbols.iloc[j,0]] = ((Close-Open)/Open)*100
                        
        recommand_dict = sorted(recommand_dict.items(), key=(lambda x:x[1]), reverse=True)
        recom = min(len(recommand_dict),10)
        if recom != 0:
            correct = 0
            for k in range(min(len(recommand_dict),10)):
                if result_dict[recommand_dict[k][0]] == 1:
                    correct += 1
                else:
                    print(k, result_dict[recommand_dict[k][0]])
        
            print(correct/recom)

            cum_recom += recom
            cum_correct += correct

    print(cum_correct/cum_recom)





