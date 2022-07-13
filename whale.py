import requests
import json
import time
from datetime import datetime, date
import tweepy
import keys
import mysql.connector
from kucoin.client import Market
import gc
import matplotlib.pyplot as plt
import numpy as np
import os
import traceback

client = tweepy.Client(consumer_key=keys.API_KEY,
                        consumer_secret=keys.API_SECRET,
                        access_token=keys.ACCES_TOKEN,
                        access_token_secret=keys.ACCES_TOKEN_SECRET)

auth = tweepy.OAuthHandler(
            keys.API_KEY,
            keys.API_SECRET
            )

auth.set_access_token(
            keys.ACCES_TOKEN,
            keys.ACCES_TOKEN_SECRET
            )

api = tweepy.API(auth)

def mysql_database_insert(data1, data2, data3, data4):

    mydb = mysql.connector.connect(
    host="localhost", # Insert your host
    user="root", # Insert your user
    password="", # Insert your password
    database="oasis_database" # Insert your database, if you follow the example bellow the database would be 'oasis_database'

                )

    mycursor = mydb.cursor()
    sql = "INSERT INTO datos (oasis_from, amount, time, price) VALUES (%s, %s, %s, %s)"
    val = (data1, data2, data3, data4)
    mycursor.execute(sql, val)

    mydb.commit()

def mysql_database_top():

    mydb = mysql.connector.connect(
    host="localhost", # Insert your host
    user="root", # Insert your user
    password="", # Insert your password
    database="oasis_database" # Insert your database, if you follow the example bellow the database would be 'oasis_database'

                )

    mycursor = mydb.cursor()

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

        myresult[0][1], myresult[0][3], myresult[0][2],
        myresult[1][1], myresult[1][3], myresult[1][2],
        myresult[2][1], myresult[2][3], myresult[2][2])
                          
        )

    elif len(myresult) == 2:

            client.create_tweet(text='''
            Top 2 Transactions of the day\n
            1🏆 {0} ROSE ({1} USD) {2} EU\n
            2🥈 {3} ROSE ({4} USD) {5} EU\n
            \n$ROSE #OasisNetwork'''
                      
            .format(

            myresult[0][1], myresult[0][3], myresult[0][2],
            myresult[1][1], myresult[1][3], myresult[1][2])
                          
            )

    elif len(myresult) == 1:

            client.create_tweet(text='''
            Top 1 Transaction of the day\n
            1🏆 {0} ROSE ({1} USD) {2} EU\n
            \n$ROSE #OasisNetwork'''
                      
            .format(

            myresult[0][1], myresult[0][3], myresult[0][2])
                          
                      )

    else:

            pass

    sql = "DELETE FROM datos"
    mycursor.execute(sql)
    mydb.commit()
    time.sleep(60)

link1 = 'https://api.oasisscan.com/mainnet/chain/transactions?method=staking.Transfer&page=1&runtime=true&size=1'
link2 = 'https://api.coinbase.com/v2/prices/ROSE-USD/buy'
link3 = 'https://api.kucoin.com'
link4 = 'https://api.oasisscan.com/mainnet/validator/list?orderBy=escrow&page=1&pageSize=10&sort=desc'
link5 = "https://api.twitter.com/2/tweets/search/recent?query=from%3Aoasis_whale"

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

    try:

        with open("pub_keys.txt","r") as e:

            for line in e:

                if (line.strip("\n").split(":")[1] == rose_api_variable3):

                    rose_api_variable3 = line.split(":")[0]

                elif(line.strip("\n").split(":")[1] == rose_api_variable4):

                    rose_api_variable4 = line.split(":")[0]

        return rose_api_variable3, rose_api_variable4

    except:

        pass

def rose_api_staking():

    try:

        response_API = requests.get(link4)
        data = response_API.text
        parse_json = json.loads(data)

        names = []
        escrow = []
        graphic_colors = ["#EAECEE", "#D5D8DC", "#D5D8DC", "#ABB2B9" ,"#808B96" ,"#566573", "#2C3E50", "#273746", "#212F3D", "#1C2833"]

        for i in range(0, 10):

            if (parse_json['data']['list'][i]['name'] == None):

                names.append('NoName')

            else:

                names.append(parse_json['data']['list'][i]['name'])

            escrow.append(int(float(parse_json['data']['list'][i]['escrow'])))
        
        plt.rcParams["figure.figsize"] = (8, 4.7)
        figure=plt.figure()
        axes = figure.add_subplot()
        axes.set_title("Top 10 Validators of Oasis Network", fontsize=20,pad=10,color="#011119", fontweight ="bold")
        plt.pie(escrow, labels=names, autopct='%0.f%%', shadow=True, startangle=90, colors = graphic_colors)
        axes.legend(escrow, loc='center', bbox_to_anchor=(-0.395, 0.52))
        plt.text(-2.225, 0.85, "Amount of ROSE", horizontalalignment='center')
        plt.text(2.3, -1.5, datetime.date(datetime.now()), horizontalalignment='center')
        #plt.show()
        plt.savefig('./images/{}.png'.format(datetime.date(datetime.now())))

        return './images/{}.png'.format(datetime.date(datetime.now()))

    except:

        pass

def twitter_account():

    try:

        headers={'Authorization':'Bearer ' + keys.EXTRA_BEARER_CODE}

        response_API = requests.get(link5, headers=headers)
        data = response_API.text
        parse_json = json.loads(data)
        result1 = parse_json['data'][0]['text']

        return result1

    except:

        pass

def errors():

    try:

        with open("exceptions.log", "a") as logfile:
                    traceback.print_exc(file=logfile)
                    logfile.write(str(datetime.now()) + "\n\n")

    except:

        pass
    
auxiliar = ""

while True:

    try:

        rose_api_variable1, rose_api_variable2, rose_api_variable3, rose_api_variable4, rose_api_variable5 = rose_api()

        try:

            rose_price_variable1, rose_price_variable2 = rose_price_coinbase_api() # The kucoin API is more accurate than the rose_price_coinbase_api() API, but you can change it if you want.

        except: # If the kucoin API fails use the coinbase API

            rose_price_variable1, rose_price_variable2 = rose_price_kucoin_api()

        if (rose_api_variable5 == True and rose_price_variable2 == True):

            dolar_cost = float(rose_price_variable1) * float(rose_api_variable1)

            if (datetime.now().strftime("%H:%M") == "22:00"):

                    mysql_database_top()

            if (date.today().weekday() == 5 and datetime.now().strftime("%H:%M") == "20:00"):
        
                path = rose_api_staking()
                media = api.media_upload(path)
                tweet = "Weekly Validator Top $ROSE #OasisNetwork"
                post_result = api.update_status(status=tweet, media_ids=[media.media_id])
                os.remove('./images/{}.png'.format(datetime.date(datetime.now())))
                time.sleep(60)


            if (dolar_cost >= 60000): # The transactions that are going to be submited 1:1 USD. In this example only transactions over 25K dollars will be processed

                if auxiliar != rose_api_variable2:

                    rose_api_variable_result3, rose_api_variable_result4 = comprobaciones(rose_api_variable3, rose_api_variable4)

                    last_tweet = twitter_account()

                    client_text = '{0} ROSE ({1} USD) transfered 𝗳𝗿𝗼𝗺 {2} 𝘁𝗼 {3}\n $ROSE #OasisNetwork'.format(rose_api_variable1, format(dolar_cost, ".2f"), rose_api_variable_result3, rose_api_variable_result4)

                    if (rose_api_variable_result3[0] == "#" and rose_api_variable_result4[0] == "#"):

                        final_tweet = "🏦 " + client_text

                        if (final_tweet != last_tweet):

                            client.create_tweet(text=final_tweet)

                            mysql_database_insert(rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"), dolar_cost)

                            auxiliar = rose_api_variable2

                    elif (rose_api_variable_result3[0] == "#"):

                        final_tweet = "🟢 " + client_text

                        if (final_tweet != last_tweet):

                            client.create_tweet(text=final_tweet)

                            mysql_database_insert(rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"), dolar_cost)

                            auxiliar = rose_api_variable2

                    elif (rose_api_variable_result4[0] == "#"):

                        final_tweet = "🔴 " + client_text

                        if (final_tweet != last_tweet):

                            client.create_tweet(text=final_tweet)

                            mysql_database_insert(rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"), dolar_cost)

                            auxiliar = rose_api_variable2

                    else:

                        if (client_text != last_tweet):

                            client.create_tweet(text=client_text)

                            mysql_database_insert(rose_api_variable3, rose_api_variable1, datetime.now().strftime("%H:%M:%S"), dolar_cost)

                            auxiliar = rose_api_variable2

                    del rose_api_variable_result3, rose_api_variable_result4, last_tweet, client_text

        del rose_api_variable1,rose_api_variable2,rose_api_variable3,rose_api_variable4,rose_price_variable1,dolar_cost, rose_api_variable5, rose_price_variable2
        gc.collect()

    except:

        errors()

        try:

            del rose_api_variable1,rose_api_variable2,rose_api_variable3,rose_api_variable4,rose_price_variable1,dolar_cost, rose_api_variable5, rose_price_variable2
            gc.collect()

        except:

            pass
