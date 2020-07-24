from sensor import sensor_data_processor as sdp
import mysql.connector

# Dockerを使う場合で、初期設定の場合hostは"192.168.99.100"
# MySQLのユーザやパスワード、データベースはdocker-compose.ymlで設定したもの
connector = mysql.connector.connect(
            user='user',
            password='password',
            host='mysql_db',
            database='sample_db',
            port='3306')

cursor = connector.cursor()
#pred_data = sdp.subscribe_sensor_data()
pred_data = [6,17,27.12,998.2,64.22] #テスト用
cursor.execute("select * from users")

disp = ""
for row in cursor.fetchall():
    disp = "ID:" + str(row[0]) + "  名前:" + row[1]

cursor.close
connector.close

print(disp)