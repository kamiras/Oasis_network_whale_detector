import requests
import json
import time
from datetime import datetime
import tweepy
import keys
import mysql.connector
from kucoin.client import Market
import gc

mydb = mysql.connector.connect(
  host="", # Insert your host
  user="", # Insert your user
  password="", # Insert your password 
  database="" # Insert your database, if you follow the example bellow the database would be 'oasis_database'

)

mycursor = mydb.cursor()

client = tweepy.Client(consumer_key=keys.API_KEY,
                        consumer_secret=keys.API_SECRET,
                        access_token=keys.ACCES_TOKEN,
                        access_token_secret=keys.ACCES_TOKEN_SECRET)

link1 ='https://api.oasisscan.com/mainnet/chain/transactions?method=staking.Transfer&page=1&runtime=true&size=1'
link2 ='https://api.coinbase.com/v2/prices/ROSE-USD/buy'
link3 = 'https://api.kucoin.com'

def rose_api():

    try:

        response_API = requests.get(link1)
        data = response_API.text
        parse_json = json.loads(data)
        result1 = parse_json['data']['list'][0]['amount']
        result2 = parse_json['data']['list'][0]['txHash']
        result3 = parse_json['data']['list'][0]['from']
        result4 = parse_json['data']['list'][0]['to']

        return result1, result2, result3, result4, True

    except:

        pass

def rose_price_coinbase_api():

    try:

        response_API = requests.get(link2)
        data = response_API.text
        parse_json = json.loads(data)
        result = parse_json['data']['amount']
        return result, True

    except:

        pass

def rose_price_kucoin_api():

    try:

        ticker = requests.get(link3 + '/api/v1/market/orderbook/level1?symbol=ROSE-USDT').json()
        result = ticker['data']['price']
        return result, True

    except:

        pass

def comprobaciones(rose_api_variable3, rose_api_variable4):

    with open("pub_keys.txt","r") as e:

        for line in e:

            if (line.strip("\n").split(":")[1] == rose_api_variable3):

                rose_api_variable3 = line.split(":")[0]

            elif(line.strip("\n").split(":")[1] == rose_api_variable4):

                rose_api_variable4 = line.split(":")[0]

    return rose_api_variable3, rose_api_variable4

num = 0
auxiliar = ""

while True:

    try:

        time.sleep(0.5)

        rose_api_variable1, rose_api_variable2, rose_api_variable3, rose_api_variable4, rose_api_variable5 = rose_api()
        rose_price_variable1, rose_price_variable2 = rose_price_kucoin_api() # The kucoin API is more accurate than the rose_price_coinbase_api() API, but you can change it if you want.

        if (rose_api_variable5 == True and rose_price_variable2 == True):

            dolar_cost = float(rose_price_variable1) * float(rose_api_variable1)

            if (datetime.now().strftime("%H:%M") == "22:00"):

                    mycursor.execute("SELECT * FROM datos ORDER BY amount DESC LIMIT 3")

                    myresult = mycursor.fetchall()

                    if len(myresult) == 3:

                      client.create_tweet(text='''
                      Top 3 Transactions of the day\n
                      1🏆 {0} ROSE ({1} USD) {2} EU\n
                      2🥈 {3} ROSE ({4} USD) {5} EU\n
                      3🥉 {6} ROSE ({7} USD) {8} EU\n
                      \n$ROSE #OasisNetwork'''
                      
                      .format(

                      myresult[0][1], format(float(rose_price_variable1) * int(myresult[0][1]), ".2f"),myresult[0][2],
                      myresult[1][1], format(float(rose_price_variable1) * int(myresult[1][1]), ".2f"),myresult[1][2],
                      myresult[2][1], format(float(rose_price_variable1) * int(myresult[2][1]), ".2f"),myresult[2][2])
                          
                      )

                    elif len(myresult) == 2:

                      client.create_tweet(text='''
                      Top 2 Transactions of the day\n
                      1🏆 {0} ROSE ({1} USD) {2} EU\n
                      2🥈 {3} ROSE ({4} USD) {5} EU\n
                      \n$ROSE #OasisNetwork'''
                      
                      .format(

                      myresult[0][1], format(float(rose_price_variable1) * int(myresult[0][1]), ".2f"),myresult[0][2],
                      myresult[1][1], format(float(rose_price_variable1) * int(myresult[1][1]), ".2f"),myresult[1][2])
                          
                      )

                    elif len(myresult) == 1:

                      client.create_tweet(text='''
                      Top 1 Transactions of the day\n
                      1🏆 {0} ROSE ({1} USD) {2} EU\n
                      \n$ROSE #OasisNetwork'''
                      
                      .format(

                      myresult[0][1], format(float(rose_price_variable1) * int(myresult[0][1]), ".2f"),myresult[0][2])
                          
                      )

                    else:

                        pass
                      

                    sql = "DELETE FROM datos"

                    mycursor.execute(sql)

                    mydb.commit()


            if (dolar_cost >= 25000): # The transactions that are going to be submited 1:1 USD. In this example only transactions over 100K dollars will be processed

                if (num == 0):

                        rose_api_variable_result3, rose_api_variable_result4 = comprobaciones(rose_api_variable3, rose_api_variable4)

                        client.create_tweet(text='{0} ROSE ({1} USD) transfered 𝗳𝗿𝗼𝗺 {2} 𝘁𝗼 {3}\n $ROSE #OasisNetwork'.format(rose_api_variable1, format(dolar_cost, ".2f"), rose_api_variable_result3, rose_api_variable_result4))

                        sql = "INSERT INTO datos (oasis_from, amount, time) VALUES (%s, %s, %s)"
                        val = (rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"))
                        mycursor.execute(sql, val)

                        mydb.commit()

                        auxiliar = rose_api_variable2         

                elif(num >= 1 and auxiliar != rose_api_variable2):

                        rose_api_variable_result3, rose_api_variable_result4 = comprobaciones(rose_api_variable3, rose_api_variable4)

                        client.create_tweet(text='{0} ROSE ({1} USD) transfered 𝗳𝗿𝗼𝗺 {2} 𝘁𝗼 {3}\n $ROSE #OasisNetwork'.format(rose_api_variable1, format(dolar_cost, ".2f"), rose_api_variable_result3, rose_api_variable_result4))

                        sql = "INSERT INTO datos (oasis_from, amount, time) VALUES (%s, %s, %s)"
                        val = (rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"))
                        mycursor.execute(sql, val)

                        mydb.commit()

                        auxiliar = rose_api_variable2

                num += 1

            del rose_api_variable1,rose_api_variable2,rose_price_variable1,dolar_cost, rose_api_variable5, rose_price_variable2
            gc.collect()

    except:

        pass

    
