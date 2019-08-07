import pandas as pd
import numpy as np
import datetime as dt

def calculate_m(df, group):
    """that function take a data frame and caculate all the featuers based on the gps signals"""
    
    df["time_diff"] = df.groupby(group)["timestamp"].diff()
    df["lat_diff"]  = df.groupby([group])["lat"].diff()
    df["lng_diff"]  = df.groupby([group])["lng"].diff()
    df["distance"]  = (df["lat_diff"]**2 + df["lng_diff"]**2)**0.5 *100000/1.1132
    df["speed(m/s)"]= df["distance"]/df.time_diff.astype("timedelta64[s]")
    df["prev_lat"]  = np.where(df[group] == df[group].shift(),df["lat"].shift(),np.nan)
    df["prev_lng"]  = np.where(df[group] == df[group].shift(),df["lng"].shift(),np.nan)
    df["prev_2_lng"]  = np.where(df[group] == df[group].shift(2),df["lng"].shift(2),np.nan)
    df["prev_2_lat"]  = np.where(df[group] == df[group].shift(2),df["lat"].shift(2),np.nan)
    df["a_c_distance"]  = ((df["lat"]-df["prev_2_lat"])**2 + (df["lng"]-df["prev_2_lng"])**2 )**0.5 *100000/1.1132
    df["a_b_c_distance"] =   np.where(df[group] == df[group].shift(),df["distance"]+df["distance"].shift(),np.nan)
    df["speed_diff"] =      df.groupby([group])["speed(m/s)"].diff()
    df["accelerattion"] = df["speed_diff"]/df["time_diff"].astype("timedelta64[s]")
    



def reset_col(df):
    """that function remove all the features added to the data frame"""
    df = df[ 'lat', 'lng', 'timestamp']
    
def smoothing(df, columns,start = 0, end = 5 ,alpha = 0.0):
    for col in columns:
        for i in range(start,end):
            df[f"{col}{'_smoothed_'}{str(i+1)}"]= (
                np.where((df["group"]==df["group"].shift(i+1)),
             df[f"{col}{'_smoothed_'*(int(bool(i)))}{str(i) if i >0 else ''}"]*alpha 
                          + df[col].shift(i+1)*(1-alpha)               
             ,np.nan)
)
                
def categrizer(row):
    global counter
    if (row["time_diff"] == pd.NaT):
        return np.nan
        counter +=1
    elif (row["time_diff"]>dt.timedelta(minutes = 2)):
        counter +=1
        return np.nan
    return counter

def print_confusion_matrix(confusion_matrix, class_names, figsize = (9,5), fontsize=18):
    df_cm = pd.DataFrame(confusion_matrix, index=class_names, columns=class_names, )
    fig = plt.figure(figsize=figsize)
    try:
        heatmap = sns.heatmap(df_cm, annot=True, fmt="d")
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=fontsize)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=fontsize)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig