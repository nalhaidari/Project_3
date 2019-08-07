def reader(gps_data_file="/Users/nayefalhaidari/Documents/Proj_3_repo/Project_3/my gps data.txt",filename = "test"):
    import pandas as pd 
    from bs4 import BeautifulSoup
    import numpy as np
    with open(gps_data_file,'r') as file:
        page = file.read()    
    soup = BeautifulSoup(page,"lxml")
    data = []
    for j in soup.find_all("trkpt"): 
        i =str(j)
        start = 5+i.find('lat="')
        end = i[start+1:].find('"')
        lat = float(i[start:start+end])
        start = 5+i.find('lon="')
        end = i[start+1:].find('"')
        lng = float(i[start:start+end])
        start = 6+i.find('<time>')
        end = i[start+1:].find('.')
        date , time = i[start:start+end].split("T")
        data.append([lat,lng,date,time])
    df = pd.DataFrame(np.array(data), columns=["lat","lng","date","time"])
    df["timestamp"] =  pd.to_datetime(df["date"]+" "+df["time"])
    df.lng = df.lng.astype("float")
    df.lat = df.lat.astype("float")
    df.to_csv("~/Documents/Proj_3_repo/Project_3/"+filename+".csv")
    return ("~/Documents/Proj_3_repo/Project_3/"+filename+".csv")
