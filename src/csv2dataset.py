import csv
import pandas as pd

def csv2list(path):
    with open(path) as f:
        reader = csv.reader(f)
        datalist = []
        for row in reader:
            # 0:年月日時 1:気温 4:気圧 7:天気 10:湿度
            # 天気があるやつだけ
            if (row[7] != ''):
                datalist.append([int(row[0].split()[0].split('/')[1]), int(row[0].split()[1].split(':')[0]), int(row[7]), float(row[1]), float(row[4]), int(row[10])])

        return pd.DataFrame(datalist, columns=['month', 'hour', 'weather', 'temperature', 'pressure', 'humidity'])

def csv2dataframe(path):
    df = pd.read_csv(path, header=None)
    df.drop([2, 3, 5, 6, 8, 9, 11, 12], inplace=True, axis=1)
    return df[df[7].isnull() == False]

print(csv2list('weather_data/data1.csv'))