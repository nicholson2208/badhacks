# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 18:27:58 2017

@author: Matt
"""

#time of first shot=
#these are all spaced out at 15 ish second interval 
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

path="test.csv"
whole_thing=pd.read_csv(path)

whole_thing.columns=["time","ax","ay","az","gx","gy","gz","ox","oy","oz","ow"]
whole_thing=whole_thing[500:19000]
start_time=whole_thing["time"].iloc[0]
second_time=whole_thing["time"].iloc[1]
end_time=whole_thing["time"].iloc[-1]

#output=pd.DataFrame(np.zeros((25,9)),columns=["axmax","axmin","axvar","aymax","aymin","azvar", "azmax","azmin","azvar"])
output=pd.DataFrame(np.zeros((125,10)),columns=["gxmax","gxmin","gxvar","gymax","gymin","gzvar", "gzmax","gzmin","gzvar","label"])

labels=pd.read_csv("label.csv")

for j in range(5):
    for i in range(25):
        temp=whole_thing[["gx","gy","gz"]][i*750:750*i+500]
        print(i)
        for dim in ["gx","gy","gz"]:
            output.loc[i+25*(j)][dim+"max"]=np.max(temp[dim])*np.random.normal(loc=1,scale=0.02)
            output.loc[i+25*(j)][dim+"min"]=np.min(temp[dim])*np.random.normal(loc=1,scale=0.02)
            
            output.loc[i+25*(j)][dim+"var"]=np.var((temp[dim].astype("float")))*np.random.normal(loc=1,scale=0.02)
#    plt.plot(whole_thing["ax"][i*750:750*i+500])
            output.loc[i+25*(j)]["label"]=labels["label"].iloc[i]
output.to_csv("gfeature.csv")