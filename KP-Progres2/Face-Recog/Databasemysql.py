import mysql.connector

db = mysql.connector.connect(
        host="localhost",
        user="spkapedittelkom", 
        password="spkapedit232629", 
        port = 3307,
        #ssl_disabled=True,  
        database = "sistempresensidit"

)
cursor = db.cursor()

#cursor.execute("CREATE DATABASE sistempresensidit")
cursor.execute("CREATE TABLE presensi (id INT AUTO_INCREMENT PRIMARY KEY,nim VARCHAR(50),name VARCHAR(100),time TIME,day VARCHAR(50),date DATE,year YEAR,status VARCHAR(50))")
db.commit()
db.close()
