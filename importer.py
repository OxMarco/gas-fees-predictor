import requests
import sqlite3
import sys, configparser
import json
import os
import csv

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

def main():

    # parse configs
    cfparser = configparser.ConfigParser()

    if(os.getenv('APP_ENV') == 'production'):
        cfparser.read('/app/config.ini') # Docker
    else:
        cfparser.read('config.ini') # Local

    database = cfparser['Server']['database']

    with open('gasprice.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                save(database, row[2], row[1])
                line_count += 1

if __name__ == '__main__':
    main()

