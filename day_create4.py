#import subprocess
from datetime import datetime
from pytz import timezone
import time
import os
import pandas as pd
import numpy as np
import gc
import FinanceDataReader as fdr

if __name__ == "__main__":
    save_path = "/home/DATA/ymh/s_modeling/redata"
    symbols = pd.read_csv("/home/DATA/ymh/s_modeling/data/data_0430_20210721.csv", encoding='cp949')
    symbols = symbols.rename(columns={"단축코드":"Code", "시장구분":"Market"})
    symbols = pd.concat([symbols['Code'], symbols['Market']], axis=1)
    symbols = symbols[symbols.Market != 'KONEX']
    len_stocks = len(symbols) # 종목의 총 개수
    
    
    target_year = '2021'
    target_month = '07'
    target_day = '22'
    #newday_path = os.path.join(save_path, target_year, target_month, target_day)
    #os.makedirs(newday_path, exist_ok=True)
    refresh = True
    print("="*20)
    print("Date %s-%s-%s is targeted." % (target_year, target_month, target_day))
    '''
    refresh = False
    '''
    while True:
        now = datetime.now(timezone('Asia/Seoul'))
        format = '%Y-%m-%d %H:%M %p'
        current_time = now.strftime(format)
        
        year = current_time[:4]
        month = current_time[5:7]
        day = current_time[8:10]
        
        hour = current_time[11:13]
        pm = current_time[-2:]
        
        
        if pm == "PM":
            if int(hour) == 18:
                #newday_path = os.path.join(save_path, year, month, day)
                #os.makedirs(newday_path, exist_ok=True)
                target_year = year
                target_month = month
                target_day = day
                refresh = True
                print("="*20)
                print("Date %s-%s-%s is targeted." % (target_year, target_month, target_day))
        
        if refresh:
            print("Refreshing start.")
            recommand_dict = {}
            download_required = True
            while download_required:
                try:
                    df = fdr.DataReader('005930', '2020-01-01', '%s-%s-%s' % (target_year, target_month, target_day))
                    download_required = False
                except:
                    print('Standard download error occured. Restart.')
                    download_required = True
            
            if str(df.index.values[-1])[:10] != '%s-%s-%s' % (target_year, target_month, target_day):
                print("Date is not same.", str(df.index.values[-1])[:10], "and %s-%s-%s" % (target_year, target_month, target_day))
                
            else:            
                for i in range(len_stocks):
                    download_required = True
                    while download_required:
                        try:
                            df_tmp = fdr.DataReader(symbols.iloc[i,0], '2020-01-01', '%s-%s-%s' % (target_year, target_month, target_day))
                            download_required = False
                        except:
                            print('%s download error occured. Restart.' % symbols.iloc[i,0])
                            download_required = True
                        
                    #past10 = df_tmp.iloc[-6:-1,3].mean()
                    past10 = df_tmp.iloc[-2,3].mean()
                    day10 = df_tmp.iloc[-1,3]
                    
                    if past10 * 1.2 <= day10:
                        #print(symbols.iloc[i,0])
                        recommand_dict[symbols.iloc[i,0]] = df_tmp.iloc[-1,3] * df_tmp.iloc[-1,4]
                
                recommand_dict = sorted(recommand_dict.items(), key=(lambda x:x[1]), reverse=True)
                for i in range(min(len(recommand_dict),10)):
                    print(recommand_dict[i])
                
                refresh = False
                print("%s-%s-%s is done." % (target_year, target_month, target_day))
                    
                del df_tmp
            
            del df
            gc.collect()
        
        
        time.sleep(3600)










