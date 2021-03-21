# gas-fees-predictor
Predict Ethereum gas fees in the next few days (<5) using an ARIMA statistical model and historical data from etherscan API.

## Files
In order to start tinkering, you need to run the following files in the exact order:

*init_db.py*
creates the sqlite3 db

*importer.py*
imports the CSV dataset inside the database

*ml.py*
contains the statistical analysis code producing a visual output graph
