#Creation of the databse via Python
# You have to remember that every 24 hours the whale.py script deletes all the data from the databe to keep it clean and more efficient

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost", # Insert your host
  user="root", # Insert your user
  password="asir1", # Insert your password 
  database="oasis_database" # Insert your database, if you follow the example bellow the database would be 'oasis_database'

)

''' Creation of the the database, table and columns

mycursor.execute("CREATE DATABASE oasis_database")

mycursor.execute("CREATE TABLE datos (oasis_from VARCHAR(255), amount DECIMAL(32,2), time VARCHAR(16), price DECIMAL(32,2))")

'''

''' We commit 2 examples of data strings to check if the database works

sql = "INSERT INTO datos (oasis_from, amount, time) VALUES (%s, %s, %s, %s)"
val = ("oasis1qzwfdgpt3p6dd2mk6207qhf9qrxuvfn9eunurdgu", "4867.90", "10:58:07", "2000")
mycursor.execute(sql, val)

mydb.commit()

sql = "INSERT INTO datos (oasis_from, amount, time) VALUES (%s, %s, %s)"
val = ("oasis1qzwfdgpt3p6dd2mk6207qhf9qrxuvfn9eunurdgu", "3867.90", "10:58:10", "4000")
mycursor.execute(sql, val)

mydb.commit()

'''


''' Here we can see the first the highest transaction of the database

mycursor.execute("SELECT * FROM datos ORDER BY amount DESC")

myresult = mycursor.fetchall()

print(myresult[0])

'''
