from reader import reader
import pandas as pd
from Functions import  calculate_m, smoothing
import numpy as np
import datetime as dt
import math

full_path = reader(filename="Nayef") #read file is optional the function return the full path of the saved file
proj_init_df = pd.read_csv(full_path)
proj_init_df["timestamp"] =  pd.to_datetime(proj_init_df["date"]+" "+proj_init_df["time"])

def categrizer(row):
    global counter
    if (row["time_diff"] == pd.NaT):
        return np.nan
        counter +=1
    elif (row["time_diff"]>dt.timedelta(minutes = 2)):
        counter +=1
        return np.nan
    return counter
proj_init_df["i"] = 1
calculate_m(proj_init_df,"i")
proj_init_df = proj_init_df[proj_init_df["time_diff"]>dt.timedelta(seconds = 0 )]

counter = 1
proj_init_df["group"]=proj_init_df.apply(categrizer,axis=1)

calculate_m(proj_init_df,"group")
proj_init_df.dropna(inplace = True)

proj_init_df["direction"] = proj_init_df.apply(lambda x: math.atan2(x['lat_diff'], x['lng_diff']), axis=1).apply(math.degrees)
proj_init_df["direction_change"] = proj_init_df.groupby(["group"])["direction"].diff()
proj_init_df["direction_change"] =  proj_init_df["direction_change"].apply(lambda x: abs(x) if abs(x) <180 else 360-abs(x))

smoothing(proj_init_df, ["speed(m/s)","direction_change",'accelerattion' ],end = 10)
proj_init_df.dropna(inplace = True)
proj_init_df.drop(columns = [ "Unnamed: 0",'lat', 'lng', 'timestamp', 'time_diff','lat_diff',
                       'lng_diff','distance','a_c_distance', 
                       'a_b_c_distance', 'group','speed_diff', 'direction',
                       'prev_lat', 'prev_lng',"prev_2_lng",
                       "prev_2_lat","date","time","i"],inplace=True)

speed_df = proj_init_df.loc[:,[col for col in proj_init_df.columns if col[:4] == "spee"]]
dire_df = proj_init_df.loc[:,[col for col in proj_init_df.columns if col[:4] == "dire"]]
acce_df = proj_init_df.loc[:,[col for col in proj_init_df.columns if col[:4] == "acce"]]


a = speed_df.values
a.sort(axis=1)
a = a[:,::-1]
speed_df = pd.DataFrame(a, speed_df.index, speed_df.columns)

a = dire_df.values
a.sort(axis=1)
a = a[:,::-1]
dire_df = pd.DataFrame(a, dire_df.index, dire_df.columns)

a = acce_df.values
a.sort(axis=1)
a = a[:,::-1]
acce_df = pd.DataFrame(a, acce_df.index, acce_df.columns)
proj_init_df = pd.concat([speed_df,dire_df,acce_df],axis=1)
del(speed_df,dire_df,acce_df)
proj_init_df.to_csv("test1.csv")