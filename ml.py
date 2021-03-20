import sqlite3
import sys, configparser, json
import pmdarima as pm
from pmdarima.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

def main():
    cfparser = configparser.ConfigParser()
    cfparser.read('config.ini')
    database = cfparser['Server']['database']

    try:
        con = sqlite3.connect(database)
    except Error as e:
        print('database connection error: '+str(e))
        sys.exit(-1)

    with con:
        cur = con.cursor()

        cur.execute("SELECT * FROM gas_fees")
        data = cur.fetchall()

    d = []
    for x in data:
        if(x[0] > 4000):
            d.append(x[1])

    y = np.asarray(d)
    print(y)
    train, test = train_test_split(y, train_size=100)

    # Fit your model
    model = pm.auto_arima(train, seasonal=True)

    # make your forecasts
    forecasts = model.predict(test.shape[0])  # predict N steps into the future

    # Visualize the forecasts (blue=train, green=forecasts)
    x = np.arange(y.shape[0])
    plt.plot(x[:100], train, c='blue')
    #plt.plot(x[118:], forecasts, c='green')
    plt.show()

if __name__ == '__main__':
    main()
