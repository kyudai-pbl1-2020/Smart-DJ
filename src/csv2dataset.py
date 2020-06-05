# In[0]:
import csv
import glob
import pandas as pd

# In[1]:
def read_weather_token(path):
    with open(path) as f:
        reader = csv.reader(f)
        weather_dict = {}
        for row in reader:
            weather_dict[int(row[0])] = row[1]
        
        return weather_dict

# print (read_weather_token("weather_token.csv"))

# In[2]: change scv to list
def csv2list(path):
    with open(path) as f:
        reader = csv.reader(f)
        datalist = []
        for row in reader:
            # 0:ymdt 1:temperature 4:barometric pressure 7:weather 10:humidity
            # append only including weather
            if (row[7] != ''):
                datalist.append([int(row[0].split()[0].split('/')[1]), int(row[0].split()[1].split(':')[0]), int(row[7]), float(row[1]), float(row[4]), int(row[10])])

        return datalist

# In[3]: make dataframe from csv directory path
def dataframe_exporter(path):
    path_list = glob.glob(path)
    list_list = []
    for csv_path in path_list:
        list_list = list_list + csv2list(csv_path)
    return pd.DataFrame(list_list, columns=['month', 'hour', 'weather', 'temperature', 'pressure', 'humidity'])

# print(dataframe_exporter("weather_data/*"))

# In[4]:
def change_weather(data_frame, path):
    convertion_dict = {}
    with open(path) as f:
        reader = csv.reader(f)
        weather_dict = {}
        for row in reader:
            weather_dict[int(row[0])] = int(row[1])
        
        convertion_dict = weather_dict
    return data_frame.replace({'weather': convertion_dict})

# change_weather(dataframe_exporter("weather_data/*"), "convert_weather_token.csv")