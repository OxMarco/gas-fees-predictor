import requests
import sqlite3
import sys, configparser
import json
import os

def ping(session, url):
    try:
        response = session.get(url, allow_redirects=True, timeout=15)
        res = json.loads(response.text)
        return res
    except Exception as e:
        print('http connection error: '+str(e))
        sys.exit(-1)

def save(database, fee, blocknumber):
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print('database connection error: '+str(e))
        sys.exit(-1)

    sql = 'INSERT INTO gas_fees(fee, blocknumber) VALUES('+str(fee)+', '+str(blocknumber)+')'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def clean(database):
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print('database connection error: '+str(e))
        sys.exit(-1)

    sql = "DELETE FROM gas_fees WHERE created < datetime('now', '- 7 days')"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def main():

    # parse configs
    cfparser = configparser.ConfigParser()

    if(os.getenv('APP_ENV') == 'production'):
        cfparser.read('/app/config.ini') # Docker
    else:
        cfparser.read('config.ini') # Local

    database = cfparser['Server']['database']
    api_endpoint = cfparser['Api']['endpoint'] + "?api-key=" + cfparser['Api']['key']

    # proxy setup
    session = requests.session()

    # api endpoint
    data = ping(session, api_endpoint)

    fee = data['average']*100000000
    blocknumber = data['blockNum']

    save(database, fee, blocknumber)

    clean(database)

if __name__ == '__main__':
    main()