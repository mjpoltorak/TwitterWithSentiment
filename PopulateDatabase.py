import psycopg2
import pandas as pd
import json
import requests
import time

Location = "./NAS.csv"
Location2 = "./NYSE.csv"

df = pd.read_csv(Location)
df2 = pd.read_csv(Location2)
dfticker = df["Symbol"]
df2ticker = df2["Symbol"]
lista = dfticker.append(df2ticker)

openfigi_url = 'https://api.openfigi.com/v1/mapping'
openfigi_apikey = '28fd4b05-17d4-4d89-8d72-294e480749c5'  # Put API Key here
openfigi_headers = {'Content-Type': 'text/json'}



if openfigi_apikey:
    openfigi_headers['X-OPENFIGI-APIKEY'] = openfigi_apikey



conn = psycopg2.connect("dbname='postgres' user='postgres' host='dev-datafactory-postgresql.csodrrohkuas.us-east-1.rds.amazonaws.com' password='sbterminal'") #GLobal host
cur = conn.cursor()

count = 0

for i in lista:
    print(i)
    jobs = [{'idType': 'TICKER', 'idValue': i, "exchCode":"US"}]

    r = requests.post('https://api.openfigi.com/v1/mapping',
                      headers=openfigi_headers,
                      data=json.dumps(jobs))
    print(r.status_code)


    for job, result in zip(jobs, r.json()):
        count += 1
        print(count)
        if count % 100 == 0:
            print("Sleeping to wait for more API requests")
            time.sleep(85)  #The information on the website is an estimate. After trial and error this is the true lowest time

        else:
            figi_list = result.get('data')
            if figi_list is None:
                print(figi_list)
                # insert = f"INSERT INTO tickernamesentiment VALUES ('{i}', '{figi_list}');"
                # cur.execute(insert)
                # conn.commit()
            else:
                figi_list = figi_list[0]['name']
                print(figi_list)
                # figi_list = figi_list.replace("'", "")
                # insert = f"INSERT INTO tickernamesentiment VALUES ('{i}', '{figi_list}');"
                # cur.execute(insert)
                # conn.commit()





