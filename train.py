import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
import torch.optim as optim
import os
from tqdm import tqdm
import numpy as np

from Dataset import forautoset
from architecture import HB_transformer as net

save_path = "/home/DATA/ymh/s_modeling/redata/model_save"
##############################################################################################################################
input_path = "/home/DATA/ymh/s_modeling/redata"

dataset = forautoset(input_path)

total = dataset.len
n_train_sample = int(total*0.8)

##############################################################################################################################
device = torch.device("cuda:0")
#criterion = nn.BCELoss()
criterion = nn.CrossEntropyLoss()

for test_idx in range(5):
    print("="*100)
    indices = list(range(total))
    np.random.shuffle(indices)

    train_idx = indices[:n_train_sample]
    valid_idx = indices[n_train_sample:]

    train_sampler = SubsetRandomSampler(train_idx)
    valid_sampler = SubsetRandomSampler(valid_idx)
    n_val_sample = len(valid_idx)

    train_loader = DataLoader(dataset=dataset, batch_size=8192, sampler=train_sampler, num_workers=32)
    valid_loader = DataLoader(dataset=dataset, batch_size=8192, sampler=valid_sampler, num_workers=32)
        
    model = net((6,5), output=4)
    model.to(device)

    optimizer = optim.Adam(model.parameters(), lr=0.004)
    
    print("="*100)
    best_profit = 0
    for epoch in range(80):
        running_loss=0
        model.train()
        for x, y, _, _ in tqdm(train_loader):
            x = x.float().to(device)
            #y = y.float().to(device)
            y = y.long().to(device)

            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()
        
            running_loss += loss.item()
            #print(loss.item())
            
        running_loss /= len(train_loader)
    
        if (epoch+1) % 1 == 0:
            model.eval()

            correct = 0
            mean_profit = 0
            mean_stop = 0
            buy_cnt = 0
            
            for x, y, profit, stop in tqdm(valid_loader):
                x = x.float().to(device)
                y = y.float().to(device)
                profit = profit.float().to(device)
                stop = stop.float().to(device)
    
                with torch.no_grad():
                    output = model(x)
    
                pred = output.argmax(1)
                correct += pred.eq(y).sum().item()
                
                mean_profit += profit[pred >= 1].sum().item()
                mean_stop += stop[pred >= 1].sum().item()
                buy_cnt += (pred >= 1).sum().item()
                
            accuracy = correct / len(valid_loader.dataset)
            
            if buy_cnt > 0:
                mean_profit = mean_profit/buy_cnt
                mean_stop = mean_stop/buy_cnt
            else:
                mean_profit = 0
                mean_stop = 0
                
            print("[Epoch:%d] [Loss:%f]" % ((epoch+1), running_loss), end=" ")
            print("[Accuracy:%f]" % accuracy, end=" ")
            print("[Profit:%f]" % mean_profit, end=" ")
            print("[Stop:%f]" % mean_stop)
            
            #if precision >= best_precision:
            if (epoch+1) > 10 and mean_profit >= best_profit:
                model_name = os.path.join(save_path, "input_redata_test_%02d.pth" % test_idx)
                torch.save({'model_state_dict': model.state_dict()}, model_name)
                print("model saved.")
                #best_precision = precision
                best_profit = mean_profit