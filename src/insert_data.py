from sensor import sensor_data_processor as sdp
import mysql.connector

# Dockerを使う場合で、初期設定の場合hostは"192.168.99.100"
# MySQLのユーザやパスワード、データベースはdocker-compose.ymlで設定したもの
for i in range(0, 4):
    connector = mysql.connector.connect(
                user='user',
                password='password',
                host='mysql_db',
                database='sample_db',
                port='3306')

    cursor = connector.cursor()
    pred_data = sdp.subscribe_sensor_data()
    if (pred_data != []):
        inserted_data = "INSERT INTO users (month,day,temperature,pressure,humidity) VALUES ({}, {}, {}, {}, {});".format(pred_data[0], pred_data[1], pred_data[2], pred_data[3], pred_data[4])
        cursor.execute(inserted_data)
    #pred_data = [6,17,27.12,998.2,64.22] #テスト用
    #pred_data = [7,26,30.12,987.6,78.90] #テスト用2
    

    '''
    cursor.execute("select * from users")
    disp = ""
    for row in cursor.fetchall():
        disp = "ID:" + str(row[0]) + "<br>month:" + str(row[1]) + "<br>day:" + str(row[2]) + "<br>temperature:" + str(row[3]) + "<br>pressure:" + str(row[4]) + "<br>humidity:" + str(row[5])
    print(disp)
    '''

    cursor.close
    connector.commit()
    connector.close
