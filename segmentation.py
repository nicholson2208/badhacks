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

output=pd.DataFrame(np.zeros((25,9)),columns=["axmax","axmin","axvar","aymax","aymin","azvar", "azmax","azmin","azvar"])



for i in range(25):
    temp=whole_thing[["ax","ay","az"]][i*750:750*i+500]
    print(i)
    for dim in ["ax","ay","az"]:
        output.loc[i][dim+"max"]=np.max(temp[dim])
        output.loc[i][dim+"min"]=np.min(temp[dim])
        
        output.loc[i][dim+"var"]=np.var((temp[dim].astype("float")))
#    plt.plot(whole_thing["ax"][i*750:750*i+500])

output.to_csv("feature.csv")