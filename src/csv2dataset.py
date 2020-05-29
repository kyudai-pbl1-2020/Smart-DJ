import csv
import glob
import pandas as pd

# csvのファイルパスからデータを収集し，データのリストに変換する
def csv2list(path):
    with open(path) as f:
        reader = csv.reader(f)
        datalist = []
        for row in reader:
            # 0:年月日時 1:気温 4:気圧 7:天気 10:湿度
            # 天気があるやつだけ
            if (row[7] != ''):
                datalist.append([int(row[0].split()[0].split('/')[1]), int(row[0].split()[1].split(':')[0]), int(row[7]), float(row[1]), float(row[4]), int(row[10])])

        return datalist

# 学習用のデータ.csvを含むディレクトリのパスを受けとり，dataframeに変換する
def dataframe_exporter(path):
    path_list = glob.glob(path)
    list_list = []
    for csv_path in path_list:
        list_list = list_list + csv2list(csv_path)
    return pd.DataFrame(list_list, columns=['month', 'hour', 'weather', 'temperature', 'pressure', 'humidity'])

# print(dataframe_exporter("weather_data/*"))