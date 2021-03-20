import sqlite3
import sys, configparser, json
import os

cfparser = configparser.ConfigParser()

if(os.getenv('APP_ENV') == 'production'):
    cfparser.read('/app/config.ini') # Docker
else:
    cfparser.read('config.ini') # Local

database = cfparser['Server']['database']

try:
    connection = sqlite3.connect(database)
except Error as e:
    sys.exit(str(e))

cursor = connection.cursor()

if(os.getenv('APP_ENV') == 'production'):
    sql_file = open("/app/schema.sql") # Docker
else:
    sql_file = open("schema.sql") # Local

sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)